# Doc type recognition with Laya

Document typing for specialty insurance submissions. Laya makes a fast `choice`
decision over five document types, a confidence gate routes each document to a
typed extractor or an LLM fallback, and every decision and label lands in a label
store that feeds versioned training snapshots, golden-set eval and a promotion gate.

```
document -> Laya -> decision log -> gate --auto--> typed extractor --schema fail--> DOWNSTREAM label
                                       \--low---> LLM fallback ----------------> LLM_FALLBACK label
                       random audit sample + review queue -----------------------> HUMAN label
label store -> snapshot (golden excluded) -> fine-tune -> eval on golden -> promote or reject
```

Document types: `sov`, `loss_run`, `acord`, `broker_email`, `other`. The option
descriptions Laya scores live in `src/doctype/domain.py` (`CRITERIA`).

## Setup

Laya needs PyTorch, which lags new Python releases, so the project pins Python
3.12 (`.python-version`). uv fetches it if you don't have it.

```bash
uv sync --extra dev --extra trace    # simulated adapters only, no model downloads
uv run pytest
uv run doctype demo                  # whole flow, offline
```

### Real Laya

```bash
uv sync --extra dev --extra trace --extra laya
uv run doctype probe "Schedule of values 22 locations TIV 140m"   # raw SDK output, first download
uv run doctype --model laya classify "Loss run 5 years incurred 2.1m"
uv run doctype --model laya eval
uv run doctype --model laya demo     # trainer defaults to export with a real model
```

`probe` prints the raw SDK answer. For a choice question laya 0.4.15 returns
`probabilities` as a dict keyed by label and `answer_confidence` as max(p). If
`laya.load` hangs, the adapter already sets `USE_TF=0`, the model card's fix.

### Fine-tuning real Laya

```bash
uv run doctype --model laya --trainer export demo   # writes models/candidate-v2/train.jsonl
uv run laya-train --data models/candidate-v2/train.jsonl --base english \
                  --out models/candidate-v2/checkpoint --device mps
uv run doctype --model laya --trainer laya demo     # or let the pipeline call finetune itself
```

Rows use Laya's `{state, questions, gold}` schema. Laya has no per-row weight, so
label trust is a soft target: a human label is one-hot, an LLM label (weight 0.4)
keeps 0.4 on its label and spreads 0.6 over the others.

The default checkpoint is `typed-decisions` (1k context). Set `LAYA_SUBFOLDER=`
(blank) for the English root checkpoint (512 tokens) or `multilingual`.

### LLM fallback

```bash
# Local, free, offline
ollama pull qwen3.8:27b-mlx
uv run doctype --fallback ollama demo

# Bedrock, the production path (Converse API, any text model)
uv sync --extra dev --extra trace --extra bedrock
export AWS_PROFILE=...   # credentials with bedrock:InvokeModel
uv run doctype --fallback bedrock demo
```

Defaults are in `.env.example`; copy it to `.env` to change them.

## Commands

| Command | What it does |
|---|---|
| `doctype demo` | Week 1 intake, ops review, calibration, training run, week 2 on unseen documents |
| `doctype classify TEXT` | One text through the model and the gate |
| `doctype eval [--temperature T]` | Current model against the golden set |
| `doctype probe TEXT` | Raw Laya SDK output for one text |

Global flags: `--model simulated|laya`, `--fallback simulated|ollama|bedrock`,
`--trainer simulated|export|laya`, `--threshold`.

Each demo run writes `decisions.jsonl`, `labels.jsonl`, the snapshot
`manifest.json`, `eval.json` and `trace.json` under `var/runs/<timestamp>/`.

`trace.json` is the run as an OpenTelemetry trace: a tree of timed steps (`demo` > `week` >
`intake.document` > `model.predict`, `gate`, `review.queue`, `fallback.classify`, `extract`, then
`ops.review`, `calibration` and `training.run` with its snapshot, eval, fine-tune and promotion steps).
Each step records what was invoked (model version, fallback actor, trainer), what it returned and what
was decided, plus its duration. Failed steps carry `"status": "ERROR"` and the exception. Document
text is never recorded; documents are identified by id, hash and template group. `doctype eval` writes
a trace too. Set `DOCTYPE_TRACE=off` to turn tracing off, or run without the `trace` extra.

## Layout

```
src/doctype/
  domain.py            types, CRITERIA, no I/O
  ports.py             protocols the services depend on
  services/
    label_store.py     decision log, labels with provenance, snapshots
    intake.py          gate, fallback, extraction router, label capture
    evaluation.py      golden-set metrics (accuracy, per-class P/R, ECE, coverage) and promotion policy
    training.py        snapshot -> fine-tune -> eval -> promote
    calibration.py     temperature scaling and threshold tuning on the audit sample
  adapters/
    laya_model.py      real Laya via the laya SDK
    laya_trainer.py    export to train.jsonl, or laya.train.finetune
    fallback.py        Ollama and Bedrock classifiers
    simulated.py       offline stand-ins for Laya, the trainer and the LLM
    extractors.py      schema-checked regex extractors
    storage.py         in-memory and JSONL/file stores
    tracing.py         OpenTelemetry tracer writing trace.json, and a no-op tracer
  container.py         composition root
  cli.py
data/
  golden/golden-v1.jsonl        frozen exam, never trained on
  production/week1.jsonl, week2.jsonl   sample traffic with ground truth for the simulated reviewer
```

## Rules the code enforces

- Every Laya call is logged with its full distribution, model version and route before anything else happens.
- Labels carry a source and trust tier. Human beats downstream beats LLM. Disagreement below human sends the example to review, not training.
- Snapshots drop golden documents by hash and by template group, so near-duplicates can't leak.
- Promotion requires no accuracy loss, no per-class recall drop over 5 points, and no calibration regression over 0.02 ECE.
- Temperature and threshold are fitted on the random audit sample, drawn from auto-routed and fallback-routed decisions alike, never on the golden set, and only once there are at least 30 audited decisions.

## What is real and what is simulated

| Part | Status |
|---|---|
| Laya inference | Real, via `laya.load` and `agent.predict` (documented SDK calls) |
| Laya fine-tuning | `laya.train.finetune` with the `{state, questions, gold}` row schema, both checked against laya 0.4.15. Slow on CPU; use `LAYA_DEVICE=mps` on a Mac. |
| Ollama and Bedrock fallback | Real HTTP and Converse API calls |
| Extractors | Regex stand-ins with the real contract (accept or reject) |
| Ops reviewer | Simulated from ground truth in the sample files |
| Storage | Local JSONL; production would be Iceberg tables and S3 manifests per tenant |

The golden set has 10 examples, so its numbers say little. Real eval needs a few
hundred hand-labelled documents per class.
