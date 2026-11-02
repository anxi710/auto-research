# Operations evidence

All values below are synthetic test inputs.
The target load is 100 parcels per minute on one fixed server.

Alpha has a measured end-to-end p95 of 480 ms at the target load.
Alpha costs $0.001 per parcel.

Beta has a model-stage p95 of 400 ms at the target load.
Beta has a queue-stage p95 of 80 ms at the target load.
These summaries came from separate logs. They contain no paired per-parcel timings.
The evidence gives no dependency between the two stage delays.
Beta has no measured end-to-end p95 at the target load.
Beta costs $0.002 per parcel.

An older Beta end-to-end test gives a p95 of 430 ms at 40 parcels per minute.
That test does not establish latency at the target load.
