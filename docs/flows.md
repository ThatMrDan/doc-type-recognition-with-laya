# Components, flows and sequences

How a run moves through the code, which component does what, and how each step shows up in
`var/runs/<ts>/trace.json`. Span names in `code font` are the names you will see in the trace.

Observed figures come from a real run on 25 October 2026: Laya `typed-decisions`, fallback
`ollama:qwen3.8:27b-mlx`, export trainer, 28 production documents (`var/runs/20261025-200303`).

## 1. Components

![Components: CLI calls services, services call ports only, adapters implement ports and reach Laya, Ollama, Bedrock and local disk](diagrams/components.svg)

*The CLI calls services; services see only ports; `container.py` picks one adapter per port from `Settings`. Adapters are the only code that touches Hugging Face, Ollama, Bedrock or disk.*

| Component | File | Responsibility |
|---|---|---|
| CLI | `cli.py` | Parses flags, runs `demo` and `eval`, plays the simulated ops reviewer, runs calibration |
| Composition root | `container.py` | The only place adapters are chosen, from `Settings` (env, `.env`, CLI flags) |
| IntakeService | `services/intake.py` | One document: predict, gate, audit, fallback, extract, label, review |
| ExtractionRouter | `services/intake.py` | Runs the extractor for the chosen type; if it rejects, tries the others to find the real type |
| LabelStoreService | `services/label_store.py` | Decision log, audit sampling, labels with provenance, label resolution, training snapshots |
| TrainingPipeline | `services/training.py` | Snapshot, eval current, fine-tune, eval candidate, promote |
| EvalService, PromotionPolicy | `services/evaluation.py` | Golden-set metrics and the promotion gate |
| calibration | `services/calibration.py` | Temperature and threshold fitted on the audit sample |
| LayaModel | `adapters/laya_model.py` | `laya.load(...)`, `agent.predict(text, questions)`, answer to a distribution over `DOC_TYPES` |
| OllamaFallback, BedrockFallback | `adapters/fallback.py` | LLM classification with a JSON schema; unparseable output becomes `other` |
| SchemaExtractor | `adapters/extractors.py` | Regex stand-ins; `ok=False` means "not my type" |
| Storage | `adapters/storage.py` | JSONL decision log and labels, file snapshot manifests, in-memory text store and queues |
| Trainers | `adapters/laya_trainer.py`, `adapters/simulated.py` | Export `train.jsonl`, real `laya.train.finetune`, or the offline stand-in |
| OtelTracer | `adapters/tracing.py` | OpenTelemetry spans, written as one nested `trace.json` when the run closes |

## 2. A demo run

`doctype demo` is one trace. `build_app` first chooses the adapters and opens the tracer; then the
root span `demo` opens and these steps nest under it, in order:

1. `week` (week1, 20 documents): `IntakeService.process` per document, then `ops.review` labels everything queued.
2. `calibration`: fits temperature and threshold if there are at least 30 audited decisions, otherwise keeps 0.85.
3. `training.run`: snapshot, eval, fine-tune, and promotion when there is a candidate. Writes `eval.json`.
4. `week` (week2, 8 documents) at the threshold calibration left, then `ops.review` again.

When `demo` closes, even after an exception, the tracer writes `trace.json`.

![Timeline of one real demo run: 31.6 s, 89% of it in the LLM fallback](diagrams/run-timeline.svg)

*Measured from `trace.json`. Each block in the `intake.document` row is one document: blue is Laya, orange is the Ollama fallback. Calibration and the training run sit in the 0.6 s gap between the weeks, shown zoomed below.*

## 3. One document through intake

Every document is an `intake.document` span. Its children appear in this order.

![Sequence for one document through intake](diagrams/intake-sequence.svg)

*Left gutter: the span each call appears under in `trace.json`. The decision is logged before any routing, so the decision log has every Laya call even if a later step fails.*

### Routes a document can take

![Routes taken by the 28 documents of the real run](diagrams/routes.svg)

*Line width is the number of documents. Nothing cleared the 0.85 gate, so all 28 went to the fallback; 11 were also picked for audit.*

Step sequences seen in the traces, children of `intake.document` in order:

| Sequence | Real run (28) | Simulated run (28) | Meaning |
|---|---|---|---|
| `model.predict > gate > fallback.classify > extract` | 16 | 10 | Below threshold, LLM typed it, extractor accepted |
| `model.predict > gate > review.queue > fallback.classify > extract` | 10 | 5 | Same, and picked for audit |
| `model.predict > gate > review.queue > fallback.classify > review.queue` | 1 | 2 | Audited, LLM said `other`, so queued twice |
| `model.predict > gate > fallback.classify > review.queue` | 1 | 1 | LLM said `other` |
| `model.predict > gate > extract` | 0 | 6 | Auto-routed |
| `model.predict > gate > review.queue > extract` | 0 | 4 | Auto-routed and audited |

