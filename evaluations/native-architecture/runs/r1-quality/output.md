Beta passes the quality gate. Alpha fails because its damaged-parcel lower bound is below 0.90. This quality assessment does not establish full-service eligibility for Beta. The inputs are synthetic and provide no evidence about a real inspection system.

The [case](../../frozen/case.md) requires a lower confidence bound of at least 0.95 for ordinary parcels and 0.90 for damaged parcels. A lower confidence bound is the conservative end of an uncertainty interval. The policy applies separately to each parcel type.

The [quality table](../../frozen/quality.md) reports 95% Wilson lower bounds. Alpha classifies 990/1000 ordinary parcels correctly, with a bound of 0.982, so it passes that requirement. Alpha classifies 90/100 damaged parcels correctly, with a bound of 0.826, so it fails that requirement. Its damaged-parcel accuracy of 90% does not meet a requirement for a lower bound of 90%.

Beta classifies 980/1000 ordinary parcels correctly, with a bound of 0.969, and 98/100 damaged parcels correctly, with a bound of 0.930. Both bounds exceed their respective thresholds. The fixed tests use the intended parcel mix and deployed model versions, so those conditions do not require another quality test for this assessment.

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms."

Alpha's pooled accuracy is correctly reported as 1080/1100, or 98.18%. Beta's pooled accuracy is 1078/1100, or 98.00%. Pooling hides Alpha's damaged-parcel failure and cannot establish compliance with either separate requirement. The inherited claim's full-service conclusion is therefore unsupported. Its 480 ms figure remains an unverified draft assertion within this branch.

Full service also requires an end-to-end p95 of at most 500 ms at 100 parcels per minute. A p95 is a value that at least 95% of observations do not exceed. This branch contains no operational measurements or cost evidence. Beta's full-service eligibility remains unresolved, and cost cannot decide between models before both gates pass.

The next evidence needed for Beta is its end-to-end p95 at the required throughput. Consult the operations branch before requesting a new measurement. If that evidence is absent, measure that value. For Alpha, any proposed repair needs fresh quality evidence, especially a damaged-parcel lower bound of at least 0.90. No repair or new test ran here.

This is AI assessment for the authorized synthetic evaluation. Human approval of deployment or scientific claims is not established.
