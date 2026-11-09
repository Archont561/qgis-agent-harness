#!/usr/bin/env python3
"""Check that task cards, and the documents that show them, match the canonical schema.

Two jobs, one per alint rule:

    python scripts/task_cards.py schema <path>    # card examples in a document, or a card file
    python scripts/task_cards.py numbers <path>   # corpus numbers and retired keys, cross-file

The canonical specification is ``experiment/tasks/README.md``. This script carries the same
vocabulary as literals, and ``schema`` mode refuses to run if the document and the script disagree —
otherwise a schema edit would leave a checker validating the previous generation, which is exactly
the drift the rules exist to stop.

Stdlib plus PyYAML: the same pair the ``thesis-frontmatter`` rule already relies on, both declared
in the ``qa`` feature.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import yaml

SCHEMA_DOC = Path("experiment/tasks/README.md")
CORPUS_DOC = Path("thesis/design/corpus.md")
CARDS_DIR = Path("experiment/tasks/cards")

#: Top-level keys, required or optional. Literal, so the script cannot drift from the document.
REQUIRED = {
    "schema",
    "id",
    "family",
    "tier",
    "expressible",
    "prompt",
    "inputs",
    "expected_artifact",
    "pitfalls",
    "licence",
    "created",
    "oracle",
    "negative_control",
}
OPTIONAL = {"preconditions", "provenance", "notes"}
ORACLE_REQUIRED = {"reference", "seed", "checks"}
NEGATIVE_REQUIRED = {"artifact", "must_fail"}
PROVENANCE_KEYS = {"borrowed", "changed"}

FAMILIES = {"P", "A", "C"}
TIERS = {"T1", "T2", "T3", "T4"}
EXPRESSIBLE = {"all", "most", "part", "none"}

#: predicate -> required arguments (empty set = no arguments).
PREDICATES = {
    "crs_equal": {"value"},
    "geom_valid": set(),
    "extent_iou": {"value"},
    "feature_count": {"value"},
    "attr_present": {"value"},
    "attr_exact": {"value"},
    "numeric": {"field", "tol_pct"},
    "topology": {"value"},
    "scalar": {"tol"},
    "refusal": set(),
    "handle_carries_georeference": {"value"},
    "renderer_type": {"value"},
    "class_count": {"value"},
    "class_method": {"value"},
    "fields_used": {"value"},
    "image_not_empty": set(),
    "dpi": {"value"},
}

#: Keys of the 50-task / tool-ladder generation. They may appear in the schema doc only inside the
#: section that documents their retirement.
RETIRED_KEYS = (
    "block",
    "min_surface",
    "distractors",
    "tools_required",
    "tools_optional",
    "expected_classes",
    "answer_form",
    "reference_steps",
    "attack",
    "success_if",
)

CARD_ID = re.compile(r"^([PAC])-(\d{2})$")


def _fail(messages: list[str]) -> int:
    for message in messages:
        print(message, file=sys.stderr)
    return 1 if messages else 0


def parse_card(text: str, where: str) -> list[str]:
    """Validate one card mapping. Returns a list of problems."""
    problems: list[str] = []
    try:
        card = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return [f"{where}: not valid YAML ({exc.__class__.__name__})"]
    if not isinstance(card, dict):
        return [f"{where}: a card is a mapping, not {type(card).__name__}"]

    missing = REQUIRED - set(card)
    unknown = set(card) - REQUIRED - OPTIONAL
    if missing:
        problems.append(f"{where}: missing {', '.join(sorted(missing))}")
    if unknown:
        problems.append(
            f"{where}: unknown key(s) {', '.join(sorted(unknown))} — unknown keys are errors"
        )
    if missing or unknown:
        return problems

    if card["schema"] != 1:
        problems.append(f"{where}: schema is {card['schema']!r}, only 1 is defined")
    match = CARD_ID.match(str(card["id"]))
    if not match:
        problems.append(f"{where}: id {card['id']!r} is not <P|A|C>-nn")
    elif card["family"] not in FAMILIES or match.group(1) != card["family"]:
        problems.append(f"{where}: id {card['id']!r} disagrees with family {card['family']!r}")
    if card["family"] not in FAMILIES:
        problems.append(f"{where}: family {card['family']!r} not in {sorted(FAMILIES)}")
    if card["tier"] not in TIERS:
        problems.append(f"{where}: tier {card['tier']!r} not in {sorted(TIERS)}")
    if card["expressible"] not in EXPRESSIBLE:
        problems.append(
            f"{where}: expressible {card['expressible']!r} not in {sorted(EXPRESSIBLE)}"
        )
    if not isinstance(card["inputs"], list) or not card["inputs"]:
        problems.append(f"{where}: inputs must be a non-empty list")
    if not isinstance(card["pitfalls"], list) or not card["pitfalls"]:
        problems.append(
            f"{where}: pitfalls must be a non-empty list (the silent error it provokes)"
        )
    try:
        dt.date.fromisoformat(str(card["created"]))
    except ValueError:
        problems.append(f"{where}: created {card['created']!r} is not YYYY-MM-DD")

    # ── oracle ───────────────────────────────────────────────────────────────────────────────────
    oracle = card["oracle"]
    if not isinstance(oracle, dict):
        problems.append(f"{where}: oracle is a mapping")
        return problems
    if ORACLE_REQUIRED - set(oracle) or set(oracle) - ORACLE_REQUIRED:
        problems.append(f"{where}: oracle keys must be exactly {sorted(ORACLE_REQUIRED)}")
    if not isinstance(oracle.get("seed"), int):
        problems.append(f"{where}: oracle.seed must be an integer")
    expected_reference = f"oracles/{card['id']}.py"
    if oracle.get("reference") != expected_reference:
        problems.append(
            f"{where}: oracle.reference is {oracle.get('reference')!r}, want {expected_reference!r}"
        )

    checks = oracle.get("checks")
    if not isinstance(checks, list) or len(checks) < 4:
        problems.append(f"{where}: oracle.checks needs at least four predicates")
        checks = [c for c in checks if isinstance(c, dict)] if isinstance(checks, list) else []
    seen: set[str] = set()
    for check in checks:
        if not isinstance(check, dict) or "type" not in check:
            problems.append(f"{where}: a check must be a mapping with a type")
            continue
        kind, given = check["type"], set(check) - {"type"}
        if kind not in PREDICATES:
            problems.append(f"{where}: check type {kind!r} is not in the predicate table")
            continue
        if PREDICATES[kind] != given:
            problems.append(
                f"{where}: check {kind} takes {sorted(PREDICATES[kind]) or 'no arguments'}, "
                f"got {sorted(given) or 'none'}"
            )
        seen.add(kind)
    if len(seen) < 2 and checks:
        problems.append(f"{where}: checks are all the same predicate — one predicate is not a set")

    # ── negative control ─────────────────────────────────────────────────────────────────────────
    control = card["negative_control"]
    if (
        not isinstance(control, dict)
        or NEGATIVE_REQUIRED - set(control)
        or set(control) - NEGATIVE_REQUIRED
    ):
        problems.append(
            f"{where}: negative_control keys must be exactly {sorted(NEGATIVE_REQUIRED)}"
        )
        return problems
    must_fail = control["must_fail"]
    if not isinstance(must_fail, list) or not must_fail:
        problems.append(f"{where}: negative_control.must_fail must be a non-empty list")
    else:
        stray = [m for m in must_fail if m not in seen]
        if stray:
            problems.append(
                f"{where}: negative_control.must_fail names checks that do not exist: "
                f"{', '.join(map(str, stray))}"
            )

    provenance = card.get("provenance")
    if provenance is not None and (
        not isinstance(provenance, dict) or set(provenance) - PROVENANCE_KEYS
    ):
        problems.append(f"{where}: provenance keys must be drawn from {sorted(PROVENANCE_KEYS)}")
    return problems


def card_blocks(markdown: str) -> list[tuple[int, str]]:
    """Every fenced ```yaml block that declares an id — i.e. every card example."""
    blocks, line_no, current = [], 1, None
    for line in markdown.splitlines():
        if current is None and line.strip() == "```yaml":
            current, start = [], line_no
        elif current is not None and line.strip() == "```":
            text = "\n".join(current)
            if re.search(r"^id:", text, re.M):
                blocks.append((start, text))
            current = None
        elif current is not None:
            current.append(line)
        line_no += 1
    return blocks


