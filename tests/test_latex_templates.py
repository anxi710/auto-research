"""Offline integrity checks for the redistributed third-party template subset."""
from pathlib import Path
import hashlib
import json
import unittest

CATALOG = Path(__file__).resolve().parents[1] / 'templates' / 'latex'


class LatexTemplateIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((CATALOG / 'manifest.json').read_text())

    def test_upstream_bytes_match_the_manifest(self):
        for project in self.manifest['projects']:
            for entry in project['files']:
                with self.subTest(path=entry['path']):
                    path = CATALOG / entry['path']
                    self.assertTrue(path.resolve().is_relative_to(CATALOG.resolve()))
                    content = path.read_bytes()
                    self.assertEqual(len(content), entry['size_bytes'])
                    self.assertEqual(hashlib.sha256(content).hexdigest(), entry['sha256'])
                    self.assertTrue(entry['upstream_bytes_unchanged'])

    def test_all_vendor_files_have_provenance_or_a_packaging_notice(self):
        tracked = {entry['path'] for project in self.manifest['projects'] for entry in project['files']}
        notices = {project['notice'] for project in self.manifest['projects']}
        actual = {str(p.relative_to(CATALOG)) for p in (CATALOG / 'vendor').rglob('*') if p.is_file()}
        self.assertEqual(actual, tracked | notices)

    def test_every_template_preserves_full_license_and_recovery_information(self):
        for project in self.manifest['projects']:
            with self.subTest(project=project['name']):
                self.assertEqual(project['license'], 'LPPL-1.3c-or-later')
                licenses = [entry for entry in project['files'] if Path(entry['path']).name.lower() == 'license']
                self.assertEqual(len(licenses), 1)
                text = (CATALOG / licenses[0]['path']).read_text()
                self.assertIn('LPPL Version 1.3c', text)
                self.assertIn('CONDITIONS ON DISTRIBUTION AND MODIFICATION', text)
                self.assertIn('MAINTENANCE OF THE WORK', text)
                notice = (CATALOG / project['notice']).read_text()
                self.assertIn(project['commit'], notice)
                self.assertIn(project['immutable_source_archive'], notice)
                for omitted in project['omitted_archive_members']:
                    self.assertIn(omitted, notice)


if __name__ == '__main__':
    unittest.main()