The recovery and "no extractor accepted" branches did not occur in either run; the test
`test_schema_failure_produces_downstream_label` covers recovery.

## 4. Labels and how they are trusted

![Label trust tiers, soft training targets and resolution](diagrams/labels.svg)

*The tier sets both how conflicts resolve and how hard a label pushes in training: a HUMAN label is one-hot, an LLM label puts 0.4 on its type and spreads 0.6 over the other four.*

The ops reviewer is simulated: it labels every queued item with `truth` from
`data/production/*.jsonl`. The HUMAN labels on audited decisions are what calibration fits on.

## 5. Training run

![Training run: snapshot, eval, fine-tune, then export or promotion gate](diagrams/training.svg)

*Values are from the real run. With `ExportTrainer` the run stops after writing `train.jsonl`; a real or simulated trainer continues to the candidate eval and the promotion gate.*

The real run used `ExportTrainer`, so the trace stops at `trainer.fine_tune` with
`candidate: "none (exported data only)"`. The simulated run continues to `eval.candidate` and
`promotion.decide` and promoted `candidate-v2`.

## 6. Span reference

| Span | Emitted by | Key attributes | Events |
|---|---|---|---|
| `demo` | `cli.cmd_demo` | `model`, `fallback`, `trainer`, `tenant`, `run_dir` | |
| `eval` | `cli.cmd_eval` | `model_version`, `threshold`, `accuracy`, `ece`, `coverage`, `recall.*` | |
| `week` | `cli._run_week` | `week`, `model_version`, `threshold`, `documents`, `auto_routed` | |
| `intake.document` | `IntakeService.process` | `doc_id`, `tenant_id`, `template_group`, `decision_id`, `final_type`, `path` | |
| `model.predict` | `IntakeService` | `model_version`, `probabilities.*` | |
| `gate` | `IntakeService` | `threshold`, `decision_id`, `doc_hash`, `predicted`, `confidence`, `route`, `audited` | |
| `review.queue` | `IntakeService._push_review` | `decision_id`, `reason` | |
| `fallback.classify` | `IntakeService` | `actor`, `doc_type`, `agrees_with_model` | `label` (LLM_FALLBACK) |
| `extract` | `IntakeService` | `doc_type`, `ok`, `error`, `recovered_type` | `label` (DOWNSTREAM) |
| `ops.review` | `cli._run_week` | `actor`, `items` | `label` per item (HUMAN, reason, doc_type) |
| `calibration` | `cli._demo_steps` | `min_audit_sample`, `audited`, `fitted`, `temperature`, `threshold` | |
| `training.run` | `TrainingPipeline.run` | `tenant_id`, `new_version`, `threshold`, `min_source`, `promoted`, `reasons` | |
| `snapshot.build` | `TrainingPipeline` | `uri`, `snapshot_id`, `examples`, `excluded.*` | |
| `eval.current`, `eval.candidate` | `TrainingPipeline._evaluate` | `model_version`, `golden_version`, `n`, `accuracy`, `ece`, `coverage`, `auto_error`, `recall.*` | |
| `trainer.fine_tune` | `TrainingPipeline` | `base`, `trainer`, `candidate` | |
| `promotion.decide` | `TrainingPipeline` | `current`, `candidate`, `promoted`, `reasons` | |

Every node also carries `trace_id`, `span_id`, `start` (UTC ISO), `duration_ms` and `children`.
A step that raised has `"status": "ERROR"` and an `exception` event with the message.
Document text is never recorded.

## 7. Where the time goes (real run)

| Span | Count | Total ms | Median ms | Max ms |
|---|---|---|---|---|
| `fallback.classify` | 28 | 28,134 | 540 | 10,691 |
| `model.predict` | 28 | 2,829 | 49 | 1,143 |
| `eval.current` | 1 | 441 | 441 | 441 |
| `snapshot.build` | 1 | 31 | 31 | 31 |
| `gate` | 28 | 15 | 0.4 | 4 |
| `extract` | 26 | 1 | 0.0 | 0 |

The whole run took 31.6 s and the fallback took 28.1 s of it (89%). The first call, about
10.7 s, includes loading the 27B model into memory. Each Laya call is about 50 ms once warm.
Because nothing cleared the 0.85 gate, every document paid for the fallback.

## 8. Reading a trace

```bash
# the run's top-level steps
jq -r '.[0].children[].name' var/runs/<ts>/trace.json

# one line per document: id, Laya's choice and confidence, route, final type
jq -r '.. | objects | select(.name? == "intake.document")
       | [.attributes.doc_id, (.children[] | select(.name == "gate") | .attributes.predicted,
          .attributes.confidence, .attributes.route), .attributes.final_type] | @tsv' var/runs/<ts>/trace.json

# any step that failed
jq '.. | objects | select(.status? == "ERROR") | {name, events}' var/runs/<ts>/trace.json
```

Spans are held in memory and written when the run closes, including when it raises. A run killed
outright (for example `kill -9`) leaves no trace file.
