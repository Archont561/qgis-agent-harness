#!/usr/bin/env python3
"""Check that the prose agrees with the tree it describes.

Four modes, each answering one class of drift this repository has produced at least once:

  counts    numeric claims ("20 tasks", "69 references", "# 40 rules") against the filesystem
  retired   words from the retired design generation, unless the sentence marks them as retired
  ids       backlog ids named in prose (`TASK-19`, `d-2`, `doc-8`, `m-1`) against `backlog/`
  coverage  every rule in .alint.yml lints at least one file, and every document we own is linted
  backlog   every task record: id, status, label, milestone, dependency and path it promises

Usage: python3 scripts/repo_facts.py {counts|retired|ids|coverage|backlog}

No PATH argument: the walker starts at the repository root (the current directory, which is what
alint gives a `command` rule). Exit status is 0 when nothing is wrong and 1 when something is, with
one `file:line: message` per problem on stdout.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path.cwd()

# The documents that state facts about this repository. Everything else may say what it likes.
INDEX_DOCS = ("README.md", "thesis/README.md")

# Exemptions are declared here with a reason, so that they appear in review instead of hiding in a
# path prefix. A tree listed here is not checked by any of the four modes.
EXEMPT = {
    "backlog/": "work records managed by the Backlog.md CLI: historical by construction",
    "thesis/literature/": "sources: transcripts and digests quote whatever the paper said",
    "thesis/writing/": "critique, defence and rehearsal notes argue against the retired design",
    ".agents/": "vendored skills, pinned by skills-lock.json",
}

# A rule is allowed to match nothing only while it is declared here, with the reason and a removal
# condition. If a sleeping rule starts matching, that is a problem too: the entry is now a lie.
SLEEPING = {
    "task-card-schema-cards": "no card files exist yet, and TASK-15 creates them",
    "bdd-feature-has-test": "no .feature file exists yet, and the rebuilt suite brings them",
}

# The rules that check links, backticked paths and fragments. Every document we own must be covered
# by their `paths`, or a document silently leaves the check the day someone adds a directory.
MARKDOWN_RULES = (
    "markdown-links-resolve",
    "markdown-paths-resolve",
    "markdown-fragments-resolve",
)

# ── shared ──────────────────────────────────────────────────────────────────────────────────────


def _glob(*parts: str) -> list[pathlib.Path]:
    return sorted(ROOT.glob("/".join(parts)))


def _rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _exempt(path: pathlib.Path) -> bool:
    return any(_rel(path).startswith(prefix) for prefix in EXEMPT)


def _walk_md() -> list[pathlib.Path]:
    return sorted(
        p
        for p in ROOT.rglob("*.md")
        if not any(part.startswith(".") or part == "node_modules" for part in p.parts)
        and not _exempt(p)
    )


# A line that dates itself or spans two numbers is a history row: it is allowed to be stale,
# because it is not describing the tree as it is now.
HISTORICAL = re.compile(r"→|\b\d{1,2} (?:XI|I{1,3}V?|X)\b|\b20\d\d-\d\d-\d\d\b")

WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}

# ── counts ──────────────────────────────────────────────────────────────────────────────────────


def _bib_entries() -> int:
    bib = ROOT / "thesis/literature/literature.bib"
    return len(re.findall(r"^@\w+\{", bib.read_text(encoding="utf-8"), re.MULTILINE))


def _alint_rules() -> int | None:
    """The rule count alint itself reports, not a grep of the config (a grep undercounts).

    Tried directly first, then through pixi, so the check also works when the script runs outside
    the `qa` environment — and says so rather than passing when neither route is available.
    """
    routes: list[list[str]] = []
    if exe := shutil.which("alint"):
        routes.append([exe, "validate-config"])
    if exe := shutil.which("pixi"):
        routes.append([exe, "run", "-e", "qa", "alint", "validate-config"])
    for route in routes:
        done = subprocess.run(route, capture_output=True, text=True, cwd=ROOT, check=False)
        match = re.search(r"(\d+) rule\(s\) loaded", done.stdout + done.stderr)
        if match:
            return int(match.group(1))
    return None


# (documents it applies to, claim pattern, what it counts, the count). Each noun is registered only
# where its meaning is fixed: "20 tasks" is the backlog in README.md, while thesis/README.md says
# "40 tasks" of the generation `d-2` replaced. A failure reads as the sentence it is about.
#
# This registry is explicit on purpose: a number nobody registered is not checked. Quote a new noun
# and the claim has to be added here — that is the one caveat of this mode, and it is cheap.
R = ("README.md",)
T = ("thesis/README.md",)
COUNTS = [
    (R, r"(\d+) tasks\b", "backlog tasks", lambda: len(_glob("backlog", "tasks", "*.md"))),
    (R, r"(\d+) documents\b", "backlog documents", lambda: len(_glob("backlog", "docs", "*.md"))),
    (
        R,
        r"(\d+) decisions\b",
        "backlog decisions",
        lambda: len(_glob("backlog", "decisions", "*.md")),
    ),
    (
        R,
        r"(\d+) milestones\b",
        "backlog milestones",
        lambda: len(_glob("backlog", "milestones", "*.md")),
    ),
    (
        R,
        r"(\d+) working documents in four directories",
        "documents in thesis/{framing,design,analysis,writing}",
        lambda: sum(
            len(_glob("thesis", d, "*.md")) for d in ("framing", "design", "analysis", "writing")
        ),
    ),
    (R + T, r"(\d+) references\b", "entries in thesis/literature/literature.bib", _bib_entries),
    (T, r"\((\d+) items\)", "entries in thesis/literature/literature.bib", _bib_entries),
    (
        R,
        r"(\d+) full-text transcripts",
        "transcripts in thesis/literature/fulltexts",
        lambda: len(_glob("thesis", "literature", "fulltexts", "*.md")),
    ),
    (
        T,
        r"\((\d+) transcripts\)",
        "transcripts in thesis/literature/fulltexts",
        lambda: len(_glob("thesis", "literature", "fulltexts", "*.md")),
    ),
    (T, r"# (\d+) rules\b", "rules in .alint.yml", _alint_rules),
    (
        T,
        r"\*\*([a-z]+|\d+) directories\*\*",
        "subdirectories of thesis/",
        lambda: len([p for p in (ROOT / "thesis").iterdir() if p.is_dir()]),
    ),
]


def _claims() -> list[str]:
    problems: list[str] = []
    for doc in INDEX_DOCS:
        path = ROOT / doc
        if not path.is_file():
            problems.append(
                f"{doc}: the index document is missing, so its quotes cannot be checked"
            )
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if HISTORICAL.search(line):
                continue
            for docs, pattern, noun, count in COUNTS:
                if doc not in docs:
                    continue
                for match in re.finditer(pattern, line):
                    group = match.group(1)
                    quoted = int(group) if group.isdigit() else WORDS.get(group, -1)
                    try:
                        truth = count()
                    except OSError:
                        truth = None
                    if truth is None:
                        problems.append(f"{doc}:{lineno}: cannot verify the count of {noun}")
                    elif quoted != truth:
                        problems.append(f"{doc}:{lineno}: says {quoted}, but {noun} counts {truth}")
    return problems


# ── retired ─────────────────────────────────────────────────────────────────────────────────────

# Values of the generation that decisions `d-1` and `d-2` replaced. They may still appear — several
# documents keep a register of what was cut — but only in a sentence that says so.
RETIRED = {
    "1 218 runs": r"\b1[ ,]218\b",
    "mcp-5/15/30/50 ladder": r"\bmcp[-_ ]?(?:5|15|30|50)\b",
    "H4a": r"\bH4a\b",
    "TOST": r"\bTOST\b",
    "four agents": r"\bfour (?:agents|models)\b",
    "50-task corpus": r"\b50[- ]tasks?\b",
    "T001-T050 card ids": r"\bT0\d\d\b",
    "min_surface": r"\bmin_surface\b",
}

# Written on the line, or on the heading the line sits under. Only words that name the retirement
# itself: "earlier" or "old" would excuse half the thesis, so they are not here.
MARKED = re.compile(
    r"retir|prun|replac|no longer|stale|void|was cut|withdrawn|abolish|dropped|superseded|"
    r"deprecated|decommission",
    re.IGNORECASE,
)
FROZEN = re.compile(r"^status:\s*frozen\b", re.MULTILINE)


def _retired() -> list[str]:
    problems: list[str] = []
    for path in _walk_md():
        text = path.read_text(encoding="utf-8", errors="replace")
        if text.startswith("---") and FROZEN.search(text.split("---")[1]):
            continue  # a frozen file is a record, not ours to bring up to date
        heading = ""
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.startswith("#"):
                heading = line
            for name, pattern in RETIRED.items():
                if not re.search(pattern, line):
                    continue
                if MARKED.search(line) or MARKED.search(heading):
                    continue
                problems.append(
                    f"{_rel(path)}:{lineno}: {name} belongs to the retired design "
                    f"— say so, or use the live value"
                )
    return problems


# ── ids ────────────────────────────────────────────────────────────────────────────────────────

# `TASK-19` in prose, and the three other id families. Each maps onto a file prefix.
ID_PATTERNS = {
    "TASK": (re.compile(r"\bTASK-(\d+)\b"), "task"),
    "doc": (re.compile(r"\bdoc-(\d+)\b"), "docs/doc"),
    "decision": (re.compile(r"\bd-(\d+)\b"), "decisions/decision"),
    "milestone": (re.compile(r"\bm-(\d+)\b"), "milestones/m"),
}
# An archived id resolves, but only as history: the sentence has to say the work is finished.
FINISHABLE = re.compile(
    r"\b(?:completed?|closed?|done|archived?|superseded|delivered|finished|shipped|merged)\b",
    re.IGNORECASE,
)


def _present_ids(base: str) -> set[tuple[str, str]]:
    present: set[tuple[str, str]] = set()
    for kind, (_pattern, stem) in ID_PATTERNS.items():
        name = stem.rsplit("/", 1)[-1]
        for path in (ROOT / base).rglob(f"{name}-*.md"):
            if "archive" in path.parts and base == "backlog":
                continue  # archived work is resolved by the second pass, and only as history
            match = re.match(rf"{name}-(\d+) -", path.name)
            if match:
                present.add((kind, match.group(1)))
    return present


def _ids() -> list[str]:
    live, archived = _present_ids("backlog"), _present_ids("backlog/archive")
    problems: list[str] = []
    for path in _walk_md():
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            if HISTORICAL.search(line):
                continue
            for kind, (pattern, _stem) in ID_PATTERNS.items():
                for match in pattern.finditer(line):
                    key = (kind, match.group(1))
                    if key in live:
                        continue
                    if key in archived and not FINISHABLE.search(line):
                        problems.append(
                            f"{_rel(path)}:{lineno}: {match.group(0)} is archived — say it is "
                            f"completed, or point at the file in backlog/"
                        )
                    elif key not in archived:
                        problems.append(
                            f"{_rel(path)}:{lineno}: {match.group(0)} names no file in backlog/ "
                            f"or backlog/archive/"
                        )
    return problems


# ── coverage ───────────────────────────────────────────────────────────────────────────────────


def _yaml(path: pathlib.Path) -> object | None:
    """Parse `path` through PyYAML (declared in the `harness` and `qa` features), or None."""
    try:
        import yaml
    except ModuleNotFoundError:
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _config() -> dict | None:
    """`.alint.yml` as a mapping, or None when it cannot be read."""
    config = _yaml(ROOT / ".alint.yml")
    return config if isinstance(config, dict) else None


def _patterns(rule: dict) -> list[str]:
    paths = rule.get("paths")
    if paths is None:
        return []
    return [paths] if isinstance(paths, str) else list(paths)


def _coverage() -> list[str]:
    problems: list[str] = []
    config = _config()
    if config is None:
        return ["cannot read .alint.yml: PyYAML is not importable in this interpreter"]

    linted: set[pathlib.Path] = set()
    for rule in config.get("rules", []):
        rule_id = rule.get("id", "?")
        patterns = _patterns(rule)
        if not patterns or "kind" not in rule:
            continue  # a level override, or a whole-tree rule: nothing to select
        matched: set[pathlib.Path] = set()
        for pattern in patterns:
            matched |= {p.resolve() for p in ROOT.glob(pattern)}
        if rule_id in MARKDOWN_RULES:
            linted |= matched
        sleeping = SLEEPING.get(rule_id)
        if not matched and sleeping is None:
            problems.append(
                f".alint.yml: rule {rule_id!r} selects no file — fix its paths, "
                f"or declare it in SLEEPING with a reason"
            )
        elif matched and sleeping is not None:
            problems.append(
                f".alint.yml: rule {rule_id!r} is declared sleeping ({sleeping}) but now "
                f"matches {len(matched)} file(s) — drop the SLEEPING entry"
            )

    for path in _walk_md():
        if path.resolve() not in linted:
            problems.append(
                f"{_rel(path)}: no markdown rule covers this document — add its directory to the "
                f"markdown-* paths in .alint.yml"
            )
    return problems


# ── backlog ───────────────────────────────────────────────────────────────────────────────────

# The trees a task record may point into. A path outside these is prose, not a promise.
PROMISED_ROOTS = ("thesis/", "docs/", "experiment/", "scripts/", "backlog/")
BODY_PATH = re.compile(r"`([\w./-]+\.(?:md|py|toml|yaml|yml|bib|gpkg|feature))`")


def _front_matter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    head = text.split("---", 1)[1].split("---", 1)[0] if text.startswith("---") else ""
    fields = _yaml_text(head)
    fields["_body"] = text.split("---", 2)[-1]
    fields["_path"] = path
    return fields


def _yaml_text(text: str) -> dict:
    try:
        import yaml
    except ModuleNotFoundError:
        return {}
    loaded = yaml.safe_load(text)
    return loaded if isinstance(loaded, dict) else {}


def _backlog() -> list[str]:
    """The backlog's own links: ids, promises, statuses, and Done tasks that are not done."""
    problems: list[str] = []
    config = _yaml(ROOT / "backlog/config.yml")
    if not isinstance(config, dict):
        return ["backlog/config.yml: cannot be read, so the backlog cannot be checked"]
    statuses = set(config.get("statuses") or [])
    labels = set(config.get("labels") or [])

    milestones = {
        fields.get("id")
        for path in (ROOT / "backlog/milestones").glob("*.md")
        for fields in [_front_matter(path)]
        if fields.get("id")
    }
    records = [_front_matter(p) for p in sorted((ROOT / "backlog/tasks").glob("*.md"))]
    known = {fields.get("id") for fields in records}
    known |= {_front_matter(p).get("id") for p in (ROOT / "backlog/archive/tasks").glob("*.md")}

    for fields in records:
        path, rel = fields["_path"], _rel(fields["_path"])
        task_id = fields.get("id")
        if f"{path.name.split(' - ')[0]}".upper() != str(task_id).upper():
            problems.append(f"{rel}: id {task_id!r} disagrees with the filename")
        if fields.get("status") not in statuses:
            problems.append(
                f"{rel}: status {fields.get('status')!r} is not one of {sorted(statuses)}"
            )
        for label in fields.get("labels") or []:
            if label not in labels:
                problems.append(f"{rel}: label {label!r} is not declared in backlog/config.yml")
        milestone = fields.get("milestone")
        if milestone and milestone not in milestones:
            problems.append(f"{rel}: milestone {milestone!r} names no file in backlog/milestones/")
        for dependency in fields.get("dependencies") or []:
            if dependency not in known:
                problems.append(
                    f"{rel}: dependency {dependency} names no task, here or in the archive"
                )
        for key in ("references", "documentation"):
            value = fields.get(key) or []
            for target in value if isinstance(value, list) else [value]:
                if not (ROOT / target).exists():
                    problems.append(f"{rel}: {key} {target} does not resolve")
        if fields.get("status") == "Done" and "- [ ]" in fields["_body"]:
            problems.append(f"{rel}: status Done, but an acceptance criterion is still unticked")
        for target in sorted(set(BODY_PATH.findall(fields["_body"]))):
            if target.startswith(PROMISED_ROOTS) and not (ROOT / target).exists():
                problems.append(f"{rel}: the body promises {target}, which does not exist")
    return problems


MODES = {
    "counts": _claims,
    "retired": _retired,
    "ids": _ids,
    "coverage": _coverage,
    "backlog": _backlog,
}


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in MODES:
        print(f"usage: {argv[0]} {{{'|'.join(MODES)}}}", file=sys.stderr)
        return 2
    problems = MODES[argv[1]]()
    for problem in problems:
        print(problem)
    if problems:
        print(f"{len(problems)} problem(s) in mode {argv[1]!r}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
