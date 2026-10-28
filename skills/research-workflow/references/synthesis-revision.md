# Synthesize fixed branch evidence

A synthesis explains what several sources support together.
A literal aggregate preserves worker responses without adding a joint conclusion.
Use [response collection](response-collection.md) when a task needs these distinct artifacts.
Keep scientific support judgments in the existing [evidence review](evidence-ledger.md#assess-support-in-the-existing-review).
Keep permission in the existing [human review records](human-review.md).

## Build the joint answer

Read the fixed aggregate and its coverage before drawing a conclusion.
Treat a missing, unfinished, invalid, or stale branch as a limit on the answer.
Read the original evidence when a worker summary cannot support the needed inference.

1. State the question and the conclusion that the available evidence supports.
2. Connect each conclusion to source locations and the conditions needed for the inference.
3. Distinguish compatible partial answers from conflicting findings under comparable conditions.
4. Explain condition differences and superseded sources before combining their findings.
5. State a supported alternative explanation and the observation needed to distinguish it.
6. Leave unresolved questions explicit when the evidence is insufficient.

Use the optional [research-report skill](../../research-report/SKILL.md) for the reader's argument and reading path.
Its summary and full account must preserve the same conditions and uncertainty.
Do not infer a cross-branch conclusion from the presence of two separate paragraphs.

## Evaluate the content

Freeze the materials, task questions, and criteria before comparing candidates.
Keep literal collection and wording-only revision as controls when testing added reasoning.
Give each control credit for the correct content that it actually contains.

| Dimension | What the reviewer assesses |
| --- | --- |
| Source quality | Version, access, reading depth, applicable methods, and limits of the source. |
| Claim support | Whether the cited evidence supports the stated strength and conditions. |
| Cross-branch reasoning | Whether the conclusion uses the required premises from distinct branches. |
| Question coverage | Which requested questions have supported answers or explicit evidence gaps. |

Do not combine these dimensions into a formatting score.
The [fixed-material checker](../scripts/synthesis_eval.py) compares declared findings with selected evidence relations.
Its matching fields do not establish that the prose is correct.
An independent reader must inspect the actual conclusion, alternative, and boundary statements.
The [W022 cases](../../../tests/synthesis) provide bounded examples, not a general scientific evaluator.

## Revise the affected argument

A dependency closure includes every output that uses a changed premise.
Freeze the initial draft, evidence versions, feedback, and criteria before revision.
Keep the feedback's actual source visible, including synthetic or delegated AI feedback.
Use the existing human-review boundary before dependent research.

1. Locate each requested scientific correction and the claim that it changes.
2. Save the affected dependency closure before drafting replacements.
3. Include other branches, recommendations, summaries, and ledger claims that use the changed premise.
4. Write revisions in a new attempt and reuse unaffected original files by reference.
5. Assess feedback implementation separately from damage to previously correct content.
6. Make sure that citations support the revised strength, conditions, and source versions.
7. Mark unrevised dependent conclusions as stale and keep the earlier revision available.

The [revision helper](../scripts/revision_loop.py) replays supplied replacements for frozen examples.
It computes the affected closure before writing the new attempt.
It checks selected findings, preserved statements, file history, and existing ledger bindings separately.
It does not generate replacement prose or decide scientific support.
Changed bytes alone do not prove that feedback was implemented.
An unchanged selected statement alone does not prove that the full draft survived.

Run a replay in a temporary copy from the toolkit root:

```sh
revision_dir=$(mktemp -d)
cp -R tests/revision/. "$revision_dir/"
python3 -B skills/research-workflow/scripts/revision_loop.py \
  --root "$revision_dir" --case synthetic/case.json \
  --candidate synthetic/full.json --output attempts/A002
```

The `local-only.json` control revises A while leaving B and the report stale.
Use a different output directory to inspect that blocked result.
The `public-source` case uses selected passages from Mr Dre v1.
Both examples are fixed correction exercises and do not measure human reviewer effort.