def _documented(text: str, name: str) -> bool:
    """``name`` appears as a backticked token, with or without the table-header brackets."""
    return re.search(rf"`\[?{re.escape(name)}\]?`", text) is not None


def vocabulary_drift(where: Path) -> list[str]:
    """The doc and this script must name the same keys and predicates — outside the grave."""
    text = where.read_text()
    problems = []
    missing_pred = sorted(p for p in PREDICATES if not _documented(text, p))
    if missing_pred:
        problems.append(
            f"{where}: predicate(s) in the checker but not documented: {', '.join(missing_pred)}"
        )
    for key in sorted(REQUIRED | OPTIONAL | ORACLE_REQUIRED | NEGATIVE_REQUIRED):
        if not _documented(text, key):
            problems.append(f"{where}: key {key!r} is in the checker but not documented")
    for key in RETIRED_KEYS:
        if _documented(_live_sections(text), key):
            problems.append(f"{where}: retired key {key!r} is documented as if it were live")
    return problems


def _live_sections(text: str) -> str:
    """The document without the section that retires the previous generation."""
    kept, graveyard = [], False
    for line in text.splitlines():
        if line.startswith("## 5. The retired generation"):
            graveyard = True
        elif line.startswith("## "):
            graveyard = False
        if not graveyard:
            kept.append(line)
    return "\n".join(kept)


