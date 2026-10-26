# Offline claim-evidence example

This small fixture demonstrates a claim-to-source chain with deliberately limited support.
It uses hand-authored synthetic fractions, not a model trial, scientific experiment, or real accuracy result.
The existing summation-order example is separate and unchanged.

Run the read-only checker from the toolkit repository root with Python 3.9 or later.
No dependencies, accounts, source downloads, or network requests are needed.

```bash
python3 -B skills/research-workflow/scripts/lint_records.py \
  --root examples/claim-evidence \
  --task tasks/T001/task.json \
  --result tasks/T001/attempts/A001/result.json \
  --review reviews/R001.md
```

The expected exit code is `0` and the JSON report contains an empty `diagnostics` list.
That checks the selected file bindings, exact quotes, numeric context, and review partition.
It does not establish scientific support or human approval.

Run the fixture replay checks from the same directory.

```bash
python3 -B -m unittest discover -s tests -p 'test_evidence_example.py' -v
```

The checks compare fixed digests, repeat the CLI inspection in a temporary copy,
independently inspect the decimal comparison, and verify that the example stays unchanged.

## Expected limits

The [claim index](CLAIMS.md) leads to four exact candidate statements.
Only the two declared D1/test-v1 fractions can be read from the metric rows.
One row cannot justify an every-dataset or every-split extension.
The difference between the recorded fractions is 0.02, below a proposed minimum of 0.05.
No variance, significance, general accuracy, or causal conclusion follows.
The fictional literature entry intentionally has no local content or full-text hash.
Its asserted D2 result cannot be inspected.
The stored formal assessments and review coverage are in [R001](reviews/R001.md#task-acceptance).

The review is a same-author AI simulation for this fixture contract.
It does not claim independent candidate review.
[Human review](reviews/R001.md#human-decision) remains pending with no approved next action or waiver.

## Record boundaries

The [current task](tasks/T001/task.json) requires a ledger artifact.
The [fixed contract](tasks/T001/attempts/A001/task.json) and [result](tasks/T001/attempts/A001/result.json) bind the submitted version.
The [ledger](tasks/T001/attempts/A001/artifacts/evidence-ledger.json) pins the raw manuscript and metric bytes.
Paths are relative to this example's root.
The numeric `experiment` kind demonstrates the schema; it does not imply that an experiment ran.
The `seed` value is a context label with no executed random process.

Keep the submitted attempt and completed review unchanged.
Create a new attempt for changed claims or evidence and a new review for a changed decision.
Use the existing supersedes convention when replacing a review of the same exact result.
Do not regenerate hashes to repair historical records in place.
