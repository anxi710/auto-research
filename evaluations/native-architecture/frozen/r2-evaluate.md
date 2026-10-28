You are one native actor in a fixed synthetic toolkit evaluation.
The user selected gpt-6-astra with ultra reasoning. Fast-tier control is unavailable.
Read AGENTS.md and the research workflow skill as required by this repository.
This task is authorized synthetic behavior verification, including delegated AI feedback and revision.
It does not approve a scientific claim or represent human peer review.
Do not spawn agents, browse, use paid APIs, or change any other file.
Read /tmp/auto-research-writing-skills/simple-english/SKILL.md.
Read /tmp/auto-research-writing-skills/ponytail/SKILL.md.
Read /tmp/auto-research-writing-skills/stop-that-shit/SKILL.md.
Use their writing guidance. Preserve exact quoted claims.
Keep your answer within 500 words, except the evaluator JSON.
Use only the listed task evidence. Other runs and the rubric are hidden from actors.
Write your complete answer to evaluations/native-architecture/runs/r2-evaluate/output.md.
Return only that output path in your final message.

Task files below use evaluations/native-architecture/ as their root unless stated otherwise.
Read frozen/case.md, frozen/quality.md, frozen/operations.md, and frozen/rubric.json.
Evaluate these anonymous candidate files independently:
A: runs/r2-candidate-a.md
B: runs/r2-candidate-b.md
C: runs/r2-candidate-c.md
Apply the frozen rubric without assuming any architecture is better.
Do not inspect call metadata, other runs, or candidate provenance.
Output JSON only. Use this shape:
{"candidates": {"A": {"scores": {"evidence_accuracy": 0, "support": 0, "cross_branch_inference": 0, "coverage": 0}, "evidence": {"evidence_accuracy": [], "support": [], "cross_branch_inference": [], "coverage": []}, "errors": [], "uncertainties": []}, "B": {}, "C": {}}, "limits": []}
Use the same full object shape for B and C.
Score content only. The literal presence of a correct fact earns the same point in any candidate.
The absence of an explicit cross-branch decision does not earn an inference point.