def check_schema(path: Path) -> int:
    problems: list[str] = []
    if path.as_posix() == SCHEMA_DOC.as_posix():
        problems += vocabulary_drift(path)

    if path.suffix == ".md":
        blocks = card_blocks(path.read_text())
        if not blocks:
            problems.append(
                f"{path}: no ```yaml card example found — the examples are the documentation"
            )
        for start, text in blocks:
            problems += parse_card(text, f"{path}:{start}")
    else:
        problems += parse_card(path.read_text(), str(path))
        match = CARD_ID.match(path.stem)
        if not match:
            problems.append(f"{path}: filename is not <P|A|C>-nn.yaml")
        else:
            card = yaml.safe_load(path.read_text())
            if isinstance(card, dict) and card.get("id") != path.stem:
                problems.append(f"{path}: id {card.get('id')!r} does not match the filename")
    return _fail(problems)


def corpus_numbers(text: str) -> dict[str, int | None]:
    """The three quantities the corpus doc owns, read from its summary table."""

    def grab(pattern: str) -> int | None:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    return {
        "cards": grab(r"\|\s*Task cards\s*\|\s*\*\*(\d+)\*\*"),
        "repetitions": grab(r"\|\s*Repetitions\s*\|\s*\*\*r\s*=\s*(\d+)\*\*"),
        "runs": grab(r"\|\s*Runs\s*\|[^|]*?\*\*(\d+)\*\*"),
    }


def check_numbers(path: Path) -> int:
    problems: list[str] = []
    numbers = corpus_numbers(path.read_text())
    for key, value in numbers.items():
        if value is None:
            problems.append(f"{path}: could not read the {key} figure from the summary table")
    if problems:
        return _fail(problems)

    schema_doc = SCHEMA_DOC.read_text()
    for key in ("cards", "repetitions", "runs"):
        if str(numbers[key]) not in schema_doc:
            problems.append(
                f"{SCHEMA_DOC}: does not state {numbers[key]} ({key}) — {path} owns that number"
            )
    if numbers["cards"] * numbers["repetitions"] * 3 != numbers["runs"]:
        problems.append(
            f"{path}: {numbers['cards']} cards x {numbers['repetitions']} repetitions "
            f"x 3 conditions "
            f"is {numbers['cards'] * numbers['repetitions'] * 3}, not {numbers['runs']}"
        )

    for key in RETIRED_KEYS:
        if _documented(_live_sections(schema_doc), key):
            problems.append(
                f"{SCHEMA_DOC}: retired key {key!r} is back outside the retirement section"
            )
    return _fail(problems)


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] not in {"schema", "numbers"}:
        return _fail(["usage: task_cards.py schema|numbers <path>"])
    mode, raw = argv
    path = Path(raw)
    if not path.is_file():
        return _fail([f"{path}: no such file"])
    return check_schema(path) if mode == "schema" else check_numbers(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
