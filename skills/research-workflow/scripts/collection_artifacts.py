"""Versioned response artifacts; collection coverage never grants acceptance."""

from evidence_ledger import LedgerValidator, digest, identifier, text


KINDS = {"worker_response", "literal_aggregate", "synthesis"}


def reference(value):
    return (isinstance(value, dict) and set(value) == {"path", "sha256"}
            and text(value["path"]) and digest(value["sha256"]))


def revision(value):
    return type(value) is int and value > 0


class CollectionValidator(LedgerValidator):
    def task_schema(self, task, source):
        valid = True
        if "response_branches" in task:
            branches = task["response_branches"]
            if not isinstance(branches, list) or not branches:
                self.issue("SCHEMA", source, "task.response_branches must be a nonempty array.")
                return False
            seen = set()
            for branch in branches:
                good = self.fields(branch, {
                    "branch_id": identifier, "task_path": text, "task_revision": revision,
                    "task_sha256": digest, "result_path": text, "response_path": text,
                }, source, "response_branches[]")
                valid = good and valid
                if good:
                    if branch["branch_id"] in seen:
                        self.issue("DUPLICATE_ID", source, "Duplicate expected response branch.")
                        valid = False
                    seen.add(branch["branch_id"])
                    for key in ("task_path", "result_path", "response_path"):
                        valid = self.lint.path(branch[key], source, required=False) is not None and valid
        if "synthesis" in task and not text(task["synthesis"]):
            self.issue("SCHEMA", source, "task.synthesis must be a research-relative path.")
            valid = False
        return valid

    def validate(self, kind, path, source, result=None):
        if path in self.lint.artifact_stack:
            self.issue("BINDING", source, "Response artifact references contain a cycle.")
            return None
        self.lint.artifact_stack.add(path)
        try:
            return self._validate(kind, path, source, result)
        finally:
            self.lint.artifact_stack.remove(path)

    def _validate(self, kind, path, source, result):
        value = self.read(path, source, structured=True)
        fields = {"schema_version": lambda v: v == "1", "artifact_type": lambda v: v == kind,
                  "task_id": identifier, "task_revision": revision, "attempt_id": identifier}
        if kind == "worker_response":
            fields.update(branch_id=identifier, content=text)
        elif kind == "literal_aggregate":
            fields.update(contract=reference, branches=lambda v: isinstance(v, list),
                          coverage=lambda v: isinstance(v, dict))
        else:
            fields.update(aggregate=reference, coverage=lambda v: isinstance(v, dict),
                          manuscript=reference, evidence_ledger=reference)
        if not self.fields(value, fields, source, kind):
            return None
        if result is not None and any(value[key] != result[key]
                                      for key in ("task_id", "task_revision", "attempt_id")):
            self.issue("BINDING", source, f"{kind} identity does not match its result.")
        if kind == "literal_aggregate":
            if result is not None and value["contract"]["sha256"].lower() != result["task_sha256"].lower():
                self.issue("BINDING", source, "Aggregate scope must match its result's exact fixed contract.")
            self.aggregate(value, source)
        elif kind == "synthesis":
            self.synthesis(value, source, result)
        return value

    def fixed(self, entry, source):
        path = self.lint.reference(entry["path"], source, entry["sha256"])
        if path is None or self.lint.hashes.get(path) != entry["sha256"].lower():
            return None
        return path

    def aggregate(self, value, source):
        contract = self.fixed(value["contract"], source)
        if contract is None:
            return
        expected, diagnostics = collect(self.lint.root, contract, value["attempt_id"],
                                        self.lint.artifact_stack)
        if diagnostics:
            self.issue("BINDING", source, "Aggregate contract is invalid: " + diagnostics[0]["message"])
            return
        if any(value[key] != expected[key] for key in ("task_id", "task_revision")):
            self.issue("BINDING", source, "Aggregate identity does not match its fixed collection contract.")
        # Pins preserve the collected version even when a newly available branch changes coverage.
        for branch in value["branches"]:
            if not isinstance(branch, dict):
                continue
            for key in ("result", "response"):
                if reference(branch.get(key)):
                    self.fixed(branch[key], source)
        if value["branches"] != expected["branches"]:
            self.issue("BINDING", source, "Aggregate branches differ from the fixed scope and current source versions; recollect in a new attempt.")
        if value["coverage"] != expected["coverage"]:
            self.issue("BINDING", source, "Aggregate coverage must list every expected branch and every collection gap exactly once.")

    def synthesis(self, value, source, result):
        aggregate_path = self.fixed(value["aggregate"], source)
        aggregate = (self.validate("literal_aggregate", aggregate_path, source)
                     if aggregate_path is not None else None)
        if aggregate is not None and value["coverage"] != aggregate["coverage"]:
            self.issue("BINDING", source, "Synthesis must preserve the aggregate's exact coverage and gaps.")
        for key in ("manuscript", "evidence_ledger"):
            target = self.fixed(value[key], source)
            if result is None:
                continue
            entries = [entry for entry in result["artifacts"]
                       if self.lint.path(entry["path"], source) == target
                       and entry["sha256"].lower() == value[key]["sha256"].lower()]
            if len(entries) != 1 or (key == "evidence_ledger" and entries[0].get("kind") != "claim_evidence_ledger"):
                self.issue("BINDING", source, f"Synthesis {key} must be a fixed artifact of the same result with its required kind.")
        if result is not None:
            refs = self.lint.refs.get(("result", source), {})
            task = self.lint.records["task"].get(refs.get("task"))
            if task is not None and not any(
                    self.lint.path(entry["path"], source) == aggregate_path
                    and entry["sha256"].lower() == value["aggregate"]["sha256"].lower()
                    for entry in task["inputs"]):
                self.issue("BINDING", source, "Synthesis aggregate must be a fixed input of its task contract.")
            ledger = refs.get("ledger")
            manuscript = self.lint.path(value["manuscript"]["path"], source)
            if ledger is not None:
                for claim in ledger["claims"]:
                    location = claim.get("location") if isinstance(claim, dict) else None
                    if (not isinstance(location, dict) or not text(location.get("artifact"))
                            or self.lint.path(location["artifact"], source) != manuscript
                            or not digest(location.get("sha256"))
                            or location["sha256"].lower() != value["manuscript"]["sha256"].lower()):
                        self.issue("BINDING", source, "Synthesis ledger claims must locate the fixed synthesis manuscript.")

    def result(self, path, result, task):
        typed = [entry for entry in result["artifacts"]
                 if isinstance(entry.get("kind"), str) and entry["kind"] in KINDS]
        for kind in KINDS:
            if sum(entry["kind"] == kind for entry in typed) > 1:
                self.issue("DUPLICATE_ID", path, f"A result may contain at most one {kind} artifact.")
        if task is not None and result["execution_status"] == "completed":
            if "response_branches" in task and not any(entry["kind"] == "literal_aggregate" for entry in typed):
                self.issue("BINDING", path, "A completed collection task requires a literal_aggregate artifact.")
            if "synthesis" in task:
                target = self.lint.path(task["synthesis"], path)
                if not any(entry["kind"] == "synthesis" and self.lint.path(entry["path"], path) == target
                           for entry in typed):
                    self.issue("BINDING", path, "A completed synthesis task requires its declared synthesis artifact.")
        for entry in typed:
            artifact = self.fixed(entry, path)
            if artifact is not None:
                self.validate(entry["kind"], artifact, path, result)


