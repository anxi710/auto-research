"""Offline metadata and isolated-copy checks for the optional writing skill."""
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

from test_package import destinations, anchors, SEMVER, scalar

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'research-report'


class ResearchReportPackageTests(unittest.TestCase):
    def test_metadata_and_ui_are_consistent(self):
        text = (SKILL / 'SKILL.md').read_text()
        header = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.DOTALL)
        self.assertIsNotNone(header)
        fields = dict(re.findall(r'(?m)^(name|description):\s*([^\n]+)$', header[1]))
        self.assertEqual(fields['name'], SKILL.name)
        self.assertTrue(fields['description'].strip())
        version = re.search(r'(?m)^metadata:\n  version:\s*([^\n]+)$', header[1])
        self.assertIsNotNone(version)
        self.assertRegex(scalar(version[1]), '^' + SEMVER.pattern + '$')
        ui = (SKILL / 'agents' / 'openai.yaml').read_text()
        prompt = re.search(r'(?m)^  default_prompt:\s*"([^\n]+)"$', ui)
        self.assertIsNotNone(prompt)
        self.assertIn('$' + SKILL.name, prompt[1])
        short = re.search(r'(?m)^  short_description:\s*"([^\n]+)"$', ui)
        self.assertIsNotNone(short)
        self.assertTrue(25 <= len(short[1]) <= 64)

    def test_standalone_copy_resolves_its_own_links(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / SKILL.name
            shutil.copytree(SKILL, copied)
            for source in copied.rglob('*.md'):
                for line, destination in destinations(source.read_text()):
                    with self.subTest(file=source.name, line=line):
                        url = urlsplit(destination)
                        if url.scheme or url.netloc:
                            continue
                        target = (source.parent / unquote(url.path)).resolve() if url.path else source.resolve()
                        self.assertTrue(target.is_relative_to(copied.resolve()))
                        self.assertTrue(target.exists(), destination)
                        if url.fragment and target.suffix.lower() == '.md':
                            self.assertIn(unquote(url.fragment), anchors(target.read_text()))

    def test_standalone_copy_preserves_its_license(self):
        self.assertEqual((SKILL / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())


if __name__ == '__main__':
    unittest.main()
