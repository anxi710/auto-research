# Claims from the synthetic practice run

All claims below apply only to E001 protocol 1 and its recorded environment.
They describe synthetic practice data, not evidence about real research outcomes.
The [raw output](tasks/T001/attempts/A001/artifacts/results.json) identifies rows by `case_id` and `order_index`.

| ID | Claim | Type | Evidence | Opposing evidence | Status | Limit |
| --- | --- | --- | --- | --- | --- | --- |
| C001 | The plain loop's output depends on order for the cancellation case. | observation | E001: cancellation orders 1, 3, 4, 6 return 0. Orders 2 and 5 return 1. | The control is invariant across all six orders. | supported | These inputs and this environment only. |
| C002 | math.fsum has a smaller error in four tested orderings and equal error in eight. | observation | E001: cancellation orders 1, 3, 4, 6 have errors 1 and 0. The other eight rows tie. | The eight ties limit any strict-improvement claim. | supported | No evidence about other inputs or platforms. |
| C003 | math.fsum strictly improves every tested ordering. | hypothesis | Four cancellation rows show smaller error. | All six control rows and cancellation orders 2 and 5 have equal error. | opposed | The claim fails within this fixed example. |

The current [review](reviews/R001.md) records whether the exact result meets its task contract.
Task acceptance does not extend these claims beyond their stated scope.
Assistant token and cost use remain unknown.
No speed, significance, novelty, or multi-agent benefit was measured.