def observed(lint, value, source):
    path = lint.path(value, source)
    hashed = lint.digest(path, source) if path is not None else None
    return {"path": path, "sha256": hashed} if hashed is not None else None


def collect_branch(root, branch, stack):
    # Reuse record, ledger, dependency and current-contract checks. Failures become
    # explicit collection gaps; they do not manufacture technical acceptance.
    from lint_records import Linter
    lint = Linter(root, artifact_stack=stack)
    task_path = lint.reference(branch["task_path"], ".", branch["task_sha256"], kind="task", current=True)
    result_path = lint.reference(branch["result_path"], ".", kind="result")
    lint.load()
    lint.check()
    task = lint.records["task"].get(task_path)
    result = lint.records["result"].get(result_path)
    if task is not None and task["revision"] != branch["task_revision"]:
        lint.issue("STALE", ".", "Branch contract revision differs from the fixed collection scope.")
    result_ref = observed(lint, branch["result_path"], ".")
    response_ref = observed(lint, branch["response_path"], ".")
    response = None
    if result is not None and response_ref is not None:
        matches = [entry for entry in result["artifacts"]
                   if lint.path(entry["path"], ".") == response_ref["path"]
                   and entry.get("kind") == "worker_response"]
        if len(matches) != 1:
            lint.issue("BINDING", ".", "Expected response must occur once as a worker_response result artifact.")
        else:
            response = lint.collection_validator.validate("worker_response", response_ref["path"], ".", result)
            if response is not None and response["branch_id"] != branch["branch_id"]:
                lint.issue("BINDING", ".", "Response belongs to a different expected branch.")
    codes = {item["code"] for item in lint.output()["diagnostics"]}
    if "DUPLICATE_ID" in codes:
        state = "duplicate"
    elif codes & {"HASH", "STALE"}:
        state = "stale"
    elif "SCHEMA" in codes:
        state = "malformed"
    elif result_ref is None or response_ref is None:
        state = "missing"
    elif result is not None and result["execution_status"] != "completed":
        state = "unfinished"
    elif codes or response is None:
        state = "invalid"
    else:
        state = "collected"
    return {"branch_id": branch["branch_id"], "state": state, "result": result_ref,
            "response": response_ref, "content": response["content"] if response is not None and not codes else None,
            "diagnostics": lint.output()["diagnostics"]}


