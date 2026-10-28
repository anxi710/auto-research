# Native comparison on one heldout case

The strong single agent and the synthesis workflow tied in both repeats.
The literal merge kept the correct evidence but did not state the combined eligibility decision.
This case provides no evidence that multiple agents outperform the strong single agent.

| Repeat | Arm | Evidence accuracy / 4 | Support / 3 | Combined inference / 3 | Coverage / 4 |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | Single with on-demand skills | 4 | 3 | 3 | 4 |
| 1 | Independent workers, literal merge | 4 | 3 | 2 | 4 |
| 1 | Shared workers, synthesis, feedback, revision | 4 | 3 | 3 | 4 |
| 2 | Single with on-demand skills | 4 | 3 | 3 | 4 |
| 2 | Independent workers, literal merge | 4 | 3 | 0 | 4 |
| 2 | Shared workers, synthesis, feedback, revision | 4 | 3 | 3 | 4 |

The [rubric](frozen/rubric.json) gave no points for format or polish.
Two native AI evaluators scored the outputs, one per repeat.
Their [first](runs/r1-evaluate/output.md) and [second](runs/r2-evaluate/output.md) reports preserve evidence quotes and uncertainty.
The [score file](scores.json) keeps the full dimensions, errors, and uncertainties.

The first merge earned two inference points for explicit conditional next steps within the quality branch.
The first evaluator marked one of those credits as less explicit than the other candidates.
The second merge left those connections to its reader and earned no inference points.
The second evaluator also recorded its interpretation of the single agent's conditional 90% bound.
These judgments and changed worker text both affect the observed variation.
Two repeats do not separate those effects or establish statistical significance.

The [plan](frozen/plan.json), case, evidence, prompts, and rubric were fixed before any actor ran.
The [freeze record](freeze.json) binds their exact bytes.
The parcel data are invented test inputs, separate from the toolkit's worked fixture.
They did not guide later prompt or rubric changes.
The native outputs are observed model behavior on those synthetic inputs.
They are not real inspection results or evidence for a scientific hypothesis.

Each actor used a fresh native context.
All study calls ran sequentially in the same role order for each repeat.
Parallel scheduling was not run.
The single arm received both evidence branches and access to an on-demand reasoning aid and reporting skill.
The two multi-agent arms shared the same independent worker outputs.
This pairing holds worker content fixed, but does not compare independent runs of complete systems or equal-compute budgets.

The study completed 14 native calls.
These comprise two single agents, four workers, two synthesis agents, two AI critics, two revision agents, and two evaluators.
The two pre-existing coordinator contexts are also part of the work, with usage limits stated below.
The [resource record](resources.json) charges shared workers fully to both consuming arms and evaluators fully to all three arms.
Arm counts and times therefore overlap and must not be added together.

| Arm, both repeats | Charged native calls, including evaluation | Recorded call seconds |
| --- | ---: | ---: |
| Single | 4 | 482.07 |
| Literal merge | 6 | 509.89 |
| Synthesis, feedback, revision | 12 | 894.74 |

The wall time from freeze through the last observed completion was 1115.77 seconds.
The sum of unique call observation intervals was 1107.67 seconds.
These intervals run from preparation for dispatch through the coordinator's observation of completion.
They include orchestration, observation delay, and the first single agent's capacity wait.
Study wall time includes coordination and local work after the freeze.
Preparation before the freeze and allocation of coordinator time to each arm remain unknown.

Every actor request specified `gpt-6-astra` and `ultra` reasoning.
The native tool supplied no actual model receipt, token counter, or billing counter.
It offered no Fast-tier control.
Actual model, Fast tier, tokens, and cost remain `null` in the call records.
The coordinator model receipts, token use, cost, and preparation time also remain unknown.
No token estimate, cost estimate, speed gain, or complete efficiency comparison is claimed.

Both [first](runs/r1-feedback/output.md) and [second](runs/r2-feedback/output.md) AI critics found no material error in the initial synthesis.
They proposed an explicit statement of the next latency test's failure outcome.
Both revisions kept the decision and clarified its support.
The [first initial memo](runs/r1-synthesis/output.md) and [second initial memo](runs/r2-synthesis/output.md) remain unchanged beside their revisions.
The exact old pooled-accuracy claim stays visible in the outputs.
This is delegated AI feedback, not human peer review or a measured reduction in human review work.

The [duplication record](duplication.json) counts the inherited claim twice in each literal merge.
Each single and revised memo contains it once.
Both workers also reason about the shared policy from their branch scope.
The preserved text shows repeated work, but its byte count is not a token or cost estimate.

One native dispatch was [denied before execution](runs/r1-single/dispatch-failures.json) because the agent limit was reached.
The retry followed notice that a slot was free.
No actor failed or remained open at completion.
The earlier denial stays in the record and does not count as a model call.

The [before](context-before.json) and [after](context-after.json) hashes match for the prescribed entry files and writing skills.
Other repository references changed during the study, including `synthesis-revision.md` and W022 evidence documents.
Actual file-access traces were not captured, and shared-file read restrictions were cooperative.
Full instruction-context isolation is therefore not established.
Masked labels hid candidate names, but their structure still exposed clues about the method.

The [runner checks](checks.json) passed two deterministic tests and the frozen-input inspection.
Those tests use dummy bytes and do not supply model performance evidence.
The [README](README.md) gives the native dispatch and replication procedure.
This completed toolkit test supports a narrow distinction between literal collection and an explicit final decision.
It does not support a general architecture default, parallel speed claim, or human scientific approval.
