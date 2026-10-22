"""Offline behavior tests. No accounts or external processes are used."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/research-workflow/scripts/bulk_literature.py"
spec = importlib.util.spec_from_file_location("bulk_literature", SCRIPT)
bulk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bulk)


class FakeTools:
    def __init__(self):
        self.calls = []
        self.notebooks = []
        self.sources = {}
        self.drive = []
        self.export_entries = None
        self.fail = None
        self.wait_timeout = False
        self.degraded = False
        self.version = "0.8.5"
        self.auth = True
        self.remote_changed = False

    def reply(self, args, data, code=0):
        return subprocess.CompletedProcess(args, code, json.dumps(data), "")

    def __call__(self, args, **kwargs):
        self.calls.append(args)
        tool, action = args[:2]
        if action in ("version", "--version"):
            return subprocess.CompletedProcess(args, 0, self.version if tool == "notebooklm" else "1.3.1", "")
        if args[1:3] == ["auth", "check"]:
            return self.reply(args, {"status": "ok", "checks": {"token_fetch": self.auth}, "storage_path": "SECRET"})
        if tool == "zpm":
            root = Path(args[args.index("--output") + 1]) / "Selection"
            (root / ".zpm").mkdir(parents=True)
            entries = []
            for index in range(3):
                relative = f"collection-{index}/paper.pdf"
                path = root / relative
                path.parent.mkdir()
                # The last path repeats the first attachment through another collection.
                path.write_bytes(b"%PDF-1.7\n" + bytes([index % 2]))
                entries.append({"collection_key": f"COL{index}", "item_key": f"ITEM{index % 2}", "attachment_key": f"ATT{index % 2}", "state": "active", "destination_path": relative, "sha256": bulk.digest(path), "source_path": "/PRIVATE/PATH", "title": f"Paper {index % 2}"})
            if self.export_entries:
                self.export_entries(entries, root)
            (root / ".zpm/metadata.json").write_text(json.dumps({"generated_by": "zpm", "schema_version": 1, "collection_key": "TESTCOL", "items": entries}))
            return self.reply(args, {})
        if tool == "rclone":
            if action == "check" and self.remote_changed:
                return self.reply(args, {}, 1)
            if action == "copy":
                paths = Path(args[args.index("--files-from") + 1]).read_text().splitlines()
                if not self.drive:
                    self.drive = [{"Path": path, "ID": f"drive-{i}"} for i, path in enumerate(paths)]
            return self.reply(args, self.drive if action == "lsjson" else {})
        if action == "list":
            return self.reply(args, {"notebooks": self.notebooks})
        if action == "create":
            notebook = {"id": f"nb-{len(self.notebooks)}", "title": args[2]}
            self.notebooks.append(notebook)
            self.sources[notebook["id"]] = []
            if self.fail == "create":
                self.fail = None
                return self.reply(args, {"error": True, "code": "UNCONFIRMED_WRITE"}, 1)
            if self.fail == "create-json":
                self.fail = None
                return subprocess.CompletedProcess(args, 0, "invalid", "")
            return self.reply(args, {"notebook": notebook})
        notebook = args[args.index("-n") + 1]
        if action == "ask":
            if self.fail == "ask":
                self.fail = None
                return self.reply(args, {"error": True}, 1)
            ids = [args[index + 1] for index, part in enumerate(args) if part == "-s"]
            return self.reply(args, {"answer": "Generated finding [1].", "references": [{"source_id": sid, "citation_number": i + 1, "cited_text": "Original passage", "start_char": 3, "end_char": 9} for i, sid in enumerate(ids)], "conversation_id": "conversation", "turn_number": 1})
        operation = args[2]
        if operation == "list":
            return self.reply(args, {"sources": self.sources[notebook]})
        if operation == "add-drive":
            row = {"id": f"source-{notebook}-{len(self.sources[notebook])}", "title": args[4], "drive_document_id": args[3], "status": "ready", "drive_status": "active", "is_drive_degraded": self.degraded}
            self.sources[notebook].append(row)
            if self.fail == "add-drive":
                self.fail = None
                return self.reply(args, {"error": True, "code": "UNCONFIRMED_WRITE"}, 1)
            return self.reply(args, {"source": {**row, "drive_file_id": args[3]}})
        if operation == "wait":
            return self.reply(args, {"source_id": args[3], "status": "timeout" if self.wait_timeout else "ready"}, 2 if self.wait_timeout else 0)
        if operation == "fulltext":
            return self.reply(args, {"source_id": args[3], "content": "Indexed text from this paper.", "char_count": 29})
        raise AssertionError(args)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.settings_file = self.root / "settings.json"
        self.settings = {"collection_key": "TESTCOL", "question": "Which evidence supports the method?", "remote": "drive:literature", "run_dir": "run-2026-10-23", "source_limit": 2, "batch_size": 1, "max_queries": 2}
        self.settings_file.write_text(json.dumps(self.settings))
        self.tools = FakeTools()

    def tearDown(self):
        self.temp.cleanup()

    def pipeline(self):
        return bulk.Pipeline(bulk.load_config(self.settings_file), self.tools)

    def count(self, tool, operation):
        return sum(args[0] == tool and operation in args[1:3] for args in self.tools.calls)

    def test_plan_has_zero_effects(self):
        before = sorted(self.root.rglob("*"))
        plan = self.pipeline().plan()
        self.assertEqual(plan["mode"], "plan")
        self.assertEqual(self.tools.calls, [])
        self.assertEqual(before, sorted(self.root.rglob("*")))

    def test_run_and_resume_preserve_identity_and_citations(self):
        first = self.pipeline()
        self.assertEqual(first.run()["status"], "complete")
        self.assertEqual(len(first.manifest["files"]), 2)
        self.assertEqual(len(first.manifest["files"][0]["members"]), 2)
        self.assertEqual(first.state["queries_attempted"], 2)
        before = [self.count("zpm", "export"), self.count("notebooklm", "create"), self.count("notebooklm", "add-drive"), self.count("notebooklm", "ask")]
        self.pipeline().run()
        self.assertEqual(before, [self.count("zpm", "export"), self.count("notebooklm", "create"), self.count("notebooklm", "add-drive"), self.count("notebooklm", "ask")])
        self.assertEqual(before, [1, 2, 2, 2])
        written = "\n".join(path.read_text() for path in first.root.rglob("*.json") if "export" not in path.parts)
        self.assertNotIn("SECRET", written)
        self.assertNotIn("/PRIVATE/PATH", written)
        self.assertIn("Original passage", written)
        self.assertIn("generated and unverified", (first.root / "REPORT.md").read_text())
        self.assertEqual(bulk.read_json(first.root / "coverage.json")["papers_fully_read"], 0)
        for args in self.tools.calls:
            self.assertNotIn("--new", args)
            self.assertNotIn("sync", args)
            self.assertNotIn("--overwrite", args)
            if "ask" in args:
                self.assertIn("--prompt-file", args)
                self.assertIn("-s", args)
                self.assertIn("-n", args)
            if "copy" in args:
                self.assertIn("--immutable", args)

    def test_unknown_create_and_import_reconcile(self):
        for failure in ("create", "create-json", "add-drive"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as directory:
                settings = bulk.load_config(self.settings_file)
                settings["run_dir"] = str(Path(directory) / "run")
                tools = FakeTools()
                tools.fail = failure
                with self.assertRaises(bulk.Stop):
                    bulk.Pipeline(settings, tools).run()
                result = bulk.Pipeline(settings, tools)
                result.run()
                self.assertEqual(len(tools.notebooks), 2)
                self.assertEqual(sum(len(s) for s in tools.sources.values()), 2)

    def test_completed_outputs_must_still_match_saved_hashes(self):
        for filename, count_field in (("F0001.text.json", "indexed_sources_saved"),
                                      ("batch-001.answer.json", "batch_answers_saved")):
            for change in ("delete", "corrupt"):
                with self.subTest(filename=filename, change=change), tempfile.TemporaryDirectory() as directory:
                    settings = bulk.load_config(self.settings_file)
                    settings["run_dir"] = str(Path(directory) / "run")
                    tools = FakeTools()
                    pipeline = bulk.Pipeline(settings, tools)
                    pipeline.run()
                    path = pipeline.root / "outputs" / filename
                    if change == "delete":
                        path.unlink()
                    else:
                        path.write_text("invalid JSON")
                    calls = len(tools.calls)
                    with self.assertRaisesRegex(bulk.Stop, "Saved .* changed"):
                        bulk.Pipeline(settings, tools).run()
                    self.assertFalse(any(args[1] in ("create", "ask") or args[1:3] == ["source", "add-drive"]
                                         for args in tools.calls[calls:]))
                    self.assertEqual(bulk.read_json(pipeline.root / "coverage.json")[count_field], 1)
                    self.assertIn("Run state: stopped", (pipeline.root / "REPORT.md").read_text())
                    if change == "delete":
                        self.assertFalse(path.exists())
                    else:
                        self.assertEqual(path.read_text(), "invalid JSON")

    def test_blank_answer_stops_without_repeating_query(self):
        def runner(args, **kwargs):
            result = self.tools(args, **kwargs)
            if args[1] == "ask":
                return self.tools.reply(args, {"answer": " \n\t", "references": []})
            return result
        settings = bulk.load_config(self.settings_file)
        with self.assertRaisesRegex(bulk.Stop, "answer"):
            bulk.Pipeline(settings, runner).run()
        self.assertEqual(self.count("notebooklm", "ask"), 1)
        self.assertEqual(bulk.read_json(self.pipeline().root / "state.json")["status"], "stopped")
        with self.assertRaisesRegex(bulk.Stop, "unconfirmed"):
            bulk.Pipeline(settings, runner).run()
        self.assertEqual(self.count("notebooklm", "ask"), 1)
        bulk.Pipeline.validate_answer({"answer": "No relevant evidence was found.", "references": []}, [])

    def test_unknown_write_without_match_never_retries(self):
        self.tools.fail = "create"
        pipeline = self.pipeline()
        with self.assertRaises(bulk.Stop):
            pipeline.run()
        self.tools.notebooks = []
        with self.assertRaisesRegex(bulk.Stop, "unconfirmed"):
            self.pipeline().run()
        self.assertEqual(self.count("notebooklm", "create"), 1)

    def test_timeout_blocks_question_then_resumes(self):
        self.tools.wait_timeout = True
        with self.assertRaises(bulk.Stop):
            self.pipeline().run()
        self.assertEqual(self.count("notebooklm", "ask"), 0)
        self.tools.wait_timeout = False
        self.pipeline().run()
        self.assertEqual(self.count("notebooklm", "add-drive"), 2)

    def test_response_file_crash_resumes_without_repeating_write_or_query(self):
        for suffix in (".text.json", ".answer.json"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as directory:
                settings = bulk.load_config(self.settings_file)
                settings["run_dir"] = str(Path(directory) / "run")
                tools = FakeTools()
                original = bulk.save_json
                def interrupted_save(path, value, exclusive=False):
                    original(path, value, exclusive=exclusive)
                    if path.name.endswith(suffix):
                        raise KeyboardInterrupt("Simulated crash after response write")
                with patch.object(bulk, "save_json", interrupted_save):
                    with self.assertRaises(KeyboardInterrupt):
                        bulk.Pipeline(settings, tools).run()
                bulk.Pipeline(settings, tools).run()
                self.assertEqual(sum(args[1] == "create" for args in tools.calls), 2)
                self.assertEqual(sum(args[1] == "ask" for args in tools.calls), 2)
                self.assertEqual(sum(args[1:3] == ["source", "fulltext"] for args in tools.calls), 2)

    def test_changed_remote_bytes_stop_resume_before_more_imports(self):
        self.tools.wait_timeout = True
        with self.assertRaises(bulk.Stop):
            self.pipeline().run()
        calls = len(self.tools.calls)
        self.tools.remote_changed = True
        self.tools.wait_timeout = False
        with self.assertRaises(bulk.Stop):
            self.pipeline().run()
        recent = self.tools.calls[calls:]
        self.assertTrue(any(args[:2] == ["rclone", "check"] for args in recent))
        self.assertFalse(any(args[1:3] == ["source", "add-drive"] or args[1] == "ask" for args in recent))

    def test_unknown_saved_state_shape_stops(self):
        root = self.pipeline().root
        root.mkdir()
        (root / "state.json").write_text("[]")
        with self.assertRaisesRegex(bulk.Stop, "saved state"):
            self.pipeline().run()

    def test_degraded_drive_blocks_question(self):
        self.tools.degraded = True
        with self.assertRaisesRegex(bulk.Stop, "access"):
            self.pipeline().run()
        self.assertEqual(self.count("notebooklm", "ask"), 0)

    def test_unknown_query_is_counted_and_not_repeated(self):
        self.tools.fail = "ask"
        with self.assertRaises(bulk.Stop):
            self.pipeline().run()
        with self.assertRaisesRegex(bulk.Stop, "unconfirmed"):
            self.pipeline().run()
        self.assertEqual(self.count("notebooklm", "ask"), 1)
        self.assertEqual(bulk.read_json(self.pipeline().root / "state.json")["queries_attempted"], 1)

    def test_small_query_budget_stops_before_remote_writes(self):
        self.settings["max_queries"] = 1
        self.settings_file.write_text(json.dumps(self.settings))
        with self.assertRaisesRegex(bulk.Stop, "queries"):
            self.pipeline().run()
        self.assertEqual(self.count("rclone", "copy"), 0)
        self.assertTrue((self.pipeline().root / "manifest.json").is_file())

    def test_changed_config_or_snapshot_rejected(self):
        pipeline = self.pipeline()
        pipeline.run()
        calls = self.count("notebooklm", "ask")
        self.settings["question"] = "A different question"
        self.settings_file.write_text(json.dumps(self.settings))
        with self.assertRaisesRegex(bulk.Stop, "Settings changed"):
            self.pipeline().run()
        self.settings["question"] = "Which evidence supports the method?"
        self.settings_file.write_text(json.dumps(self.settings))
        (pipeline.root / pipeline.manifest["workspace"] / pipeline.manifest["files"][0]["path"]).write_bytes(b"%PDF-changed")
        with self.assertRaisesRegex(bulk.Stop, "hash"):
            self.pipeline().run()
        self.assertEqual(calls, self.count("notebooklm", "ask"))

    def test_traversal_and_symlink_rejected(self):
        def traversal(entries, root):
            entries[0]["destination_path"] = "../escaped.pdf"
        self.tools.export_entries = traversal
        with self.assertRaisesRegex(bulk.Stop, "path"):
            self.pipeline().run()
        self.assertEqual(self.count("rclone", "copy"), 0)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.pdf"
            target.write_bytes(b"%PDF-data")
            (root / "link.pdf").symlink_to(target)
            with self.assertRaisesRegex(bulk.Stop, "symbolic"):
                bulk.safe_file(root, "link.pdf")

    def test_duplicate_drive_path_rejected(self):
        self.tools.drive = [{"Path": "collection-0/paper.pdf", "ID": "id1"}, {"Path": "collection-0/paper.pdf", "ID": "id2"}]
        with self.assertRaisesRegex(bulk.Stop, "duplicate"):
            self.pipeline().run()
        self.assertEqual(self.count("notebooklm", "create"), 0)

    def test_auth_or_version_failure_has_no_local_or_remote_mutation(self):
        for version, auth in (("0.8.4", True), ("0.8.5", False)):
            self.tools.version, self.tools.auth = version, auth
            with self.assertRaises(bulk.Stop):
                self.pipeline().run()
            self.assertFalse(self.pipeline().root.exists())
            self.assertEqual(self.count("zpm", "export"), 0)

    def test_run_cannot_write_into_portable_skill(self):
        self.settings["run_dir"] = str(SCRIPT.parent / "private-run")
        self.settings_file.write_text(json.dumps(self.settings))
        with self.assertRaisesRegex(bulk.Stop, "outside"):
            bulk.load_config(self.settings_file)


if __name__ == "__main__":
    unittest.main()
