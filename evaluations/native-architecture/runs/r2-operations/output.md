Alpha passes the latency gate. Beta’s latency status remains unknown. This operations branch cannot establish full-service eligibility for either model without the quality evidence.

The [case](../../frozen/case.md) requires an end-to-end p95 of at most 500 ms at 100 parcels per minute. A p95 is a value that at least 95% of observations do not exceed. Full automatic service also requires quality lower confidence bounds of at least 0.95 for ordinary parcels and 0.90 for damaged parcels. A lower confidence bound is the conservative end of an uncertainty interval. Cost decides between models only after both gates pass.

The [operations evidence](../../frozen/operations.md) reports Alpha’s measured end-to-end p95 as 480 ms at the target load on one fixed server. This is 20 ms below the limit. Alpha costs $0.001 per parcel.

Beta’s model-stage p95 is 400 ms, and its queue-stage p95 is 80 ms at the target load. These summaries come from separate logs without paired per-parcel timings. Their delay dependency is unknown. Although 400 + 80 = 480 ms, adding stage percentiles does not establish the end-to-end p95. Beta’s older end-to-end p95 of 430 ms at 40 parcels per minute does not establish performance at 100 parcels per minute. Beta therefore has neither an established latency pass nor an established latency failure at the target load.

Beta costs $0.002 per parcel, twice Alpha’s cost. If both models pass both gates, the cost rule favors Alpha. Lower cost cannot replace either gate.

The inherited draft states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms."

This claim is not evidence. The operations evidence supports Alpha’s latency pass, but pooled accuracy does not establish the required quality bounds for each parcel group. The supported correction is that Alpha passes latency, while full-service readiness requires the separate quality assessment.

The smallest useful next operations measurement is Beta’s end-to-end per-parcel latency at 100 parcels per minute on the fixed server. Measure the complete path, including queue and model delays, and report its p95 against 500 ms. This measurement is proposed, not executed.

This memo uses synthetic inputs only. I did not inspect quality evidence or select a deployment. The output version is r2-operations-v1. Human review remains pending, and this AI assessment is not scientific approval.
