#!/usr/bin/env python3
"""Check a repository's README and CONTRIBUTING against the house markdown style.

The conventions are the ones every Archont561 repository already follows, read off `skills`,
`qgis-sdk`, `ODM-conda`, `universe`, `pixi-sandbox`, `clifacet` and `playtest`. They are structural
on purpose: what a document *says* belongs to Vale, what it *is shaped like* belongs here, because
shape is the part that silently drifts when a README is edited six months later.

Three modes, and the split is deliberate: the invariants hold in **every** repository under this
account, while the skeleton describes the shape the newest ones settled on. A rule that six of seven
repositories fail is an opinion, not a convention, so it is opt-in:

  1. `invariants` — one H1 on line 1, no skipped heading levels, no punctuation at the end of a
     heading, no emoji, tagged fences from a known vocabulary (a MyST `{note}` counts: the fence is
     named by its directive), `alt` on every badge, an alignment row under every table header,
     `## License` last and spelled the American way;
  2. `skeleton` — the README shape of `qgis-sdk` and `skills`: a centred `<p align="center">` badge
     block, a bold tagline and a `> Status:` line above the first `##`, then `Try it` → `Develop` →
     `Documentation` → `License`;
  3. `contributing` — one H1 reading `# Contributing to <repository>`, then `Environment` →
     `Commands` → `Commits`, with a command table that gives every command a purpose.

`readme` runs 1 and 2 together, which is what a repository that adopts the skeleton wants.

Shared checks, because they are what a diff notices: every `<img>` carries `alt`, every table has an
alignment row, every fence names its language, headings carry no trailing punctuation, no emoji, no
tab-indented bullets, and no heading skips a level.

Usage: python3 scripts/house_style.py {invariants,skeleton,readme,contributing} PATH

alint passes `{path}`. Exit 0 when the document holds the shape, 1 with one line per violation; each
line names the line number the way a compiler would, so the fix is a jump and not a search.
"""

from __future__ import annotations

import pathlib
import re
import sys