def collect(root, task_path, attempt_id, stack=None):
    """Return a literal artifact and contract errors; branch errors remain gaps."""
    from lint_records import Linter
    lint = Linter(root, artifact_stack=stack)
    canonical = lint.reference(task_path, ".", kind="task", current=True)
    lint.load()
    lint.check()
    task = lint.records["task"].get(canonical)
    if task is not None and "response_branches" not in task:
        lint.issue("SCHEMA", canonical, "A collection task requires response_branches.")
    if lint.diagnostics or task is None:
        return None, lint.output()["diagnostics"]
    branches = [collect_branch(root, branch, lint.artifact_stack) for branch in task["response_branches"]]
    # Different branch labels must not turn one physical submission into two outputs.
    for key in ("result", "response"):
        groups = {}
        for branch in branches:
            if branch[key] is not None:
                path = root / branch[key]["path"]
                try:
                    info = path.stat()
                except OSError:
                    branch["state"], branch["content"] = "invalid", None
                    branch["diagnostics"].append({"code": "READ", "path": branch[key]["path"],
                                                  "message": "Source changed during collection; recollect after writes finish."})
                    continue
                groups.setdefault((info.st_dev, info.st_ino), []).append(branch)
        for duplicates in groups.values():
            if len(duplicates) > 1:
                for branch in duplicates:
                    branch["state"], branch["content"] = "duplicate", None
                    issue = {"code": "DUPLICATE_ID", "path": branch[key]["path"],
                             "message": f"Multiple branches refer to the same {key} file."}
                    branch["diagnostics"].append(issue)
    coverage = {"expected": [branch["branch_id"] for branch in branches],
                "collected": [branch["branch_id"] for branch in branches if branch["state"] == "collected"],
                "gaps": [{"branch_id": branch["branch_id"], "reason": branch["state"]}
                         for branch in branches if branch["state"] != "collected"]}
    return {"schema_version": "1", "artifact_type": "literal_aggregate", "task_id": task["task_id"],
            "task_revision": task["revision"], "attempt_id": attempt_id,
            "contract": {"path": canonical, "sha256": lint.hashes[canonical]},
            "branches": branches, "coverage": coverage}, []
