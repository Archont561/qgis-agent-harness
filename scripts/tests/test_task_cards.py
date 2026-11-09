"""What `scripts/task_cards.py` accepts as a card, and what it refuses to read.

Every case is a whole card in a throwaway tree, run through the same command line alint uses.
"""

from __future__ import annotations

import pathlib

from conftest import Run, Write


def _said(done) -> str:
    """task_cards.py reports problems on stderr, so read both streams."""
    return done.stdout + done.stderr


CARD = """schema: 1
id: P-07
family: P
tier: T2
expressible: all
prompt: >
  Compute each feature's area in square metres and write it to `area_m2`.
inputs: [obszary.gpkg]
expected_artifact: wynik/bilans.gpkg
oracle:
  reference: oracles/P-07.py
  seed: 42
  checks:
    - {type: crs_equal,    value: "EPSG:2180"}
    - {type: geom_valid}
    - {type: attr_present, value: [area_m2]}
    - {type: numeric,      field: area_m2, tol_pct: 0.1}
negative_control:
  artifact: the area computed on the layer's degrees instead of its metres
  must_fail: [numeric]
pitfalls: [area in degrees instead of metres]
licence: n/a
created: 2026-11-07
"""


def _card(write: Write, root: pathlib.Path, text: str = CARD, name: str = "P-07.yaml") -> str:
    return str(write(root, f"experiment/tasks/cards/{name}", text))


def test_a_valid_card_passes(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    path = _card(write, tmp_path)
    done = run("task_cards.py", "schema", path, cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_an_unknown_key_is_an_error(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    path = _card(write, tmp_path, CARD.replace("tier: T2", "tier: T2\nmin_surface: 1"))
    done = run("task_cards.py", "schema", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "unknown key(s) min_surface" in _said(done)


def test_a_predicate_with_the_wrong_arguments_is_an_error(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    text = CARD.replace(
        "{type: numeric,      field: area_m2, tol_pct: 0.1}",
        "{type: numeric,      field: area_m2, tol_pct: 0.1, tol: 2}",
    )
    path = _card(write, tmp_path, text)
    done = run("task_cards.py", "schema", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "check numeric takes" in done.stdout + done.stderr


def test_four_checks_of_one_predicate_are_not_a_set(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    text = CARD.replace(
        """    - {type: geom_valid}
    - {type: attr_present, value: [area_m2]}
    - {type: numeric,      field: area_m2, tol_pct: 0.1}""",
        """    - {type: crs_equal, value: "EPSG:2180"}
    - {type: crs_equal, value: "EPSG:2180"}
    - {type: crs_equal, value: "EPSG:2180"}""",
    )
    path = _card(write, tmp_path, text)
    done = run("task_cards.py", "schema", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "one predicate is not a set" in done.stdout + done.stderr


def test_the_id_must_agree_with_the_family(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    text = CARD.replace("id: P-07", "id: C-07")
    path = _card(write, tmp_path, text)
    done = run("task_cards.py", "schema", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "disagrees with family" in done.stdout + done.stderr


def test_the_id_must_match_the_filename(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    path = _card(write, tmp_path, CARD, name="P-08.yaml")
    done = run("task_cards.py", "schema", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "does not match the filename" in done.stdout + done.stderr


def test_a_document_without_a_card_example_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    path = write(tmp_path, "experiment/tasks/README.md", "# Schema\n\nNo example yet.\n")
    done = run("task_cards.py", "schema", str(path), cwd=tmp_path)
    assert done.returncode == 1
    assert "card example found" in _said(done)


def test_usage_without_a_mode_is_refused(run: Run, tmp_path: pathlib.Path) -> None:
    done = run("task_cards.py", cwd=tmp_path)
    assert done.returncode == 1
    assert "usage: task_cards.py" in done.stderr or "usage: task_cards.py" in done.stdout


CORPUS = """# Corpus

| Quantity | Value |
|---|---|
| Task cards | **80** |
| Repetitions | **r = 4** |
| Runs | **960** |
"""

SCHEMA_DOC = "# Schema\n\nThe corpus is 80 cards at r = 4, so 960 runs.\n"


def _numbers(
    write: Write, root: pathlib.Path, corpus: str = CORPUS, schema: str = SCHEMA_DOC
) -> str:
    write(root, "experiment/tasks/README.md", schema)
    return str(write(root, "thesis/design/corpus.md", corpus))


def test_the_run_arithmetic_must_hold(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    path = _numbers(write, tmp_path, corpus=CORPUS.replace("**960**", "**965**"))
    done = run("task_cards.py", "numbers", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "is 960, not 965" in done.stdout + done.stderr


def test_the_arithmetic_passes_when_it_holds(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    path = _numbers(write, tmp_path)
    done = run("task_cards.py", "numbers", path, cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_the_schema_document_must_state_the_numbers(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    path = _numbers(write, tmp_path, schema="# Schema\n\nNothing quoted.\n")
    done = run("task_cards.py", "numbers", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "does not state 80 (cards)" in done.stdout + done.stderr


def test_a_retired_key_is_refused_outside_the_grave(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    schema = SCHEMA_DOC + "\nA card carries `min_surface` today.\n"
    path = _numbers(write, tmp_path, schema=schema)
    done = run("task_cards.py", "numbers", path, cwd=tmp_path)
    assert done.returncode == 1
    assert "retired key 'min_surface' is back outside the retirement section" in _said(done)


def test_a_retired_key_is_allowed_inside_the_grave(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    schema = SCHEMA_DOC + "\n## 5. The retired generation\n\nA card carried `min_surface`.\n"
    path = _numbers(write, tmp_path, schema=schema)
    done = run("task_cards.py", "numbers", path, cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
