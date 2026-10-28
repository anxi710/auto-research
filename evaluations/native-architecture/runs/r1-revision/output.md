Neither model currently qualifies for full automatic service. Alpha fails quality despite passing latency. Beta passes quality, but its latency qualification remains unknown. Measure Beta's end-to-end latency at the required load next.

The [case](../../frozen/case.md) requires both gates to pass. A lower confidence bound is the conservative end of an uncertainty interval. The quality thresholds are 0.95 for ordinary parcels and 0.90 for damaged parcels. A p95 is a value that at least 95% of observations do not exceed. The latency threshold is an end-to-end p95 of at most 500 ms at 100 parcels per minute.

The [quality report](../r1-quality/output.md) gives Alpha lower bounds of 0.982 for ordinary parcels and 0.826 for damaged parcels. Alpha passes the first requirement and fails the second. Beta's corresponding bounds are 0.969 and 0.930, so it passes both. These tests use the intended parcel mix and deployed model versions. Alpha's pooled accuracy of 98.18% cannot replace the separate quality requirements.

The [operations report](../r1-operations/output.md) establishes Alpha's end-to-end p95 of 480 ms at the required load on the fixed server. This resolves the quality report's uncertainty about that number. The quality report supplies the quality assessment absent from the operations report.

Beta's model-stage p95 of 400 ms and queue-stage p95 of 80 ms do not establish an end-to-end p95 of 480 ms. The logs lack paired parcel timings and evidence about dependence between delays. Beta's older end-to-end p95 of 430 ms at 40 parcels per minute does not establish performance at the required load. Beta's latency remains unknown, rather than a demonstrated failure. [Operations report](../r1-operations/output.md)

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms." Both numbers are supported within this synthetic case. The readiness conclusion is false because Alpha fails damaged-parcel quality.

Alpha costs $0.001 per parcel and Beta costs $0.002. Cost decides only after both gates pass, so Alpha's lower cost cannot override its quality failure. [Operations report](../r1-operations/output.md) [Case](../../frozen/case.md)

Measure Beta's complete per-parcel elapsed time at 100 parcels per minute on the same fixed server. Use the deployed version and intended parcel mix. Calculate its end-to-end p95 directly. At or below 500 ms, Beta qualifies under the case rules. Above 500 ms, neither model qualifies. Alpha needs improved damaged-parcel quality and fresh evidence before reconsideration.

The [delegated AI feedback](../r1-feedback/output.md) did not change the decision. It only clarified its support and the failed-test outcome. It is not human review. The [earlier memo](../r1-synthesis/output.md) remains unchanged.

This is revision r1-revision-v1. I read the case and four assigned outputs in full. I did not inspect underlying branch evidence. No measurement ran. All numbers are synthetic. Human review remains pending, and this memo grants no deployment approval.
