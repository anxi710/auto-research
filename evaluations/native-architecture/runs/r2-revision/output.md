Neither model currently qualifies for full automatic service. Alpha fails quality despite passing latency. Beta passes quality, but its latency remains unknown. Measure Beta’s complete-path latency next to resolve its only missing gate.

The [case](../../frozen/case.md) requires both gates. A lower confidence bound is the conservative end of an uncertainty interval. Required bounds are 0.95 for ordinary parcels and 0.90 for damaged parcels. A p95 is a value that at least 95% of observations do not exceed. The latency limit is an end-to-end p95 of 500 ms at 100 parcels per minute.

The [quality assessment](../r2-quality/output.md) reports Alpha’s ordinary and damaged bounds as 0.982 and 0.826. Alpha passes ordinary quality but fails damaged quality. Beta’s bounds, 0.969 and 0.930, pass both thresholds. These reported bounds need no recalculation.

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms."

Alpha’s pooled accuracy is correct, but it hides the damaged-parcel failure. Its 98.18% exceeds Beta’s 98.00%, yet Beta alone passes quality. The [operations assessment](../r2-operations/output.md) supports Alpha’s measured end-to-end p95 of 480 ms at the target load on one fixed server. Retain that latency pass and reject the claim of full-service readiness.

Beta’s model-stage p95 is 400 ms, and its queue-stage p95 is 80 ms. Separate logs provide no paired timings for individual parcels. Their unknown delay dependency prevents treating 480 ms as the end-to-end p95. Beta’s older 430 ms end-to-end result at 40 parcels per minute does not establish performance at the required load. Its latency gate remains unresolved, not failed.

Alpha costs $0.001 per parcel and Beta costs $0.002. Cost decides only after both gates pass. If both eventually qualify, the stated cost rule favors Alpha.

The [delegated AI feedback](../r2-feedback/output.md), version r2-feedback-v1, clarified support and next-test outcomes. It did not change the decision. Its hypothetical delay example illustrates uncertainty and adds no measurement evidence.

Measure Beta’s complete-path latency at 100 parcels per minute on the fixed server with the assessed model version and intended parcel mix. Record each parcel’s queue and model delays. If end-to-end p95 is at most 500 ms, Beta qualifies under this synthetic policy. If it exceeds 500 ms, neither model qualifies. Unchanged Beta needs no new quality test under these inputs. Alpha needs a targeted quality correction and evidence for both parcel groups before reconsideration.

All five listed inputs were read in full. Original branch evidence was not inspected. The [earlier memo](../r2-synthesis/output.md), version r2-synthesis-v1, remains unchanged. This revision is r2-revision-v1. The proposed measurement remains unrun. These invented inputs establish no real deployment result. Human review of this memo and proposed measurement remains pending. Delegated AI feedback is not human peer review or scientific approval.
