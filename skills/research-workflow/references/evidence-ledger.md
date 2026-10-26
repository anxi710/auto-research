# Link claims to fixed evidence

A claim is a statement that needs evidence.
An artifact is a saved file.
When selected claims need a machine-readable evidence trail, use a claim-evidence ledger.
This optional artifact extends the existing [collaboration records](collaboration.md).
The checker does not find every claim or judge scientific support.

The checker reads local files with Python 3.9+ and the standard library.
It does not write research files or call external services.

## Keep one authority for each decision

An attempt records one execution of a task.
Save the ledger in a new attempt, such as `tasks/T001/attempts/A001/artifacts/evidence-ledger.json`.
A sealed result fixes the submitted files and hashes.
Before you seal the result, finish the ledger and its evidence.

A raw SHA256 hash identifies the complete file bytes.
List the ledger in the result's existing `artifacts` array with its raw SHA256 and `kind: "claim_evidence_ledger"`.
This kind identifies the artifact as a ledger.
Use at most one ledger per result.
The result records the ledger path and hash like those of its other artifacts.

The research root is the directory selected for records.
If the task requires a ledger, set its `evidence_ledger` field to the ledger path relative to that root.
A completed result must then list that artifact with the ledger kind.
The checker rejects a required ledger that is missing or lacks the ledger kind.
Tasks and results that do not use this feature retain the existing format.

The checker finds ledgers through selected results, including results required by task dependencies.
These checks need no extra CLI flag.

Keep `CLAIMS.md` as the claim summary and navigation entry point.
Link its stable claim IDs to the exact ledger and review records.
Do not maintain a second final verdict in the ledger or CLAIMS.
Record scientific assessments in the existing review's task acceptance block.

Keep human decisions under the existing [human review procedure](human-review.md).
A clean structural check and an AI review do not authorize dependent research.

If claim text or evidence changes, use a new attempt.
Preserve the prior ledger, manuscript, result, and reviews.
If you revise an assessment of the same exact result, use a new review with `supersedes`.
Evidence from other attempts retains its original paths and hashes.
If you reuse evidence, state that reuse and whether a new experiment ran.

## Record claims and locations

The ledger contains `schema_version: "1"`, `task_id`, `attempt_id`, and a nonempty `claims` array.
Its task and attempt IDs must match the result.
Use only the documented fields in the ledger.
Do not add approval, status, or verdict fields to it.

Each claim contains these fields:

| Field | Meaning |
| --- | --- |
| `claim_id` | Stable ID, unique within this ledger. Preserve the ID across later attempts. |
| `text` | Exact wording of the selected claim. |
| `location` | `artifact`, raw `sha256`, and `exact_quote` for the fixed UTF-8 manuscript. |
| `evidence` | Nonempty array of evidence entries. |
| `verification_request` | `question` and a `limitations` array for the reviewer. |

The first format uses one exact rule to find a claim.
`exact_quote` must equal the claim text and occur exactly once in the manuscript.
Overlapping matches count as separate occurrences.
The checker rejects an absent or repeated quote without guessing a location.
The file hash fixes the entire manuscript version.
This rule does not interpret Markdown headings, HTML anchors, or meaning.

All artifact paths are relative to the selected research root.
Keep them inside that root, including symbolic link targets.
Do not use paths relative to the ledger's directory.
Before the checker uses source content, it compares the file hash with the recorded hash.

Each evidence entry contains `evidence_id`, `kind`, `availability`, `scope`, and `limitations`.
Evidence IDs are unique within the ledger.
Use `experiment` or `literature` for `kind`.
`scope` states the range of the evidence, not a support verdict.

## Bind an experiment to structured measurements

JSON Pointer identifies a field within a JSON document.
An experiment entry uses `availability: "available"` and includes these fields:

| Field | Meaning |
| --- | --- |
| `artifact`, `sha256` | Fixed JSON measurement artifact and its raw digest. |
| `locator` | Object with `type: "json_pointer"` and a `value` pointer to a number. |
| `value`, `unit` | Referenced finite numeric value and its declared unit. |
| `context` | `dataset`, `split`, `method`, `baseline`, and a `conditions` object. |
| `baseline_locator`, `baseline_value` | JSON Pointer string and finite value for the baseline. |

Store each measurement in an object with a numeric field named `value`.
Both pointers must end in `/value`.
The containing measurement object must include `dataset`, `split`, `method`, `unit`, and `conditions`.
The method measurement also includes `baseline`.
Its fields must match the ledger's declared context and unit.

The baseline measurement's method must equal `context.baseline`.
Its dataset, split, unit, and conditions must match the comparison.
Additional source measurement fields are allowed.

If you convert a result to this format, preserve the original file.
Save the converted result as a separate artifact.

Use RFC 6901 pointer escaping, including `~0` for `~` and `~1` for `/`.
For array indices, use `0` or a positive integer without leading zeros.
Booleans are not measurements and do not equal numeric conditions.
The checker compares JSON values and types at the specified fields.
The numbers `1` and `1.0` are equal in these comparisons.
The checker parses fractional and exponent tokens as exact decimal values.
It compares these values without rounding, including values nested inside conditions.
Thus `1e-400` does not equal `0`, and `0.80000000000000004` does not equal `0.8`.

