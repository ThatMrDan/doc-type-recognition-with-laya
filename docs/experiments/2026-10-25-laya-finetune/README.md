# First real Laya fine-tune, 25 October 2026

## Setup

- Base and serving model: `convaiinnovations/laya` `typed-decisions` (laya 0.4.15), Apple Silicon, `LAYA_DEVICE=mps`.
- Fallback labeller: `ollama:qwen3.8:27b-mlx`.
- Data: week 1 = 140 documents (20 hand-written + 120 from `scripts/generate_production.py`, seed 2026).
- Snapshot: 136 examples (79 LLM_FALLBACK, 55 HUMAN, 2 DOWNSTREAM); 1 golden hash and 1 golden template excluded.
- Command:

```bash
LAYA_BASE=typed-decisions LAYA_DEVICE=mps uv run doctype --model laya --fallback ollama --trainer laya demo
```

`LAYA_BASE` must be set: the `config.py` default is `english` (the 512-token root), which is a
different model from the one serving traffic. `laya.router.resolve_model_spec` accepts
`typed-decisions` as an alias.

- `TrainConfig` defaults: 4 epochs, 123 train items, 13 calibration items. Loss 1.43 to 0.96.
  Laya warned that calibration was fitted on only 13 items.

Files here: `train_report.json` (laya's report), `demo-finetune.log` (the run above) and
`demo-export-140.log` (the same data with the export trainer, before fine-tuning).

## Results

Before fine-tuning, on the 140 week 1 documents (export run): Laya top-1 119/140 (85%), Qwen
138/140; Laya called 11 of 13 `other` documents `acord`; nothing cleared 0.85 (max 0.72). The
calibration step fitted temperature 0.50 (the grid floor) and threshold 0.60 on 44 audited decisions.

Comparison of the base and fine-tuned checkpoints (`tools/compare_models.py`):

| | Current | Fine-tuned |
|---|---|---|
| golden-v1 (10) accuracy | 0.90 | 1.00 |
| Held-out (150, generator seed 99) accuracy | 0.82 | 1.00 |
| Held-out hard cases (27) | 0.70 | 1.00 |
| Held-out recall, `other` | 0.16 | 1.00 |
| Median confidence | 0.40 | 0.65 |
| Auto-routed at 0.6 (error) | 4% (17%) | 82% (0%) |
| Auto-routed at 0.85 | 0% | 0% |
| ECE (held-out) | 0.42 | 0.35 |

The promotion gate passed on golden-v1 (accuracy 1.00, ECE 0.32) and week 2 auto-routed 7 of 8.

## Caveats

- The held-out batch comes from the same generator as the training data, so 150/150 measures the
  generator's phrasing as much as the document types. golden-v2 (`docs/golden/`) exists to fix this.
- The fine-tuned model is still under-confident (accuracy 1.00, median confidence 0.65, max 0.77):
  it needs temperature calibration or the lower threshold before 0.85 means anything.
- The checkpoint is `models/candidate-v2/checkpoint` (1.6 GB, not in git). Re-create it with the
  command above; the registry promotion only lived for that run.
