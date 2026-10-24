# Summation order: a complete practice example

This synthetic exercise follows one question from a fixed plan through local execution and separate AI review.
It uses two small datasets and the Python standard library.
It illustrates saved evidence and honest limits, with no claim of research novelty or a multi-agent advantage.

The user approved P1 on 2026-10-23.
The measured run completed with exit code `0` on CPython 3.14.8 and Linux.
The independent AI review accepted the exact result after one replay reproduced all 7,798 output bytes.
The [brief](BRIEF.md), [source notes](LITERATURE.md), [question](questions/Q001.md), and [protocol](experiments/E001.md) state the scope before execution.

## Observed result

The [raw JSON](tasks/T001/attempts/A001/artifacts/results.json) contains 12 ordering rows and 24 method outputs.
Identify a row by its `case_id` and `order_index`.
Each row preserves input and output float identities, the exact reference, and exact absolute errors.
The [execution manifest](tasks/T001/attempts/A001/artifacts/manifest.json) and [log](tasks/T001/attempts/A001/artifacts/run.log) record the actual run.

| Output rows | Exact reference | Plain loop output and error | math.fsum output and error |
| --- | --- | --- | --- |
| `control`, orders 1 through 6 | 6 | Output 6, error 0. | Output 6, error 0. |
| `cancellation`, orders 1, 3, 4, 6 | 1 | Output 0, error 1. | Output 1, error 0. |
| `cancellation`, orders 2, 5 | 1 | Output 1, error 0. | Output 1, error 0. |

Eight orderings produced equal errors for the two methods.
Four cancellation orderings produced a smaller error with `math.fsum`.
The ties oppose a claim of strict improvement on every tested ordering.
These observations support an ordering effect for the plain loop on this cancellation case.
The [claim record](CLAIMS.md) keeps each statement's evidence and scope together.
No timing comparison, statistical test, or general method claim follows from this small example.

## Inspect the records

The coordinator saved [T001 revision 1](tasks/T001/task.json) and its [fixed copy](tasks/T001/attempts/A001/task.json) before execution.
The worker submitted [result.json](tasks/T001/attempts/A001/result.json) after its artifacts were complete.
The result binds the script, inputs, raw output, log, and manifest by SHA256.
It records execution completion separately from the [review decision](reviews/R001.md).
The [state file](STATE.md) indexes the current decision and next action.

The experiment plan, brief, source notes, question, script, and inputs are fixed inputs for this attempt.
Keep the submitted attempt unchanged.
Use a new attempt for a correction that changes its evidence.
The result's pending-review text describes submission time and stays unchanged after review.
The later review and state record the current decision.

## Replay into a new directory

Run these commands from the toolkit repository root with Python 3.9 or newer.
The first command creates a new temporary directory.
The script prints JSON to standard output and does not change the saved example.
A successful comparison reproduces these numerical bytes, not research quality or another harness's recovery behavior.

```bash
replay_dir="$(mktemp -d)"
python3 -B examples/summation-order/tasks/T001/attempts/A001/artifacts/run.py \
  examples/summation-order/tasks/T001/attempts/A001/artifacts/inputs.json \
  > "$replay_dir/results.json"
cmp examples/summation-order/tasks/T001/attempts/A001/artifacts/results.json "$replay_dir/results.json"
```

To inspect the saved contract and review, run the existing checker:

```bash
python3 -B skills/research-workflow/scripts/lint_records.py \
  --root examples/summation-order \
  --task tasks/T001/task.json \
  --result tasks/T001/attempts/A001/result.json \
  --review reviews/R001.md
```

The checker inspects supplied records and hashes.
A clean diagnostic report does not establish scientific correctness or complete review history.
The independent review records its numerical inspection separately.
This example does not test DSH, interruption, unknown remote jobs, or cross-harness recovery.
