"""Offline checks for this package's inline Markdown and simple frontmatter."""

from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = "skills/research-workflow/SKILL.md"
ROOT_DOCS = ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONTRIBUTING.md", "README.md", "README.zh-CN.md")
DOC_DIRS = ("docs", "skills/research-workflow", "tests", "changes", "examples")
DESTINATION = re.compile(r'\]\((<[^>\n]*>|[^\s()]*)(?:\s+(?:"[^"\n]*"|\'[^\'\n]*\'))?\)')
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.*?)\1(?!`)", re.DOTALL)
NUMBER = r"(?:0|[1-9][0-9]*)"
PRE = rf"(?:{NUMBER}|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER = re.compile(rf"{NUMBER}\.{NUMBER}\.{NUMBER}(?:-{PRE}(?:\.{PRE})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?")


def read(root, path, errors, binary=False):
    try:
        path.resolve().relative_to(root.resolve())
        return path.read_bytes() if binary else path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"{path.relative_to(root)}: cannot read inside package: {error}")
        return b"" if binary else ""


def without_fences(text):
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            lines.append("\n")
        elif marker:
            fence = marker[1]
            lines.append("\n")
        else:
            lines.append(line)
    return "".join(lines)


def prose(text):
    return INLINE_CODE.sub(lambda match: "\n" * match[0].count("\n"), without_fences(text))


def destinations(text):
    text = prose(text)
    for match in DESTINATION.finditer(text):
        yield text.count("\n", 0, match.start()) + 1, match[1].strip("<>")


def anchors(text):
    used = set()
    for line in without_fences(text).splitlines():
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not heading:
            continue
        title = INLINE_CODE.sub(lambda match: match[2], heading[1])
        title = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", title)
        slug = re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-")
        anchor, suffix = slug, 0
        while anchor in used:
            suffix += 1
            anchor = f"{slug}-{suffix}"
        used.add(anchor)
    return used


def check_links(root):
    errors = []
    documents = {root / name for name in ROOT_DOCS}
    for directory in DOC_DIRS:
        documents.update((root / directory).rglob("*.md"))
    for source in sorted(documents):
        text = read(root, source, errors)
        for line, destination in destinations(text):
            where = f"{source.relative_to(root)}:{line}: {destination!r}"
            try:
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                target = (source.parent / unquote(url.path)).resolve() if url.path else source.resolve()
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{where}: path escapes package or has an invalid URL")
                continue
            if not target.exists():
                errors.append(f"{where}: target does not exist")
            elif url.fragment and target.suffix.lower() == ".md":
                if unquote(url.fragment) not in anchors(read(root, target, errors)):
                    errors.append(f"{where}: heading anchor does not exist")
    return errors


def check_entries(root):
    errors = []
    links = [destination for _, destination in destinations(read(root, root / "AGENTS.md", errors))]
    if not any(destination in (SKILL, "./" + SKILL) for destination in links):
        errors.append(f"AGENTS.md: add a link to the shared {SKILL}")
    for name in ("CLAUDE.md", "GEMINI.md"):
        text = prose(read(root, root / name, errors))
        if not re.search(r"(?m)^\s*@(?:\./)?AGENTS\.md\s*$", text):
            errors.append(f"{name}: import the root AGENTS.md")
    return errors


def scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].strip()
    return value


def check_metadata(root):
    errors = []
    text = read(root, root / SKILL, errors)
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not frontmatter:
        return errors + [f"{SKILL}: missing simple YAML frontmatter"]
    header = frontmatter[1]
    for name in ("name", "description"):
        values = re.findall(rf"(?m)^{name}:([^\n]*)$", header)
        if len(values) != 1 or not scalar(values[0]) or scalar(values[0]) in ("null", "~", "|", ">"):
            errors.append(f"{SKILL}: {name} needs one nonempty inline value")
    versions = re.findall(r"(?m)^metadata:\n  version:([^\n]*)$", header)
    if len(versions) != 1 or not SEMVER.fullmatch(scalar(versions[0])):
        return errors + [f"{SKILL}: metadata.version needs one semantic version"]
    version = scalar(versions[0])
    for name, label in (("README.md", "Version"), ("README.zh-CN.md", "版本")):
        text = prose(read(root, root / name, errors))
        badges = re.findall(rf"!\[{label} ([^\]]+)\]\((https://img\.shields\.io/badge/version-[^\s)]+)\)", text)
        display_version = version.split("-", 1)[0].split("+", 1)[0]
        expected = (display_version, f"https://img.shields.io/badge/version-{display_version}-blue")
        if badges != [expected]:
            errors.append(f"{name}: version badge label and image must display metadata.version core {display_version}")
    return errors


def check_licenses(root):
    errors = []
    original = read(root, root / "LICENSE", errors, binary=True)
    packaged = read(root, root / "skills/research-workflow/LICENSE", errors, binary=True)
    if original != packaged:
        errors.append("skills/research-workflow/LICENSE: bytes differ from root LICENSE")
    return errors


def check_package(root):
    return check_links(root) + check_entries(root) + check_metadata(root) + check_licenses(root)


class PackageTests(unittest.TestCase):
    def test_package(self):
        self.assertEqual(check_package(ROOT), [])


class PackageCheckTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in ROOT_DOCS:
            self.write(name, "# Start\n")
        self.write("AGENTS.md", f"[Read the skill]({SKILL}).\n")
        self.write("CLAUDE.md", "@AGENTS.md\n")
        self.write("GEMINI.md", "@./AGENTS.md\n")
        self.write(SKILL, '---\nname: research-workflow\ndescription: Read research records.\nmetadata:\n  version: "0.1.6"\n---\n# Skill\n')
        for name, label in (("README.md", "Version"), ("README.zh-CN.md", "版本")):
            self.write(name, f"[![{label} 0.1.6](https://img.shields.io/badge/version-0.1.6-blue)]({SKILL})\n")
        self.write("LICENSE", "Shared license bytes.\n")
        self.write("skills/research-workflow/LICENSE", "Shared license bytes.\n")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def replace(self, path, old, new):
        target = self.root / path
        self.write(path, target.read_text(encoding="utf-8").replace(old, new))

    def check(self, expected=None):
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        errors = check_package(self.root)
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after, "Package checks changed input files")
        if expected is None:
            self.assertEqual(errors, [])
        else:
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_links_unicode_duplicates_images_and_code_examples(self):
        self.write("docs/guide.md", "# 环境要求\n## Repeat\n## Repeat\n## Repeat-1\n## Repeat\n## A `code` name\n")
        self.write("docs/space name.md", "# Other\n")
        self.write("docs/image.svg", "<svg/>\n")
        self.write("CONTRIBUTING.md", "\n".join([
            "[Unicode](docs/guide.md#环境要求)", "[Encoded](docs/guide.md#%E7%8E%AF%E5%A2%83%E8%A6%81%E6%B1%82)",
            "[Repeat](docs/guide.md#repeat-1)", "[Collision](docs/guide.md#repeat-1-1)",
            "[Next](docs/guide.md#repeat-2)", "[Code](docs/guide.md#a-code-name)",
            '[Space](<docs/space name.md> "title")', "![Image](docs/image.svg)",
            "[Web](https://invalid.example/missing)", "[Mail](mailto:example@invalid.example)",
            "[Host](//invalid.example/missing)", "`[Example](missing.md)`", "``[Example](missing.md)``",
            "````markdown", "[Example](missing.md)", "```", "[Still code](missing.md)", "````",
            "~~~markdown", "[Example](missing.md)", "~~~",
        ]) + "\n")
        self.write("personal.md", "[Ignored](missing.md)\n")
        self.check()

    def test_missing_path_and_bad_fragment(self):
        self.write("docs/guide.md", "# Guide\n[Missing](absent.md)\n[Fragment](#absent)\n![Image](absent.png)\n")
        self.check("docs/guide.md:2: 'absent.md': target does not exist")
        self.check("heading anchor does not exist")
        self.write("examples/practice/README.md", "[Evidence](missing-evidence.json)\n")
        self.check("examples/practice/README.md:1: 'missing-evidence.json': target does not exist")

    def test_paths_cannot_escape_the_package(self):
        self.write("docs/guide.md", "[Outside](../../outside.md)\n")
        self.check("path escapes package")
        (self.root / "docs/escape").symlink_to(self.root.parent, target_is_directory=True)
        self.write("docs/guide.md", "[Outside](escape/outside.md)\n")
        self.check("path escapes package")

    def test_entry_imports_and_shared_skill_link_are_required(self):
        self.write("AGENTS.md", "`[Example](skills/research-workflow/SKILL.md)`\n")
        self.check("AGENTS.md: add a link")
        for name in ("CLAUDE.md", "GEMINI.md"):
            self.write(name, "```text\n@AGENTS.md\n```\n")
            self.check(f"{name}: import the root AGENTS.md")

    def test_metadata_is_required_and_has_valid_values(self):
        original = (self.root / SKILL).read_text(encoding="utf-8")
        for old, new, error in (
            ("---\n", "", "frontmatter"),
            ("name: research-workflow", 'name: ""', "name needs"),
            ("description: Read research records.", "description: null", "description needs"),
            ("  version:", "version:", "metadata.version"),
            ('"0.1.6"', '"01.1.6"', "metadata.version"),
            ('"0.1.6"', '"0.1.6-01"', "metadata.version"),
        ):
            with self.subTest(error=error, new=new):
                self.write(SKILL, original.replace(old, new))
                self.check(error)

    def test_each_badge_label_and_image_must_match(self):
        for name in ("README.md", "README.zh-CN.md"):
            original = (self.root / name).read_text(encoding="utf-8")
            for old, new in ((" 0.1.6]", " 0.1.5]"), ("version-0.1.6-", "version-0.1.5-")):
                with self.subTest(name=name, old=old):
                    self.write(name, original.replace(old, new))
                    self.check(f"{name}: version badge")
            self.write(name, original)

    def test_prerelease_badges_display_only_the_core_version(self):
        skill = (self.root / SKILL).read_text(encoding="utf-8")
        image = "https://img.shields.io/badge/version-0.1.10-blue"
        for version in ("0.1.10-dual-delivery.2", "0.1.10-rc.1+build.7", "0.1.10+build.7"):
            with self.subTest(version=version):
                self.write(SKILL, skill.replace('"0.1.6"', f'"{version}"'))
                for name, label in (("README.md", "Version"), ("README.zh-CN.md", "版本")):
                    self.write(name, f"[![{label} 0.1.10]({image})]({SKILL})\n")
                self.check()
        for name in ("README.md", "README.zh-CN.md"):
            original = (self.root / name).read_text(encoding="utf-8")
            for old, new in (
                (" 0.1.10]", " 0.1.10-dual-delivery.2]"),
                ("version-0.1.10-blue", "version-0.1.10--dual--delivery.2-blue"),
                ("version-0.1.10-blue", "version-0.1.10-dual-delivery.2-blue"),
                (" 0.1.10]", " 0.1.9]"),
                ("version-0.1.10-blue", "version-0.1.9-blue"),
            ):
                with self.subTest(name=name, old=old, new=new):
                    self.write(name, original.replace(old, new))
                    self.check(f"{name}: version badge")
                self.write(name, original)

    def test_license_bytes_and_required_files(self):
        self.write("skills/research-workflow/LICENSE", "Different license.\n")
        self.check("LICENSE: bytes differ")
        (self.root / "LICENSE").unlink()
        self.check("LICENSE: cannot read")


if __name__ == "__main__":
    unittest.main()
