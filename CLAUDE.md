# CLAUDE.md

Context for Claude Code working in this repo.

## What this is

A working prototype of document typing for specialty insurance submissions (Send / Duck Creek
underwriting workbench). Laya, an open-weight non-autoregressive "System 1" decision model, makes a
`choice` decision over five document types. A confidence gate routes each document to a typed
extractor or an LLM fallback. Every decision and label lands in a label store that feeds versioned
training snapshots, golden-set eval and a promotion gate.

Document types and the descriptions Laya scores: `CRITERIA` in `src/doctype/domain.py`
(`sov`, `loss_run`, `acord`, `broker_email`, `other`).

## Commands

```bash
uv sync --extra dev                      # add --extra laya / --extra bedrock as needed
uv run pytest                            # must stay green
uv run doctype demo                      # offline end-to-end run, writes var/runs/<ts>/
uv run doctype --model laya probe "..."  # raw Laya answer
uv run doctype --model laya --fallback ollama demo
```

Python is pinned to 3.12 (`.python-version`) because torch wheels lag new Python releases. The
machine has 3.15 system-wide; let uv manage the interpreter.

## Architecture (hexagonal, keep it that way)

- `domain.py` types only, no I/O, no third-party imports
- `ports.py` protocols; services depend only on these
- `services/` label store, intake, evaluation, training pipeline, calibration
- `adapters/` real and simulated implementations of ports
- `container.py` the only place adapters are chosen; `cli.py` thin
- Optional dependencies (laya, boto3) are imported lazily inside adapters so the core runs without them

## Invariants the code enforces (do not weaken)

1. Every Laya call is written to the decision log, with the full distribution, model version and route, before routing.
2. Labels carry a source and trust tier: HUMAN > DOWNSTREAM > LLM_FALLBACK. Disagreement below HUMAN returns no label (goes to review, not training).
3. Snapshots exclude golden documents by hash AND by template group, so near-duplicates cannot leak.
4. The golden set is the exam: never trained on, never used to fit temperature or threshold.
5. Temperature and threshold are fitted only on the random audit sample, drawn from every decision whatever its route (sampling auto-routed decisions alone selects on confidence and starves calibration while nothing clears the gate), and only with at least 30 audited decisions (`MIN_AUDIT_SAMPLE` in cli.py).
6. Promotion needs no accuracy loss, no per-class recall drop over 0.05, no ECE increase over 0.02 (`PromotionPolicy`).

## Verified external APIs (checked October 2026, Context7 plus installed packages)

- **laya 0.4.15** `laya.load(model_id_or_path, subfolder=..., device=...)`; `agent.predict(state, questions)`.
  Choice answer: `{"choice", "probabilities": {label: p}, "confidence" (1 - normalised entropy), "answer_confidence" (max p, the value to gate on)}`.
  Fine-tune: `laya.train.finetune(data, model_dir, output_dir, config=TrainConfig(...), device="auto")`, returns a report with `train_items`, `skipped`, `temperature`.
  Training rows: `{state, questions, gold: {qid: {probabilities}}}` or `{state, questions, expected: {qid: label}}`. No per-row weight; unknown keys ignored. We encode trust as soft `gold` targets (see `adapters/laya_trainer.py`).
  Checkpoints ship over-confident; refit calibration on own data. English root is 512 tokens, typed-decisions and multilingual 1k.
- **Ollama** `/api/chat` with `format` (JSON schema), `stream: false`, `think: false`, `options.temperature`.
- **Bedrock** `bedrock-runtime` `converse(modelId, messages, system=[{text}], inferenceConfig={maxTokens, temperature})`, response `output.message.content[].text`. Checked against the botocore service model.

## Status: real vs simulated

| Part | Status |
|---|---|
| Laya inference | Real adapter, untested against downloaded weights yet. Run `probe` first. |
| Laya fine-tune | Real adapter against the verified API, not yet run end to end |
| Ollama / Bedrock fallback | Real; model `qwen3.8:27b-mlx` set in `.env` |
| Extractors | Regex stand-ins with the real accept/reject contract |
| Ops reviewer | Simulated from `truth` in `data/production/*.jsonl` |
| Storage | Local JSONL and file manifests; production target is per-tenant Iceberg tables and S3 manifests |
| Golden set | 10 examples, illustrative only; real eval needs a few hundred per class |

## Suggested next work

1. Download Laya, run `doctype --model laya probe` and `eval`, compare against the simulated baseline.
2. Once `qwen3.8:27b-mlx` is pulled, run the demo with `--fallback ollama`, check fallback agreement with truth.
3. Run a real fine-tune on Apple Silicon (`LAYA_DEVICE=mps`) and confirm `report["skipped"]` is empty.
4. Grow the golden set and production samples with realistic, anonymised broker documents.
5. Add a Step Functions / CDK sketch for the training pipeline and Iceberg adapters for the label store.

## Conventions

- UK English, plain direct prose, no em dashes in docs or comments.
- Keep services free of adapter imports; add a port before adding a new dependency to a service.
- Add or update a test with every behaviour change.
