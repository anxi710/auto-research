# Bulk CLI acceptance conditions

Define these conditions before adopting the scripted procedure.
Use fake command responses and temporary directories.
Do not use real libraries, authentication, or cloud destinations.

The default command must print a plan without running tools or writing run files.
An explicit execution must export, select attachments, transfer, reconcile Drive IDs, import, and save cited answers.
Saved answers remain generated evidence that needs original-paper inspection.
These tests inspect the runner's mechanics with fake services.
They do not establish human authorization or enforce research review.
The [human review cases](human-review.md) test when the assistant can use an uninterrupted run.

Protect these conditions:

1. Reject paths outside the export workspace and mismatched file hashes.
2. Upload one copy of a duplicate attachment while preserving its collection membership.
3. Resume completed work without creating another notebook or importing the same file again.
4. Reconcile interrupted writes by returned IDs or unique remote matches before continuing.
5. Keep unresolved writes pending when their outcome remains unknown.
6. Preserve failed imports and source-processing timeouts as incomplete work.
7. Stop at the configured query budget without claiming full coverage.
8. Reject changed configuration or changed snapshots within a saved run.
9. Reject malformed tool responses and unsupported NotebookLM client versions before unsafe continuation.
10. Keep credentials and unfiltered authentication output out of saved records.

Run the implemented unit tests and a command-line plan smoke test.
Inspect the command contracts against the pinned client source.
Record any untested condition rather than inferring a pass.
Do not claim a working live integration from fake command tests.
