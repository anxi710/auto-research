# Summation order practice brief

This is a synthetic computational exercise for the research workflow.
The user approved its topic, files, and budget through W013 on 2026-10-23.
The example uses research-workflow version `0.1.6` from `../../skills/research-workflow/`.
It demonstrates saved evidence and separate review without claiming original research or a collaboration advantage.

## Goal and approved limits

Question: How does input order affect summation error on two fixed datasets?
Compare a plain accumulation loop with `math.fsum` using an exact reference for the actual binary inputs.
Success means traceable execution and accurate reporting, including ties, failures, and limits.
It does not require either method to win.

The budget allows one candidate within 60 minutes of starting the approved round.
It allows one measured run and one independent replay, each with a 30-second timeout.
One repair cycle can repeat those two runs, while preserving failed attempts.
Use the installed local Python and its standard library.
Use no GPU, paid API, external account, dataset download, or new dependency.
Assistant token and cost measurements are unavailable and remain unknown.

The coordinator owns shared state and contracts.
The execution worker owns the attempt outputs.
The named independent AI reviewer owns its review and the final task acceptance decision.
Separate reviews do not imply separate harnesses or human review.
The approved work ends after the example and required toolkit checks finish.
P2 recovery experiments and P3 strategy comparisons need separate approval.

## Evidence and conventions

The two datasets are synthetic and fixed in the experiment plan.
The sources are official API documentation, not research papers.
The [source record](LITERATURE.md) states the exact sections read.
The [question](questions/Q001.md) and [plan](experiments/E001.md) define the comparison before execution.
Paths in JSON records are relative to this example directory.
Markdown links are relative to their containing files.
Use plain English for this distributed toolkit example.
