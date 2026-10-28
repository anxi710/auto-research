"""Exercise actual collector output through the existing read-only consumer."""

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "skills/research-workflow/scripts"


class ResponseCollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("budget.md", "Synthetic offline fixture only.\n")
        self.branches = [self.worker("left"), self.worker("right")]
        self.task = self.contract("join")
        self.task["response_branches"] = self.branches
        self.save_contract("join", self.task)

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2) + "\n" if isinstance(value, dict) else value,
                          encoding="utf-8", newline="")

    def read(self, path):
        return json.loads((self.root / path).read_text())

    def digest(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def ref(self, path, kind=None):
        return {"path": path, "sha256": self.digest(path), **({"kind": kind} if kind else {})}

    def contract(self, name):
        return {"task_id": name, "revision": 1, "goal": "Report fixed synthetic inputs.",
                "owner": "worker", "inputs": [], "dependencies": [], "write_paths": [name + "/"],
                "budget_ref": "budget.md", "acceptance": ["Preserve evidence and gaps."],
                "stop_condition": "Stop after the requested output."}

    def save_contract(self, name, task):
        self.write(name + "/task.json", task)
        self.write(name + "/snapshot.json", task)

    def result(self, name, artifacts):
        value = {"task_id": name, "task_revision": 1, "attempt_id": "A1",
                 "task_path": name + "/snapshot.json", "task_sha256": self.digest(name + "/snapshot.json"),
                 "execution_status": "completed", "artifacts": artifacts,
                 "unresolved": [], "resource_usage": {"tokens": None}, "next_action": "Present for review."}
        self.write(name + "/result.json", value)
        return value

    def worker(self, name):
        self.save_contract(name, self.contract(name))
        self.write(name + "/response.json", {
            "schema_version": "1", "artifact_type": "worker_response", "task_id": name,
            "task_revision": 1, "attempt_id": "A1", "branch_id": name,
            "content": name + " observation: negative result.\r\nDo not infer acceptance. Ω\n",
        })
        self.result(name, [self.ref(name + "/response.json", "worker_response")])
        return {"branch_id": name, "task_path": name + "/task.json", "task_revision": 1,
                "task_sha256": self.digest(name + "/task.json"), "result_path": name + "/result.json",
                "response_path": name + "/response.json"}

    def run_script(self, script, args, expected=0):
        run = subprocess.run([sys.executable, "-B", str(SCRIPTS / script), "--root", str(self.root), *args],
                             capture_output=True, text=True, timeout=15)
        self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        return json.loads(run.stdout)

    def collect(self, expected=0):
        return self.run_script("collect_responses.py", ["--task", "join/task.json", "--attempt-id", "A1",
                                                        "--output", "join/aggregate.json"], expected)

    def submit(self):
        self.result("join", [self.ref("join/aggregate.json", "literal_aggregate")])

    def lint(self, expected=0, name="join"):
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        value = self.run_script("lint_records.py", ["--task", name + "/task.json", "--result", name + "/result.json"], expected)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        return value["diagnostics"]

    def rewrite_worker_result(self, name="right"):
        result = self.read(name + "/result.json")
        result["artifacts"] = [self.ref(name + "/response.json", "worker_response")]
        self.write(name + "/result.json", result)

    def test_normal_collection_preserves_literal_content_and_consumes_without_review(self):
        output = self.collect()
        self.assertEqual(output["coverage"], {"expected": ["left", "right"], "collected": ["left", "right"], "gaps": []})
        aggregate = self.read("join/aggregate.json")
        self.assertEqual(aggregate["branches"][0]["content"], self.read("left/response.json")["content"])
        self.assertFalse(any(key in aggregate for key in ("accepted", "approval", "decision", "execution_status")))
        self.submit()
        self.lint()

    def test_missing_unfinished_truncated_and_stale_sources_remain_explicit_gaps(self):
        for failure in ("missing", "unfinished", "malformed", "stale"):
            with self.subTest(failure=failure):
                original_result = (self.root / "right/result.json").read_bytes()
                original_response = (self.root / "right/response.json").read_bytes()
                original_task = (self.root / "right/task.json").read_bytes()
                if failure == "missing":
                    (self.root / "right/result.json").unlink()
                elif failure == "unfinished":
                    result = self.read("right/result.json")
                    result["execution_status"] = "blocked"
                    self.write("right/result.json", result)
                elif failure == "malformed":
                    self.write("right/response.json", '{"schema_version":"1",')
                    self.rewrite_worker_result()
                else:
                    task = self.read("right/task.json")
                    task["revision"] += 1
                    self.write("right/task.json", task)
                output = self.collect()
                self.assertEqual(output["coverage"]["collected"], ["left"])
                self.assertEqual(output["coverage"]["gaps"], [{"branch_id": "right", "reason": failure}])
                self.submit()
                self.lint()
                aggregate = self.read("join/aggregate.json")
                aggregate["coverage"]["gaps"] = []
                aggregate["coverage"]["collected"].append("right")
                self.write("join/aggregate.json", aggregate)
                self.submit()
                self.assertIn("BINDING", {d["code"] for d in self.lint(1)})
                (self.root / "join/aggregate.json").unlink()
                (self.root / "right/result.json").write_bytes(original_result)
                (self.root / "right/response.json").write_bytes(original_response)
                (self.root / "right/task.json").write_bytes(original_task)

    def test_changed_response_or_result_after_collection_invalidates_consumption(self):
        for target in ("response", "result", "task"):
            with self.subTest(target=target):
                path = "right/" + target + ".json"
                original = (self.root / path).read_bytes()
                self.collect()
                self.submit()
                data = self.read(path)
                if target == "response":
                    data["content"] += " Changed."
                elif target == "result":
                    data["next_action"] = "Changed next action."
                else:
                    data["revision"] = 2
                self.write(path, data)
                diagnostics = self.lint(1)
                self.assertTrue({d["code"] for d in diagnostics} & {"HASH", "BINDING"})
                (self.root / path).write_bytes(original)
                (self.root / "join/aggregate.json").unlink()

    def test_previously_missing_branch_becoming_available_requires_new_aggregate(self):
        original = (self.root / "right/result.json").read_bytes()
        (self.root / "right/result.json").unlink()
        self.collect()
        self.submit()
        self.lint()
        (self.root / "right/result.json").write_bytes(original)
        self.assertIn("BINDING", {d["code"] for d in self.lint(1)})

    def test_duplicate_physical_submission_is_not_two_collected_branches(self):
        self.branches[1].update(result_path="left/result-alias.json", response_path="left/response-alias.json")
        os.link(self.root / "left/result.json", self.root / "left/result-alias.json")
        os.symlink("response.json", self.root / "left/response-alias.json")
        self.save_contract("join", self.task)
        output = self.collect()
        self.assertEqual(output["coverage"]["collected"], [])
        self.assertEqual([g["reason"] for g in output["coverage"]["gaps"]], ["duplicate", "duplicate"])
        self.submit()
        self.lint()

    def test_duplicate_expected_ids_and_unsafe_paths_fail_before_writing(self):
        for field, value in (("branch_id", "left"), ("response_path", "../outside.json")):
            with self.subTest(field=field):
                task = copy.deepcopy(self.task)
                task["response_branches"][1][field] = value
                self.save_contract("join", task)
                self.collect(1)
                self.assertFalse((self.root / "join/aggregate.json").exists())

    def test_collector_never_overwrites_existing_evidence(self):
        self.collect()
        before = (self.root / "join/aggregate.json").read_bytes()
        self.collect(1)
        self.assertEqual(before, (self.root / "join/aggregate.json").read_bytes())

    def test_collector_respects_existing_contract_write_scope(self):
        self.run_script("collect_responses.py", ["--task", "join/task.json", "--attempt-id", "A1",
                                                 "--output", "outside.json"], 1)
        self.assertFalse((self.root / "outside.json").exists())

    def test_kind_version_wrong_branch_and_approval_fields_are_rejected(self):
        original = self.read("right/response.json")
        for key, value in (("artifact_type", "synthesis"), ("schema_version", "2"),
                           ("branch_id", "left"), ("approved", True)):
            with self.subTest(key=key):
                response = {**original, key: value}
                self.write("right/response.json", response)
                self.rewrite_worker_result()
                output = self.collect()
                self.assertEqual(output["coverage"]["collected"], ["left"])
                self.submit()
                self.lint()
                (self.root / "join/aggregate.json").unlink()

    def test_omitted_kind_cannot_bypass_declared_collection(self):
        self.collect()
        self.result("join", [self.ref("join/aggregate.json")])
        self.assertIn("BINDING", {d["code"] for d in self.lint(1)})

    def test_aggregate_cannot_substitute_a_reduced_contract_with_the_same_identity(self):
        reduced = copy.deepcopy(self.task)
        reduced["response_branches"] = reduced["response_branches"][:1]
        self.write("join/reduced.json", reduced)
        self.run_script("collect_responses.py", ["--task", "join/reduced.json", "--attempt-id", "A1",
                                                 "--output", "join/aggregate.json"])
        self.submit()
        self.assertIn("BINDING", {d["code"] for d in self.lint(1)})

    def test_nonstring_legacy_kind_does_not_crash_the_consumer(self):
        self.collect()
        self.submit()
        result = self.read("join/result.json")
        result["artifacts"].append({**self.ref("budget.md"), "kind": []})
        self.write("join/result.json", result)
        self.lint()

    def review(self, decision="accepted", path="left/review.md", supersedes=None):
        value = {"review_id": "R2" if supersedes else "R1", "task_id": "left", "task_revision": 1,
                 "attempt_id": "A1", "result_path": "left/result.json", "result_sha256": self.digest("left/result.json"),
                 "reviewer": "reviewer", "decision_owner": "coordinator", "decision": decision,
                 "basis": ["left/response.json"], "unresolved": [], "supersedes": supersedes}
        self.write(path, "# Review\n\n## Task acceptance\n\n```json\n" + json.dumps(value) + "\n```\n")
        return {"task_path": "left/task.json", "task_revision": 1, "result_path": "left/result.json",
                "result_sha256": self.digest("left/result.json"), "review_path": path, "review_sha256": self.digest(path)}

    def test_existing_review_acceptance_rework_and_supersession_remain_authoritative(self):
        self.task["dependencies"] = [self.review()]
        self.save_contract("join", self.task)
        self.collect()
        self.submit()
        self.lint()
        (self.root / "join/aggregate.json").unlink()
        self.task["dependencies"] = [self.review("rework")]
        self.save_contract("join", self.task)
        output = self.collect(1)
        self.assertIn("DEPENDENCY", {d["code"] for d in output["diagnostics"]})
        old = self.review()
        newer = self.review(path="left/new-review.md", supersedes=self.ref("left/review.md"))
        self.task["dependencies"] = [old, newer]
        self.save_contract("join", self.task)
        output = self.collect(1)
        self.assertIn("DEPENDENCY", {d["code"] for d in output["diagnostics"]})

    def test_embedded_content_and_unknown_aggregate_fields_cannot_be_rewritten(self):
        self.collect()
        original = self.read("join/aggregate.json")
        for change in ("content", "gap", "approval"):
            with self.subTest(change=change):
                aggregate = copy.deepcopy(original)
                if change == "content":
                    aggregate["branches"][0]["content"] = "A fabricated observation."
                elif change == "gap":
                    aggregate["branches"].pop()
                else:
                    aggregate["approved"] = True
                self.write("join/aggregate.json", aggregate)
                self.submit()
                self.lint(1)

    def synthesis(self):
        self.collect()
        self.submit()
        task = self.contract("synth")
        task.update(synthesis="synth/synthesis.json", evidence_ledger="synth/ledger.json")
        task["inputs"] = [self.ref("join/aggregate.json")]
        self.save_contract("synth", task)
        claim = "The retained observations are limited."
        self.write("synth/manuscript.md", claim + "\n")
        self.write("synth/ledger.json", {
            "schema_version": "1", "task_id": "synth", "attempt_id": "A1", "claims": [{
                "claim_id": "C1", "text": claim,
                "location": {"artifact": "synth/manuscript.md", "sha256": self.digest("synth/manuscript.md"), "exact_quote": claim},
                "evidence": [{"evidence_id": "E1", "kind": "literature", "availability": "missing",
                    "scope": "Synthetic missing source.", "limitations": ["No stored source."],
                    "artifact": None, "sha256": None, "reason": "Offline fixture.",
                    "source": {"version": "v1", "identifier": "urn:synthetic", "reading_depth": "metadata",
                               "content_kind": "none", "access_limitations": ["Offline fixture."]},
                    "locator": {"type": "section", "value": "Unverified section"}}],
                "verification_request": {"question": "Does the evidence support this limit?", "limitations": []},
            }]})
        value = {"schema_version": "1", "artifact_type": "synthesis", "task_id": "synth", "task_revision": 1,
                 "attempt_id": "A1", "aggregate": self.ref("join/aggregate.json"),
                 "coverage": self.read("join/aggregate.json")["coverage"],
                 "manuscript": self.ref("synth/manuscript.md"), "evidence_ledger": self.ref("synth/ledger.json")}
        self.write("synth/synthesis.json", value)
        self.result("synth", [self.ref("synth/synthesis.json", "synthesis"), self.ref("synth/manuscript.md"),
                              self.ref("synth/ledger.json", "claim_evidence_ledger")])

    def test_synthesis_uses_existing_ledger_and_propagates_partial_coverage(self):
        (self.root / "right/result.json").unlink()
        self.synthesis()
        self.lint(name="synth")
        value = self.read("synth/synthesis.json")
        value["coverage"]["gaps"] = []
        self.write("synth/synthesis.json", value)
        result = self.read("synth/result.json")
        result["artifacts"][0] = self.ref("synth/synthesis.json", "synthesis")
        self.write("synth/result.json", result)
        self.assertIn("BINDING", {d["code"] for d in self.lint(1, "synth")})

    def test_synthesis_cannot_substitute_an_unlisted_or_invalid_ledger(self):
        self.synthesis()
        self.lint(name="synth")
        ledger = self.read("synth/ledger.json")
        ledger["claims"][0]["location"]["exact_quote"] = "Changed claim."
        self.write("synth/ledger.json", ledger)
        synthesis = self.read("synth/synthesis.json")
        synthesis["evidence_ledger"] = self.ref("synth/ledger.json")
        self.write("synth/synthesis.json", synthesis)
        self.result("synth", [self.ref("synth/synthesis.json", "synthesis"), self.ref("synth/manuscript.md"),
                              self.ref("synth/ledger.json", "claim_evidence_ledger")])
        self.assertIn("BINDING", {d["code"] for d in self.lint(1, "synth")})

    def test_synthesis_cannot_use_an_undeclared_aggregate_or_unrelated_manuscript(self):
        self.synthesis()
        task = self.read("synth/task.json")
        task["inputs"] = []
        self.save_contract("synth", task)
        result = self.read("synth/result.json")
        result["task_sha256"] = self.digest("synth/snapshot.json")
        self.write("synth/result.json", result)
        self.assertIn("BINDING", {d["code"] for d in self.lint(1, "synth")})
        task["inputs"] = [self.ref("join/aggregate.json")]
        self.save_contract("synth", task)
        self.write("synth/unrelated.md", "An unrelated manuscript.\n")
        synthesis = self.read("synth/synthesis.json")
        synthesis["manuscript"] = self.ref("synth/unrelated.md")
        self.write("synth/synthesis.json", synthesis)
        result["task_sha256"] = self.digest("synth/snapshot.json")
        result["artifacts"][0] = self.ref("synth/synthesis.json", "synthesis")
        result["artifacts"].append(self.ref("synth/unrelated.md"))
        self.write("synth/result.json", result)
        self.assertIn("BINDING", {d["code"] for d in self.lint(1, "synth")})


if __name__ == "__main__":
    unittest.main()
