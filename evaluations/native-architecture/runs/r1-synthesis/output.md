Neither model currently qualifies for full automatic service. Alpha fails the quality gate despite passing latency. Beta passes quality, but its latency qualification remains unknown. The next action is to measure Beta's end-to-end latency at 100 parcels per minute.

The [case](../../frozen/case.md) requires both gates to pass. A lower confidence bound is the conservative end of an uncertainty interval. The quality thresholds are 0.95 for ordinary parcels and 0.90 for damaged parcels. A p95 is a value that at least 95% of observations do not exceed. The latency threshold is an end-to-end p95 of 500 ms at 100 parcels per minute.

The [quality branch](../r1-quality/output.md) reports Alpha's ordinary-parcel lower bound as 0.982, which passes. Its damaged-parcel lower bound is 0.826, which fails. Beta's corresponding bounds are 0.969 and 0.930, so both pass. These tests use the intended parcel mix and deployed model versions. Alpha's pooled accuracy of 98.18% exceeds Beta's 98.00%, but pooling hides Alpha's damaged-parcel failure. Pooled accuracy cannot replace either separate quality requirement.

The [operations branch](../r1-operations/output.md) reports Alpha's end-to-end p95 as 480 ms at the required load on the fixed server. This establishes its latency pass and resolves the quality branch's uncertainty about that figure. The quality branch establishes Beta's quality pass, which the operations branch could not assess alone. These branch limits are complementary, not contradictory.

Beta's model-stage p95 is 400 ms and its queue-stage p95 is 80 ms. Adding these percentiles does not establish an end-to-end p95 of 480 ms. The logs lack paired parcel timings and evidence about dependence between delays. Beta's older end-to-end p95 of 430 ms at 40 parcels per minute does not establish performance at the required load. Its latency status is unknown, not a demonstrated failure. [Operations branch](../r1-operations/output.md)

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms." Both reported numbers are supported within this synthetic case. The readiness conclusion is false under the stated gates because Alpha fails damaged-parcel quality.

Alpha costs $0.001 per parcel and Beta costs $0.002. Cost cannot override either gate, so Alpha's lower cost does not justify service. [Operations branch](../r1-operations/output.md)

Measure Beta's complete per-parcel elapsed time at 100 parcels per minute on the same fixed server. Calculate its end-to-end p95 directly. A result at or below 500 ms completes Beta's eligibility evidence under the case rules. Alpha needs improved damaged-parcel quality and fresh evidence before reconsideration.

Revision r1-synthesis-v1 uses the case and both worker outputs, read in full. Source branch evidence was not inspected. No new measurement ran. All numbers are synthetic. This authorized AI synthesis grants no deployment approval or human scientific endorsement. Human review remains pending.
