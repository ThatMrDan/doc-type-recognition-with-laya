# golden-v2 build: status and handoff (25 October 2026)

Where the golden-v2 build stands, what is left, and how to finish it on Bedrock. The design comes
from `reports/Golden set for document typing.md` (section "Golden-v2 build specification"); the
labelling rules are `docs/golden/guideline-v1.md`.

## Decisions already taken

- Edge-case taxonomy (guideline rules 3, 6, 8, 13): ACORD 139 is `sov`; ACORD certificates
  (24/25/27/28) are `other`; a no-known-loss letter is `loss_run`; an email that is mostly a pasted
  table takes the table's class.
- `CRITERIA` in `src/doctype/domain.py` stays unchanged for golden-v2, so the base and fine-tuned
  checkpoints are compared on the descriptions they were trained with.
- Generator A is Claude (hand-authored). Generator B must be neither Claude, the training
  generator (`scripts/generate_production.py`) nor the fallback model family (Qwen).
- Judging is cross-family: no row is judged by the family that wrote it. A third family is not
  required.
- The draft is produced with a blind labelling kit; it is not used by the promotion gate until two
  annotators and an adjudicator have labelled every row.

## Done

| Piece | Where | State |
|---|---|---|
| Research notes and report | `research_notes/`, `reports/` | Done |
| Guideline v1.0 | `docs/golden/guideline-v1.md` | Done (18 rules) |
| Generator A rows | `tools/golden/rows/a_*.jsonl` | 349 rows: 225 core, 84 boundary, 40 contrast |
| Generator B rows | `tools/golden/rows/b_sov.jsonl`, `b_loss_run.jsonl` | 74 rows from `ollama:gemma3:12b` (sov 37, loss_run 37) |
| Checks on generator A | `tools/golden/out/checks*.json*` | No leaks; max char 5-gram similarity to training 0.19; golden vs training discriminator 0.96 |
| Judge votes | `tools/golden/out/judge_*.jsonl` | 10 rows by `llama3.1:8b`, 1 by `gemini-3.6-flash`; the rest to do |
| Pipeline | `tools/golden/*.py` | `gen_b.py`, `noise.py`, `judge.py`, `checks.py`, `assemble.py`; providers `ollama`, `gemini`, `bedrock` |

Why it stopped: local `gemma3` and `llama3.1` made the laptop run hot, and Gemini's free tier
allows 20 requests per model per day (`gemini-3.8-flash` was also overloaded). Both scripts now
write as they go and resume.

## To finish on Bedrock

Prerequisites on the work machine:

```bash
uv sync --extra dev --extra trace --extra bedrock --extra laya
aws sts get-caller-identity                       # credentials with bedrock:InvokeModel
aws bedrock list-foundation-models --region eu-west-2 --query "modelSummaries[].modelId"
```

Model access must be enabled in the Bedrock console for the models used. Set `AWS_REGION` (and
`AWS_PROFILE` if needed) in the environment or `.env`.

Pick two Bedrock model ids:

- `B_MODEL`: a family that is not Claude and not Qwen (for example Amazon Nova, Mistral or Meta
  Llama). It writes the remaining generator B rows and judges the Claude-written rows.
- `CLAUDE_MODEL`: an Anthropic model on Bedrock. It judges the generator B rows.

Note that Bedrock has no Google model, so generator B will hold two families (74 gemma3 rows plus
the new ones). Each row records its `generator`, so reports can split them. If a single B family is
preferred, delete `rows/b_sov.jsonl` and `rows/b_loss_run.jsonl` and generate all five classes.

Then, from `tools/golden/`:

```bash
uv run python gen_b.py --provider bedrock --model $B_MODEL --only acord broker_email other
uv run python noise.py
uv run python judge.py --provider bedrock --model $B_MODEL --families A --workers 6
uv run python judge.py --provider bedrock --model $CLAUDE_MODEL --families B --workers 6
uv run python checks.py
uv run python assemble.py
```

`noise.py` must run after generator B, because it draws invariance parents from every core row.
Invariance rows inherit their parent's family, so the two judge runs cover them. `assemble.py`
writes `data/golden/golden-v2-draft.jsonl`, its `.manifest.json` and the blind labelling kit in
`docs/golden/kit/`.

Afterwards:

1. Score the base and fine-tuned checkpoints on the draft (provisional labels), using
   `tools/compare_models.py` as a starting point. The fine-tuned checkpoint has to be rebuilt first;
   see `docs/experiments/2026-10-25-laya-finetune/README.md`.
2. Write the datasheet (`docs/golden/datasheet-v2.md`): sources, families, counts, checks, judge
   agreement, and the limits (synthetic only, two judge families, B split across two families).
3. Hand the kit to two annotators; adjudicate; freeze as `golden-v2`.

## Open items outside golden-v2

- `LAYA_BASE` defaults to `english` but the serving model is `typed-decisions`; a fine-tune without
  the variable trains a different model.
- `cmd_demo` prints the fitted temperature but never applies it; only the threshold is used.
- The report recommends replacing the promotion gate's point-estimate rules with paired tests
  (McNemar, Brier bootstrap); see "Promotion gate changes".
- Align `CRITERIA` with guideline rules 6, 8 and 13 in the next model version.
- Not in git: `models/` (fine-tuned checkpoint, 1.6 GB), `var/` (run directories), `.env`, and the
  Ollama models.
