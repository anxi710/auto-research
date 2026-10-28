Alpha meets the latency gate. Beta’s latency qualification remains unknown. This operations branch cannot establish full-service eligibility for either model without the quality evidence.

The latency gate requires an end-to-end p95 of at most 500 ms at 100 parcels per minute. A p95 is a value that at least 95% of observations do not exceed. Alpha’s measured end-to-end p95 is 480 ms at that load on the fixed server, so it passes this gate by 20 ms. [Operations evidence](../../frozen/operations.md)

Beta’s model-stage p95 is 400 ms and its queue-stage p95 is 80 ms at the target load. These separate logs contain no paired per-parcel timings or evidence about dependence between delays. Adding these percentiles does not establish an end-to-end p95 of 480 ms. Beta’s older end-to-end p95 of 430 ms at 40 parcels per minute does not establish performance at 100 parcels per minute. Its target-load latency gate remains unproven, rather than a demonstrated failure. [Operations evidence](../../frozen/operations.md)

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms." The latency portion is supported, but the readiness conclusion is not established by this branch. Full service also requires quality lower confidence bounds of at least 0.95 for ordinary parcels and 0.90 for damaged parcels. A lower confidence bound is the conservative end of an uncertainty interval. Pooled accuracy alone cannot establish these separate requirements. [Case rules and inherited claim](../../frozen/case.md)

Alpha costs $0.001 per parcel and Beta costs $0.002 per parcel. Beta costs twice as much. Cost decides between models only after both gates pass, so Alpha’s lower cost does not establish a deployment choice. [Operations evidence](../../frozen/operations.md) [Cost rule](../../frozen/case.md)

The smallest useful next operations measurement is Beta’s end-to-end per-parcel timing at 100 parcels per minute on the same fixed server. Calculate its end-to-end p95 directly and compare it with 500 ms. No new test ran. Quality evidence remains outside this branch.

This is output revision r1-operations-v1. Both evidence files were read in full. All numbers are synthetic inputs, not observations from a real inspection system. The assigned task authorizes this AI assessment and delegated feedback within the evaluation. Human scientific review remains pending, and this memo grants no deployment approval.
