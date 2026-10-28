Beta passes the quality gate. Alpha fails it because its damaged-parcel lower bound is below the required threshold. These findings establish quality status only. This branch cannot decide full-service readiness without the operations evidence.

A lower confidence bound is the conservative end of an uncertainty interval. The [case](../../frozen/case.md) requires bounds of at least 0.95 for ordinary parcels and 0.90 for damaged parcels. The [quality table](../../frozen/quality.md) reports 95% Wilson lower bounds, which this assessment uses without recalculation.

Alpha correctly classifies 990 of 1,000 ordinary parcels. Its ordinary bound, 0.982, passes the 0.95 threshold. Alpha correctly classifies 90 of 100 damaged parcels. Its damaged bound, 0.826, fails the 0.90 threshold. Both parcel types must pass, so Alpha fails the overall quality gate.

Beta correctly classifies 980 of 1,000 ordinary parcels and 98 of 100 damaged parcels. Its bounds are 0.969 and 0.930, respectively. Both exceed their required thresholds, so Beta passes the quality gate.

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms."

Alpha's pooled accuracy is correctly reported as 1,080/1,100, or 98.18%. Beta's pooled accuracy is 1,078/1,100, or 98.00%. These pooled figures combine parcel types, but the policy applies to each type separately. Alpha's higher pooled accuracy cannot override its failed damaged-parcel bound. The quality evidence therefore contradicts the claim of full-service readiness.

The quoted 480 ms is part of the inherited claim, not verified latency evidence. A p95 is a value that at least 95% of observations do not exceed. Full service also requires end-to-end p95 at most 500 ms at 100 parcels per minute. Neither model's latency status is established in this branch. Cost can decide between models only after both gates pass. [Source: case](../../frozen/case.md).

No new quality measurement is needed to classify the current versions. If Alpha remains under consideration, inspect its ten damaged-parcel errors before choosing a targeted correction. The smallest useful follow-up quality measurement is a fixed damaged-parcel test of that revision against the 0.90 bound requirement. Any revised version also needs ordinary-parcel evidence against 0.95. This proposed work has not run.

The supplied fixed tests used the intended parcel mix and deployed model versions. All numbers are synthetic inputs, not real inspection observations. This is AI assessment, not human peer review or scientific approval. Output version: r2-quality v1. Human review remains pending. Operations evidence and other worker outputs were outside this review's scope, so Beta's full-service eligibility remains unresolved.
