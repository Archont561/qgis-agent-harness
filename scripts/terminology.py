"""The label vocabulary: one letter means one thing, and the check says which.

Four families of labels circulate in this repository and three of them once used the same letter:
`N1` and `N4` are the two catalogue conditions, the enforcement ladder is numbered `L0`-`L5`, the
ranked contributions are `C1`-`C6`, and the field currents in chapter 1 are `F1`-`F6`. A reader who
meets a stray N label cannot tell from the letters alone whether it is a rung, a contribution or a
current, which is why the collision was renamed rather than tolerated.

What this script promises, and each promise is tested in `scripts/tests/test_terminology.py`:

  1. `N1` and `N4` are the only N-numbered labels in the checked tree; any other N number is a
     stale label from a retired numbering.
  2. A label bound to a ladder rung reads `L1 / N1` or `L4 / N4`, and the pair agrees: `L4 / N1` and
     `L2 / N2` both fail, because only two rungs have a condition attached.
  3. `C` labels stay inside `C1`-`C6`, the ranked contributions - a `C7` is a typo or an unwritten
     promise, and both are worth stopping.
  4. `F` labels stay inside `F1`-`F6`, the field currents of chapter 1.
  5. A quoted label is allowed when the line, or the heading it sits under, says it is retired,
     pruned, renamed or superseded - and a file whose front matter freezes it is skipped entirely.
     That is how `gap-and-literature.md` §10 keeps the record of what the old numbering was.
  6. Usage: `python3 scripts/terminology.py [PATH ...]`; with no arguments the repository is walked.
     A path that does not exist exits 2, so a renamed file cannot silently stop being checked.

Exempt trees are declared here with a reason, the same convention `repo_facts.py` uses: a listing of
what the retired numbering was is a record, not a defect, and verbatim literature is not ours.

Usage: python3 scripts/terminology.py [PATH ...]
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path.cwd()

EXEMPT = {
    "backlog/": "work records managed by the Backlog.md CLI: historical by construction",
    "thesis/literature/": "sources: transcripts quote whatever the paper, benchmark or note said",
    ".agents/": "vendored skills, pinned by skills-lock.json",
}

CONDITIONS = {"1", "4"}
RUNGS = {"1", "4"}  # only the two rungs that are also conditions
CONTRIBUTIONS = 6
CURRENTS = 6

# Written on the line, or on the heading the line sits under. Only words that name the retirement
# itself: "old" or "earlier" would excuse half the thesis.
MARKED = re.compile(
    r"retir|prun|renam|replac|supersed|no longer|was cut|withdrawn|abolish|dropped|deprecated",
    re.IGNORECASE,
)
FROZEN = re.compile(r"^status:\s*frozen\b", re.MULTILINE)

N_LABEL = re.compile(r"\bN(\d)\b")
RUNG_BINDING = re.compile(r"\bL(\d)\s*/\s*N(\d)\b")
C_LABEL = re.compile(r"\bC(\d)\b")
F_LABEL = re.compile(r"\bF(\d)\b")


def _rel(path: pathlib.Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _exempt(path: pathlib.Path) -> bool:
    return any(_rel(path).startswith(prefix) for prefix in EXEMPT)


def _is_frozen(text: str) -> bool:
    if not text.startswith("---"):
        return False
    front = text.split("---", 2)
    return len(front) > 2 and bool(FROZEN.search(front[1]))


def _in_fence(text: str) -> set[int]:
    """Line numbers inside a fenced block: code samples spell labels legitimately, and `N4` inside a
    LaTeX snippet is a subscript, not a claim about a condition."""
    inside: set[int] = set()
    opened = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            opened = not opened
            inside.add(number)
            continue
        if opened:
            inside.add(number)
    return inside


def check(path: pathlib.Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    if _is_frozen(text):
        return problems
    where = _rel(path)
    fences = _in_fence(text)
    heading = ""
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("#"):
            heading = line
        if number in fences:
            continue
        excused = bool(MARKED.search(line) or MARKED.search(heading))

        for match in N_LABEL.finditer(line):
            if match.group(1) not in CONDITIONS and not excused:
                problems.append(
                    f"{where}:{number}: `N{match.group(1)}` - N1 and N4 are the only N labels; "
                    "contributions are C1-C6, currents F1-F6, rungs L0-L5"
                )

        for match in RUNG_BINDING.finditer(line):
            rung, condition = match.group(1), match.group(2)
            if rung not in RUNGS or rung != condition:
                problems.append(
                    f"{where}:{number}: `L{rung} / N{condition}` - only `L1 / N1` and `L4 / N4` "
                    "bind a rung to a condition, and the numbers have to agree"
                )

        for match in C_LABEL.finditer(line):
            if int(match.group(1)) > CONTRIBUTIONS and not excused:
                problems.append(
                    f"{where}:{number}: `C{match.group(1)}` - six ranked contributions, C1-C6"
                )

        for match in F_LABEL.finditer(line):
            if int(match.group(1)) > CURRENTS and not excused:
                problems.append(
                    f"{where}:{number}: `F{match.group(1)}` - six field currents, F1-F6"
                )
    return problems


def _walk() -> list[pathlib.Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part.startswith(".") or part == "node_modules" for part in path.parts)
        and not _exempt(path)
    )


def main(argv: list[str]) -> int:
    targets: list[pathlib.Path] = []
    for argument in argv[1:]:
        path = pathlib.Path(argument)
        if not path.exists():
            print(
                f"{argument}: missing - the vocabulary cannot be checked on a file that is gone",
                file=sys.stderr,
            )
            return 2
        targets.append(path)

    problems: list[str] = []
    for path in targets or _walk():
        if path.is_dir():
            problems.extend(_flat(check(child) for child in sorted(path.rglob("*.md"))))
        else:
            problems.extend(check(path))

    for problem in problems:
        print(problem)
    return 1 if problems else 0


def _flat(groups) -> list[str]:
    return [problem for group in groups for problem in group]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
