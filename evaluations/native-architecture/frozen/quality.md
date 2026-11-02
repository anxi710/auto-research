# Quality evidence

All values below are synthetic test inputs.
Each row reports correct classifications from a fixed test set.
The last column gives the reported 95% Wilson lower confidence bound.

| Model | Parcel type | Correct | Total | Lower bound |
| --- | --- | ---: | ---: | ---: |
| Alpha | Ordinary | 990 | 1000 | 0.982 |
| Alpha | Damaged | 90 | 100 | 0.826 |
| Beta | Ordinary | 980 | 1000 | 0.969 |
| Beta | Damaged | 98 | 100 | 0.930 |

Alpha has 1080 correct classifications from 1100 parcels, or 98.18% pooled accuracy.
Beta has 1078 correct classifications from 1100 parcels, or 98.00% pooled accuracy.
The policy applies to each parcel type. It does not use pooled accuracy.
The fixed tests used the intended parcel mix and the deployed model versions.
