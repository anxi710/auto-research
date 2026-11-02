{
  "candidates": {
    "A": {
      "scores": {
        "evidence_accuracy": 4,
        "support": 3,
        "cross_branch_inference": 0,
        "coverage": 4
      },
      "evidence": {
        "evidence_accuracy": [
          "1/1: \"Its damaged bound, 0.826, fails the 0.90 threshold. Both parcel types must pass, so Alpha fails the overall quality gate.\"",
          "1/1: \"Its bounds are 0.969 and 0.930, respectively. Both exceed their required thresholds, so Beta passes the quality gate.\" The preceding policy gives 0.95 and 0.90 for the respective parcel types.",
          "1/1: \"Alpha passes the latency gate.\" The operations section reports \"Alpha’s measured end-to-end p95 as 480 ms at the target load on one fixed server.\"",
          "1/1: \"Beta’s older end-to-end p95 of 430 ms at 40 parcels per minute does not establish performance at 100 parcels per minute. Beta therefore has neither an established latency pass nor an established latency failure at the target load.\""
        ],
        "support": [
          "1/1: \"These pooled figures combine parcel types, but the policy applies to each type separately. Alpha's higher pooled accuracy cannot override its failed damaged-parcel bound.\"",
          "1/1: \"Although 400 + 80 = 480 ms, adding stage percentiles does not establish the end-to-end p95.\"",
          "1/1: \"Cost decides between models only after both gates pass.\" Also: \"All numbers are synthetic inputs, not real inspection observations.\" The proposed measurement is explicitly \"proposed, not executed.\" No new measurement is presented as observed."
        ],
        "cross_branch_inference": [
          "0/1: No explicit conclusion says that neither model has evidence of passing both gates. Instead: \"This branch cannot decide full-service readiness without the operations evidence.\" Also: \"This operations branch cannot establish full-service eligibility for either model without the quality evidence.\"",
          "0/1: \"Beta passes the quality gate.\" and \"The smallest useful next operations measurement is Beta’s end-to-end per-parcel latency at 100 parcels per minute on the fixed server.\" appear separately. The candidate does not explicitly select this measurement because Beta passes quality and lacks latency evidence.",
          "0/1: The candidate separately proposes \"a fixed damaged-parcel test of that revision\" for Alpha and a Beta latency measurement. It does not compare those next actions by joining Alpha's known quality failure with Beta's missing latency evidence."
        ],
        "coverage": [
          "1/1: \"Beta passes the quality gate. Alpha fails it because its damaged-parcel lower bound is below the required threshold.\"",
          "1/1: \"Alpha passes the latency gate. Beta’s latency status remains unknown.\"",
          "1/1: The exact inherited claim appears: \"Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms.\" The correction states: \"Alpha's higher pooled accuracy cannot override its failed damaged-parcel bound.\"",
          "1/1: \"This memo uses synthetic inputs only.\" Also: \"The smallest useful next operations measurement is Beta’s end-to-end per-parcel latency at 100 parcels per minute on the fixed server.\""
        ]
      },
      "errors": [
        "Missing explicit conclusion about whether either model meets both gates.",
        "Missing explicit link between Beta's quality pass and the choice of its next latency measurement.",
        "Missing explicit comparison of next actions using Alpha's known failure and Beta's missing evidence."
      ],
      "uncertainties": [
        "The separate recommendations permit a reader to infer different next actions. The rubric requires an explicit combined decision, so their coexistence earns no inference point. Branch-specific scope statements do not erase correct facts elsewhere in the candidate."
      ]
    },
    "B": {
      "scores": {
        "evidence_accuracy": 4,
        "support": 3,
        "cross_branch_inference": 3,
        "coverage": 4
      },
      "evidence": {
        "evidence_accuracy": [
          "1/1: The candidate gives \"Alpha’s ordinary and damaged bounds as 0.982 and 0.826\" and states: \"Alpha passes ordinary quality but fails damaged quality.\" It gives the thresholds as \"0.95 for ordinary parcels and 0.90 for damaged parcels.\"",
          "1/1: \"Beta’s bounds, 0.969 and 0.930, pass both thresholds.\" The stated thresholds are 0.95 and 0.90.",
          "1/1: The candidate reports \"Alpha’s measured end-to-end p95 of 480 ms at the target load on one fixed server.\" It adds: \"Retain that latency pass and reject the claim of full-service readiness.\"",
          "1/1: \"Beta’s older 430 ms end-to-end result at 40 parcels per minute does not establish performance at the required load. Its latency gate remains unresolved, not failed.\""
        ],
        "support": [
          "1/1: \"Alpha’s pooled accuracy is correct, but it hides the damaged-parcel failure. Its 98.18% exceeds Beta’s 98.00%, yet Beta alone passes quality.\" The candidate explicitly rejects full-service readiness.",
          "1/1: \"Separate logs provide no paired timings for individual parcels. Their unknown delay dependency prevents treating 480 ms as the end-to-end p95.\"",
          "1/1: \"Cost decides only after both gates pass.\" Also: \"The proposed measurement remains unrun. These invented inputs establish no real deployment result.\" No new measurement is presented as observed."
        ],
        "cross_branch_inference": [
          "1/1: \"Neither model currently qualifies for full automatic service.\"",
          "1/1: \"Beta passes quality, but its latency remains unknown. Measure Beta’s complete-path latency next to resolve its only missing gate.\" The measurement is specified later at 100 parcels per minute.",
          "1/1: \"Alpha fails quality despite passing latency. Beta passes quality, but its latency remains unknown.\" The next actions distinguish \"Unchanged Beta needs no new quality test under these inputs.\" from \"Alpha needs a targeted quality correction and evidence for both parcel groups before reconsideration.\""
        ],
        "coverage": [
          "1/1: \"Alpha passes ordinary quality but fails damaged quality. Beta’s bounds, 0.969 and 0.930, pass both thresholds.\"",
          "1/1: \"Alpha fails quality despite passing latency. Beta passes quality, but its latency remains unknown.\" The body assesses the target-load measurements for both models.",
          "1/1: The exact inherited claim appears: \"Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms.\" Its correction states: \"Alpha’s pooled accuracy is correct, but it hides the damaged-parcel failure.\" Also: \"Retain that latency pass and reject the claim of full-service readiness.\"",
          "1/1: \"These invented inputs establish no real deployment result.\" Also: \"Measure Beta’s complete-path latency at 100 parcels per minute on the fixed server with the assessed model version and intended parcel mix.\""
        ]
      },
      "errors": [],
      "uncertainties": []
    },
    "C": {
      "scores": {
        "evidence_accuracy": 4,
        "support": 3,
        "cross_branch_inference": 3,
        "coverage": 4
      },
      "evidence": {
        "evidence_accuracy": [
          "1/1: \"Alpha fails the damaged-parcel quality gate.\" Also: \"It fails damaged parcels: 0.826 is below 0.90.\"",
          "1/1: \"Beta passes both: 0.969 exceeds 0.95 for ordinary parcels, and 0.930 exceeds 0.90 for damaged parcels.\"",
          "1/1: \"Alpha passes latency with an end-to-end p95 of 480 ms at 100 parcels per minute, below the 500 ms limit.\"",
          "1/1: \"Beta has no end-to-end measurement at that load.\" Also: \"Its older 430 ms result at 40 parcels per minute does not resolve the target-load gate.\""
        ],
        "support": [
          "1/1: \"Alpha's 98.18% pooled accuracy hides its failed damaged-parcel bound. Beta's slightly lower 98.00% pooled accuracy does not overturn its passing quality bounds.\"",
          "1/1: \"Its 400 ms model-stage p95 and 80 ms queue-stage p95 cannot establish a 480 ms end-to-end p95. The separate logs provide neither paired timings nor the relationship between stage delays.\"",
          "1/1: \"Cost cannot override either gate and decides between models only after both qualify.\" Also: \"These inputs are synthetic and establish no real-world readiness.\" The candidate states: \"No new experiment ran.\" No new measurement is presented as observed."
        ],
        "cross_branch_inference": [
          "1/1: \"Neither model currently qualifies for full automatic service on the supplied evidence.\"",
          "1/1: \"Beta passes quality, but its required latency remains unknown. Measure Beta next.\" Later: \"The smallest useful next measurement is Beta's end-to-end latency at 100 parcels per minute on the fixed server.\"",
          "1/1: \"Alpha fails the damaged-parcel quality gate. Beta passes quality, but its required latency remains unknown. Measure Beta next.\" The candidate specifies the Beta measurement and adds: \"Keep Alpha out of full automatic service unless revised damaged-parcel evidence meets the quality gate.\""
        ],
        "coverage": [
          "1/1: \"Alpha passes ordinary parcels: 0.982 exceeds 0.95. It fails damaged parcels: 0.826 is below 0.90. Beta passes both: 0.969 exceeds 0.95 for ordinary parcels, and 0.930 exceeds 0.90 for damaged parcels.\"",
          "1/1: \"Alpha passes latency with an end-to-end p95 of 480 ms at 100 parcels per minute, below the 500 ms limit. Beta has no end-to-end measurement at that load.\"",
          "1/1: The exact inherited claim appears: \"Alpha is ready for full service because its pooled accuracy is 98.18% and its p95 is 480 ms.\" Its correction states: \"The latency result supports only the latency gate. Alpha's 98.18% pooled accuracy hides its failed damaged-parcel bound.\"",
          "1/1: \"These inputs are synthetic and establish no real-world readiness.\" Also: \"The smallest useful next measurement is Beta's end-to-end latency at 100 parcels per minute on the fixed server.\""
        ]
      },
      "errors": [],
      "uncertainties": [
        "The statement that two 95% stage bounds guarantee only 90% jointly is read as a worst-case lower guarantee for a common workload. It is not an observed joint rate or a claim that the separate logs establish that workload. This interpretation does not change any rubric point."
      ]
    }
  },
  "limits": [
    "Each candidate was scored independently against frozen/rubric.json using frozen/case.md, frozen/quality.md, and frozen/operations.md. Evidence quotations come from that candidate's listed file.",
    "All rubric facts receive equal credit wherever they appear. Scores do not reward format, length, headings, schema, or inferred architecture. Unstated cross-branch conclusions receive no inference credit.",
    "Candidate links and statements about earlier reading or feedback were not independently inspected. They provide no additional scoring evidence.",
    "This output is r2-evaluate-v1, an AI evaluation of synthetic inputs. Human review remains pending. It provides neither scientific approval nor evidence about real inspection systems."
  ]
}
