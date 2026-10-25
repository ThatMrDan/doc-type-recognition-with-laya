# Generator A authoring scripts (provenance)

How the generator family A rows in `tools/golden/rows/a_*.jsonl` were built. Five Claude
(`claude-opus-5.5`) writers worked in parallel from `tools/golden/AUTHORING.md`, one per class. Each
hand-wrote its documents as data inside a small builder script, which computes ids, totals and
the JSONL layout. These are kept so every row can be traced to its source; they are not part of
the pipeline and are not re-run.

| Class | Files | Output |
|---|---|---|
| sov | `sov/build_sov.py` (with `patch1.py`, `patch2.py` edits, `check.py` and `colcheck.py` checkers) | `a_sov.jsonl`, 63 rows |
| loss_run | `loss_run/gen_loss_run.py` | `a_loss_run.jsonl`, 65 rows |
| acord | `acord/core.py`, `acord/rest.py`, `acord/build.py` | `a_acord.jsonl`, 65 rows |
| broker_email | `broker_email/core.py`, `broker_email/boundary.py`, `broker_email/build.py` | `a_broker_email.jsonl`, 72 rows |
| other | `other/build_a_other.py` | `a_other.jsonl`, 84 rows |

The scripts were written in a scratch folder, so some take input and output paths as arguments
and the patch scripts edit `build_sov.py` in the current directory. The committed JSONL files
are the source of truth.
