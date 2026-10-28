# Native architecture comparison

This directory holds one small test of three agent workflows.
Read the [completed report](REPORT.md) for the observed results and limits.
The task uses invented parcel inspection data.
Native agents produce the answers.
The Python runner records calls and file digests. It never creates model answers.

The frozen plan names one heldout case and two repeats.
The case was not part of the worked fixture used to build the toolkit change.
The plan, evidence, prompts, and scoring rules were fixed before the first actor ran.
Do not change those files after reading an actor result.
`freeze.json` records their SHA256 digests.
A SHA256 digest identifies the exact bytes of a file.

The three arms use the same task and model request.
The single-agent arm gets both evidence branches and an optional reasoning aid.
The merge arm joins two independent worker responses without a new inference.
The synthesis arm uses those same responses, then adds synthesis, delegated AI feedback, and revision.
The earlier memo stays unchanged.
The feedback is an AI assessment. It is not a human review.

The worker outputs are shared between the two multi-agent arms.
Both arms pay the full recorded worker count and time in the resource summary.
This pairing holds worker content fixed when the merge method changes.
It does not compare independent runs of complete multi-agent systems.
The arms also use different call counts, so this is not an equal-compute comparison.

Every actor runs in a fresh native context.
All calls run in sequence with the same role order for each repeat.
The requested model is `gpt-6-astra` with `ultra` reasoning.
The native tool has no Fast-tier control or actual model receipt.
The record therefore leaves actual model, tier, tokens, and cost unknown.
The two pre-existing coordinator contexts also have unknown token and cost use.
Their model receipts and preparation time before the freeze were not captured.

The rubric scores evidence accuracy, support, combined inference, and coverage separately.
It gives no points for formatting or polish.
A fixed oracle rejects the old pooled-accuracy claim.
It also distinguishes a known quality failure from missing latency evidence.
The old wrong claim stays beside its correction.

From the repository root, make sure that the frozen files still match:

```bash
python evaluations/native-architecture/run.py verify
```

For a new authorized replication, use a separate copy of this repository.
Keep this recorded run unchanged.
In the copy, preserve the frozen files and create an empty `runs/` directory.
Remove the copied `freeze.json`, then run `run.py freeze` to record the new start.
Keep the same repository-relative paths used by the prompts.
The writing skill files named in each prompt must exist with the hashes in `context-before.json`.
Record the local context and model controls before dispatch.
Use the native `collaboration.spawn_agent` tool with `fork_turns="none"`, `model="gpt-6-astra"`, and `reasoning_effort="ultra"`.
Use the saved dispatch message from `dispatch-messages.json`.
Change only its workspace path to the separate repository copy, and save that changed message.
Keep each task prompt unchanged.
The Python runner cannot invoke this tool itself.
The procedure needs the native collaboration tools and the external writing skill files.

For each planned call, record its start before native dispatch.
After the tool accepts the dispatch, record its native ID.
After the native agent ends, record its outcome:

```bash
python evaluations/native-architecture/run.py start --call r1-single
python evaluations/native-architecture/run.py dispatched --call r1-single --agent-id NATIVE_AGENT_ID
python evaluations/native-architecture/run.py finish --call r1-single --agent-id NATIVE_AGENT_ID
python evaluations/native-architecture/run.py summary
```

After each revision, create the literal merge and masked candidate copies before the evaluator runs:

```bash
python evaluations/native-architecture/run.py package --repeat 1
```

The package command preserves each worker response byte for byte.
It adds only branch headings to the literal merge.
Candidate labels hide names, but answer structure can still reveal the method.

A repeated run can produce a different answer.
The saved prompts make the procedure reproducible, not the generated text.
The study has one synthetic case and two repeats.
It cannot establish a general performance gain, a speed gain, a cost gain, or human review savings.
The final report records the observed outputs and their limits.

The runner test uses dummy bytes in a temporary directory.
It tests record handling only:

```bash
python -m unittest discover -s tests -p test_native_architecture_eval.py
```