The checker retains its earlier range rule for fractional and exponent tokens.
Their conversion to Python's binary64 float format must remain finite.
That conversion only determines whether the token passes the range rule.
It never supplies the value used for comparison.
For example, `1e999` is finite mathematically but fails the retained float-conversion range check.
Integer tokens retain Python's exact integer parsing.
Non-finite tokens and decimal exponents outside the parser's supported range are rejected.

The checker does not search for arbitrary number occurrences in text.
It compares only declared conditions and cannot find omitted experimental constraints.
Matching metadata does not establish a fair baseline, significance, causation, or generalization.
Record uncertainty and opposing observations in the review.

## Preserve literature access limits

A literature entry records a `source` object and a `locator` object.
The source contains `version`, `identifier`, `reading_depth`, `content_kind`, and `access_limitations`.
Use an actual DOI or URL for the identifier of a real source.
Distinguish a preprint from a publisher version.
The checker treats the identifier as text.
It does not determine whether the identifier is valid or the source exists.

Use `metadata`, `abstract`, `excerpt`, or `full_text` for reading depth.
Use `none`, `metadata`, `excerpt`, or `full_text` for locally stored content kind.
Do not call a summary a full-text reading.

Use `page`, `section`, or `quote` for the locator type.
Record the location in `value`.
For a local source, the checker makes sure that a quote occurs in its UTF-8 content.
The reviewer inspects the recorded page and section locations.
The checker does not understand PDF page layout.
It does not contact DOI services.

If you have a permitted local snapshot, set `artifact` and `sha256` together.
The hash identifies the stored content, which can be an excerpt or metadata rather than full text.
When no local snapshot exists, set both fields to `null`.
Use content kind `none` in that case.
Explain stability limits in `limitations` and access limits in `source.access_limitations`.
Both arrays must then be nonempty.

Reading depth describes what was read, while content kind describes what was retained locally.
If you declare full-text reading but retain only excerpts or metadata, provide both nonempty limitation arrays.
The checker cannot determine the actual reading depth.
Never invent a full-text hash.
Do not upload or save sources without permission to do so.

Use `available`, `missing`, `inaccessible`, or `version_uncertain` for availability.
For a non-available source, supply a `reason` and access limitations.
These labels describe source access and version limits rather than scientific support.
Missing and inaccessible sources are not evidence of fabrication.
An unsupported claim also does not by itself establish fabrication.
Retain source-version uncertainty instead of substituting a different version silently.

## Assess support in the existing review

For a result with a ledger, an accepted review includes `claim_evidence` in its task acceptance JSON.
This object has `ledger`, `assessments`, and `unreviewed_claim_ids`.
`ledger` contains the result's ledger `path` and exact `sha256`.
Each assessment has `claim_id`, `verdict`, `scope`, `reason`, `gaps`, and `follow_up`.
Use text for scope and reason and arrays of text for gaps and follow-up actions.

Use `yes`, `partial`, `no`, or `unable_to_assess` for the verdict.
Every ledger claim must appear exactly once, either in assessments or in `unreviewed_claim_ids`.
This makes checked and unchecked scope explicit.
A listed unreviewed claim has no scientific assessment.
Do not infer support from its absence in the assessment list.

Blocked or rework reviews can omit `claim_evidence`.
If a review supplies this object, the checker applies all its rules.

Explain the supported range and remaining gaps.
For partial support, propose narrower wording through a new attempt.
For a `no` verdict, retain negative results and opposing evidence.
If the available evidence cannot support a judgment, use `unable_to_assess`.
A structurally valid review can record partial or negative support and still accept accurate completion of its task.

The checker makes sure that the references and declared review scope match the records.
It does not judge scientific support.

Before proposing extra experiments, identify the unresolved explanation and discriminating observation.
State the smallest useful resources and seek the existing required authorization.
Do not retry until a preferred verdict appears.

## Inspect and migrate only the selected scope

Run the existing record checker with current tasks, results, and the relevant review history.
See the [offline practice example](../../../examples/claim-evidence/README.md) for complete synthetic records.
The checker reports errors in fields, paths, hashes, locations, context, and references through the existing diagnostics.
Errors in a required upstream ledger invalidate that dependency's structural acceptance.
The checker does not search for omitted review history or prove stable IDs across all past attempts.

HTML comments no longer supply active task acceptance.
Comment markers inside fenced code remain literal data.
Hashes still use the complete original bytes, including comments and line endings.

If an old dependency relied only on commented acceptance, preserve that file as an ordinary historical discussion.
Write a new active review of the unchanged result with `supersedes: null`.
Repin dependent contracts through new revisions and attempts.
Do not use `supersedes` to point to a file with no valid active acceptance block.
If the earlier review still has valid active acceptance, use the normal replacement rules.
Do not rewrite a completed historical review to make the checker pass.

Legacy records without ledgers need no migration.
