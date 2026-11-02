# Quality worker

Beta passes the quality gate. Alpha fails because its damaged-parcel lower bound is below 0.90. This quality assessment does not establish full-service eligibility for Beta. The inputs are synthetic and provide no evidence about a real inspection system.

The [case](../../frozen/case.md) requires a lower confidence bound of at least 0.95 for ordinary parcels and 0.90 for damaged parcels. A lower confidence bound is the conservative end of an uncertainty interval. The policy applies separately to each parcel type.

The [quality table](../../frozen/quality.md) reports 95% Wilson lower bounds. Alpha classifies 990/1000 ordinary parcels correctly, with a bound of 0.982, so it passes that requirement. Alpha classifies 90/100 damaged parcels correctly, with a bound of 0.826, so it fails that requirement. Its damaged-parcel accuracy of 90% does not meet a requirement for a lower bound of 90%.

Beta classifies 980/1000 ordinary parcels correctly, with a bound of 0.969, and 98/100 damaged parcels correctly, with a bound of 0.930. Both bounds exceed their respective thresholds. The fixed tests use the intended parcel mix and deployed model versions, so those conditions do not require another quality test for this assessment.

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms."

Alpha's pooled accuracy is correctly reported as 1080/1100, or 98.18%. Beta's pooled accuracy is 1078/1100, or 98.00%. Pooling hides Alpha's damaged-parcel failure and cannot establish compliance with either separate requirement. The inherited claim's full-service conclusion is therefore unsupported. Its 480 ms figure remains an unverified draft assertion within this branch.

Full service also requires an end-to-end p95 of at most 500 ms at 100 parcels per minute. A p95 is a value that at least 95% of observations do not exceed. This branch contains no operational measurements or cost evidence. Beta's full-service eligibility remains unresolved, and cost cannot decide between models before both gates pass.

The next evidence needed for Beta is its end-to-end p95 at the required throughput. Consult the operations branch before requesting a new measurement. If that evidence is absent, measure that value. For Alpha, any proposed repair needs fresh quality evidence, especially a damaged-parcel lower bound of at least 0.90. No repair or new test ran here.

This is AI assessment for the authorized synthetic evaluation. Human approval of deployment or scientific claims is not established.


# Operations worker

Alpha meets the latency gate. Beta’s latency qualification remains unknown. This operations branch cannot establish full-service eligibility for either model without the quality evidence.

The latency gate requires an end-to-end p95 of at most 500 ms at 100 parcels per minute. A p95 is a value that at least 95% of observations do not exceed. Alpha’s measured end-to-end p95 is 480 ms at that load on the fixed server, so it passes this gate by 20 ms. [Operations evidence](../../frozen/operations.md)

Beta’s model-stage p95 is 400 ms and its queue-stage p95 is 80 ms at the target load. These separate logs contain no paired per-parcel timings or evidence about dependence between delays. Adding these percentiles does not establish an end-to-end p95 of 480 ms. Beta’s older end-to-end p95 of 430 ms at 40 parcels per minute does not establish performance at 100 parcels per minute. Its target-load latency gate remains unproven, rather than a demonstrated failure. [Operations evidence](../../frozen/operations.md)

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms." The latency portion is supported, but the readiness conclusion is not established by this branch. Full service also requires quality lower confidence bounds of at least 0.95 for ordinary parcels and 0.90 for damaged parcels. A lower confidence bound is the conservative end of an uncertainty interval. Pooled accuracy alone cannot establish these separate requirements. [Case rules and inherited claim](../../frozen/case.md)

Alpha costs $0.001 per parcel and Beta costs $0.002 per parcel. Beta costs twice as much. Cost decides between models only after both gates pass, so Alpha’s lower cost does not establish a deployment choice. [Operations evidence](../../frozen/operations.md) [Cost rule](../../frozen/case.md)

The smallest useful next operations measurement is Beta’s end-to-end per-parcel timing at 100 parcels per minute on the same fixed server. Calculate its end-to-end p95 directly and compare it with 500 ms. No new test ran. Quality evidence remains outside this branch.

This is output revision r1-operations-v1. Both evidence files were read in full. All numbers are synthetic inputs, not observations from a real inspection system. The assigned task authorizes this AI assessment and delegated feedback within the evaluation. Human scientific review remains pending, and this memo grants no deployment approval.
