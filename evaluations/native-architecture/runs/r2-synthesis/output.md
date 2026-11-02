Neither model currently qualifies for full automatic service. Alpha fails the quality gate despite passing latency. Beta passes quality, but its latency status remains unknown. Measure Beta’s complete-path latency next because this resolves its only missing gate.

The [case](../../frozen/case.md) requires both gates. A lower confidence bound is the conservative end of an uncertainty interval. The required bounds are 0.95 for ordinary parcels and 0.90 for damaged parcels. A p95 is a value that at least 95% of observations do not exceed. The latency limit is an end-to-end p95 of 500 ms at 100 parcels per minute.

The [quality assessment](../r2-quality/output.md) reports Alpha’s lower bounds as 0.982 for ordinary parcels and 0.826 for damaged parcels. Alpha passes ordinary quality but fails damaged quality. Beta’s corresponding bounds, 0.969 and 0.930, pass both thresholds. These reported bounds need no recalculation.

The [operations assessment](../r2-operations/output.md) reports Alpha’s measured end-to-end p95 as 480 ms at the target load on one fixed server. This establishes its latency pass. Beta’s model-stage p95 is 400 ms, and its queue-stage p95 is 80 ms. These values come from separate logs without paired timings for individual parcels. Their unknown delay dependency prevents treating their sum, 480 ms, as the end-to-end p95. Beta’s older end-to-end result of 430 ms at 40 parcels per minute does not establish performance at the required load. Beta therefore has an unresolved latency gate, not a demonstrated failure.

The inherited claim states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms."

Alpha’s pooled accuracy is correct, but pooling hides its damaged-parcel failure. Alpha’s 98.18% exceeds Beta’s 98.00%, yet Beta alone passes quality. The quality branch leaves the quoted latency unverified within its scope. The operations branch supplies that evidence, so the correction retains Alpha’s latency pass and rejects its full-service readiness.

Alpha costs $0.001 per parcel, while Beta costs $0.002. Cost cannot override either gate. If both models eventually pass both gates, the stated cost rule favors Alpha.

The smallest useful next measurement is Beta’s end-to-end latency at 100 parcels per minute on the fixed server with the assessed model version. Record each parcel’s complete path, including queue and model delays, then compare its p95 with 500 ms. A pass completes Beta’s eligibility evidence. Alpha instead needs a targeted quality correction and new evidence for both parcel groups before reconsideration. These actions are proposed, not executed.

This memo uses only the synthetic case and the two worker outputs, read in full. Original branch evidence was not inspected. These invented inputs establish no real deployment result. Output version: r2-synthesis-v1. Human review remains pending for this decision and proposed measurement. This is AI assessment, not human peer review or scientific approval.
