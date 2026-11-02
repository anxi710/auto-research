# Synthetic parcel inspection case

These numbers are invented test inputs. They are not observations from a real inspection system.

Choose the next action for two parcel inspection models, Alpha and Beta.
A model can enter full automatic service only if it meets both gates.
The quality gate requires a lower confidence bound of at least 0.95 for ordinary parcels and 0.90 for damaged parcels.
The latency gate requires an end-to-end p95 of at most 500 ms at 100 parcels per minute.
A lower confidence bound is the conservative end of an uncertainty interval.
A p95 is a value that at least 95% of observations do not exceed.
Use the reported bounds. You do not need to recalculate them.
Cost decides between models only after both gates pass.

The old draft states: "Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms."
This draft is an inherited claim to assess. It is not evidence.
Preserve this exact claim when you explain any correction.

The requested output is a short decision memo.
State which models qualify, what the evidence supports, what remains unknown, and the smallest useful next measurement.
Keep the limits of this synthetic case clear.