SHELL_FENCES = {"sh", "bash", "console", "shell", "zsh"}
# A MyST page's fences are not all code: ```{note} opens an admonition, `{figure}` a figure, and
# the directive's name is what the fence is tagged with. A fence is *named* here, in other words,
# even though the name is not a language — which is the property the rule is actually after.
MYST_DIRECTIVE = re.compile(r"^\{[a-z][a-z0-9_+-]*\}$")
FENCE_LANGUAGES = SHELL_FENCES | {
    "text", "yaml", "toml", "json", "python", "py", "ts", "tsx", "js", "rust", "sql", "diff", "ini",
    "markdown", "md", "csv", "gherkin", "dockerfile", "mermaid", "xml", "html", "css", "powershell",
}
# Decorative pictographs are forbidden; typographic marks that carry data are not. A check mark in a
# table of required fields is typography — banning it would push real tables into ```text blocks to
# satisfy a linter, which is worse than the emoji.
ALLOWED_MARKS = "✓✔✗✘☑☐▲△▽▼●○■□★☆→←↑↓⇒⇔·•…"
EMOJI = re.compile(
    "[\U0001f300-\U0001faff\U00002600-\U000027bf\U0001f000-\U0001f2ff\U0000fe0f\U00002b00-\U00002bff]"
)
BADGE_IMG = re.compile(r"<img\s+[^>]*src=", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
ALIGNMENT_ROW = re.compile(r"^\s*\|(\s*:?-{2,}:?\s*\|)+\s*$")

README_SECTIONS = ["Try it", "Develop", "Documentation", "License"]
CONTRIBUTING_SECTIONS = ["Environment", "Commands", "Commits"]


def _at(path: pathlib.Path, number: int, message: str) -> str:
    """One violation, formatted the way a compiler does: `file:line: what is wrong`."""
    return f"{path}:{number}: {message}"


class Document:
    """A markdown file as the checks need to see it: lines, headings and fenced blocks."""

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.lines = path.read_text(encoding="utf-8").splitlines()
        self.start = self._content_start()
        self.fences = self._scan_fences()

    def _content_start(self) -> int:
        """The line the document proper begins on: 1, or the first line after a closing `---`."""
        start = 1
        if self.lines and self.lines[0].strip() == "---":
            for number, line in enumerate(self.lines[1:], 2):
                if line.strip() in {"---", "..."}:
                    start = number + 1
                    break
        while start <= len(self.lines) and not self.lines[start - 1].strip():
            start += 1
        return start

    def _scan_fences(self) -> list[tuple[int, str, int]]:
        """Every fenced block as `(first line, language, last line)`, 1-based and inclusive."""
        blocks: list[tuple[int, str, int]] = []
        opening: tuple[int, str] | None = None
        for number, line in enumerate(self.lines, 1):
            stripped = line.lstrip()
            if not stripped.startswith("```"):
                continue
            if opening is None:
                opening = (number, stripped[3:].strip().split(" ")[0].lower())
            else:
                blocks.append((opening[0], opening[1], number))
                opening = None
        if opening is not None:
            blocks.append((opening[0], opening[1], len(self.lines)))
        return blocks

    def in_fence(self, number: int) -> bool:
        return any(first <= number <= last for first, _, last in self.fences)

    def headings(self) -> list[tuple[int, int, str]]:
        """`(line number, level, text)` for every ATX heading outside a fence."""
        found = []
        for number, line in enumerate(self.lines, 1):
            if self.in_fence(number):
                continue
            match = HEADING.match(line)
            if match:
                found.append((number, len(match.group(1)), match.group(2)))
        return found

    def h1(self) -> tuple[int, str] | None:
        for number, level, text in self.headings():
            if level == 1:
                return number, text
        return None

    def section(self, name: str) -> tuple[int, str] | None:
        """The first `##` heading whose text matches `name`, case-insensitively."""
        for number, level, text in self.headings():
            if level == 2 and text.strip().lower() == name.lower():
                return number, text
        return None

    def preamble(self) -> list[tuple[int, str]]:
        """Everything before the first `##` heading — where tagline, badges and status belong."""
        first = next((n for n, level, _ in self.headings() if level == 2), len(self.lines) + 1)
        return [(n, self.lines[n - 1]) for n in range(1, first)]


def check_shared(doc: Document) -> list[str]:
    problems: list[str] = []
    where = doc.path

    h1 = doc.h1()
    if h1 is None:
        problems.append(f"{where}:{doc.start}: there is no H1 — every document opens with one")
    elif h1[0] != doc.start:
        problems.append(f"{where}:{h1[0]}: the H1 is on line {h1[0]}, not line {max(doc.start, 1)}")

    levels = doc.headings()
    if levels:
        levels = [(1, levels[0][1])] + [
            (levels[i][0], levels[i][1]) for i in range(1, len(levels))
        ]
        previous = 0
        for number, level, text in doc.headings():
            if previous and level > previous + 1:
                problems.append(
                    _at(
                        where,
                        number,
                        f"'{text}' is h{level} under h{previous} — a heading may not skip a level",
                    )
                )
            previous = level

    for number, _level, text in doc.headings():
        if text.endswith((".", ":", ";", "!", "?")):
            problems.append(
                _at(where, number, f"heading '{text}' ends with punctuation — headings do not")
            )

    for number, line in enumerate(doc.lines, 1):
        if doc.in_fence(number):
            continue
        if EMOJI.search(line.translate({ord(mark): None for mark in ALLOWED_MARKS})):
            problems.append(f"{where}:{number}: emoji — the house style spells it out or drops it")
        if line.startswith("\t"):
            problems.append(f"{where}:{number}: a tab-indented line — bullets and code use spaces")

    for first, language, _close in doc.fences:
        if not language:
            problems.append(
                _at(
                    where,
                    first,
                    "fence with no language — name it (`sh`, `text`, `yaml`) so it reads as code",
                )
            )
        elif language not in FENCE_LANGUAGES and not MYST_DIRECTIVE.match(language):
            problems.append(
                _at(
                    where,
                    first,
                    f"unknown fence language '{language}' — the vocabulary is "
                    + ", ".join(sorted(FENCE_LANGUAGES)),
                )
            )

    for number, line in enumerate(doc.lines, 1):
        if "<img" in line.lower() and not re.search(r"\balt\s*=", line, re.I):
            problems.append(
                _at(where, number, "<img> without alt — a badge is an image with a name")
            )

    for number, line in enumerate(doc.lines, 1):
        if not TABLE_ROW.match(line) or doc.in_fence(number):
            continue
        previous = doc.lines[number - 2] if number >= 2 else ""
        if TABLE_ROW.match(previous):  # a body row, not the header of a table
            continue
        following = doc.lines[number] if number < len(doc.lines) else ""
        if not ALIGNMENT_ROW.match(following):
            problems.append(
                _at(
                    where,
                    number,
                    "table header without an alignment row — add `| :-- | :-- |` under it",
                )
            )

    return problems


def _bold_paragraph(preamble: list[tuple[int, str]]) -> int | None:
    """The line number of a paragraph that opens and closes with `**` — a tagline may wrap."""
    block: list[tuple[int, str]] = []
    for number, line in [*preamble, (0, "")]:
        if line.strip():
            block.append((number, line))
            continue
        if block:
            first, last = block[0][1].strip(), block[-1][1].strip()
            if first.startswith("**") and last.endswith("**") and len(block) <= 4:
                return block[0][0]
            block = []
    return None


def check_skeleton(doc: Document) -> list[str]:
    problems = check_shared(doc)
    where = doc.path
    preamble = doc.preamble()

    badge_line = next((n for n, line in preamble if '<p align="center">' in line), None)
    if badge_line is None:
        problems.append(
            _at(
                where,
                1,
                'no `<p align="center">` badge block — the badges go above the tagline, centred',
            )
        )
    elif not any(BADGE_IMG.search(line) for _, line in preamble):
        problems.append(_at(where, badge_line, "the badge block holds no badge"))

    if _bold_paragraph(preamble) is None:
        problems.append(
            _at(where, 1, "no bold tagline — one bold sentence, above the first `##`, what this is")
        )

    status = None
    for number, line in preamble:
        stripped = line.strip().lower()
        if stripped.startswith("> status:") or stripped.startswith("**status:**"):
            status = number
            break
    if status is None:
        problems.append(
            _at(
                where, 1, "no status line — `> Status: …` above the first `##`, what does not exist"
            )
        )

    order: list[int] = []
    for name in README_SECTIONS:
        found = doc.section(name)
        if found is None:
            problems.append(
                _at(
                    where,
                    1,
                    f"no `## {name}` section — the shape ends {', '.join(README_SECTIONS)}",
                )
            )
        else:
            order.append(found[0])

    if order and order != sorted(order):
        problems.append(
            _at(where, 1, f"the sections are out of order — {', '.join(README_SECTIONS)}")
        )
        return problems

    license_heading = doc.section("License")
    if license_heading is not None:
        after = [
            (number, text)
            for number, level, text in doc.headings()
            if level == 2 and number > license_heading[0]
        ]
        if after:
            problems.append(
                _at(
                    where,
                    after[0][0],
                    f"`## {after[0][1]}` follows `## License` — the licence is the last section",
                )
            )

    return problems


def check_invariants(doc: Document) -> list[str]:
    problems = check_shared(doc)
    where = doc.path

    for name in ("License", "Licence", "licence", "license"):
        found = doc.section(name)
        if found and found[1] != "License":
            problems.append(
                _at(
                    where,
                    found[0],
                    f"`## {found[1]}` — the heading is `License`, as in every other repository",
                )
            )

    license_heading = doc.section("License")
    if license_heading is not None:
        after = [
            (number, text)
            for number, level, text in doc.headings()
            if level == 2 and number > license_heading[0]
        ]
        if after:
            problems.append(
                _at(
                    where,
                    after[0][0],
                    f"`## {after[0][1]}` follows `## License` — the licence is the last section",
                )
            )

    return problems


def check_readme(doc: Document) -> list[str]:
    """The skeleton implies the invariants, so a repository that adopts it runs one rule only."""
    return check_skeleton(doc)


def check_contributing(doc: Document) -> list[str]:
    problems = check_shared(doc)
    where = doc.path

    h1 = doc.h1()
    if h1 is not None and not h1[1].lower().startswith("contributing to "):
        problems.append(
            _at(where, h1[0], f"the H1 is '{h1[1]}' — it reads `# Contributing to <repository>`")
        )

    positions: dict[str, int] = {}
    for name in CONTRIBUTING_SECTIONS:
        found = doc.section(name)
        if found is None:
            problems.append(
                _at(
                    where,
                    1,
                    f"no `## {name}` section — the loop is {', '.join(CONTRIBUTING_SECTIONS)}",
                )
            )
        else:
            positions[name] = found[0]
    if len(positions) == len(CONTRIBUTING_SECTIONS) and list(positions.values()) != sorted(
        positions.values()
    ):
        problems.append(
            _at(where, 1, f"the sections are out of order — {', '.join(CONTRIBUTING_SECTIONS)}")
        )

    commands = doc.section("Commands")
    if commands is not None:
        window = [
            doc.lines[n - 1]
            for n in range(commands[0], min(commands[0] + 12, len(doc.lines) + 1))
        ]
        if not any(TABLE_ROW.match(line) for line in window):
            problems.append(
                _at(
                    where,
                    commands[0],
                    "`## Commands` carries no table — every command needs a purpose beside it",
                )
            )

    return problems


CHECKS = {
    "invariants": check_invariants,
    "skeleton": check_skeleton,
    "readme": check_readme,
    "contributing": check_contributing,
}


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in CHECKS:
        print(f"usage: house_style.py {{{','.join(CHECKS)}}} PATH", file=sys.stderr)
        return 2

    path = pathlib.Path(argv[2])
    if not path.is_file():
        print(f"{path}: missing", file=sys.stderr)
        return 2

    problems = CHECKS[argv[1]](Document(path))
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
