"""What `scripts/terminology.py` demands of the label vocabulary.

Three families once shared one letter: the catalogue conditions keep `N1` and `N4`, the ranked
contributions are `C1`-`C6`, and the field currents are `F1`-`F6`. Each promise is checked on its
own, so a document that quotes an old numbering on purpose still passes while a live document
carrying a stray N label does not.
"""

from __future__ import annotations

import pathlib

from conftest import Run, Write

CLEAN = """# A document

The conditions are K, N1 and N4; the rungs are L0-L5, and only `L1 / N1` and `L4 / N4` bind one to a
condition. Contributions are C1-C6 and the currents are F1-F6.
"""


def _doc(write: Write, root: pathlib.Path, text: str, name: str = "doc.md") -> pathlib.Path:
    return write(root, name, text)


def test_a_clean_document_passes(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _doc(write, tmp_path, CLEAN)
    result = run("terminology.py", "doc.md", cwd=tmp_path)
    assert result.returncode == 0, result.stdout
    assert result.stdout == ""


def test_an_unknown_n_label_is_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _doc(write, tmp_path, CLEAN + "\nThe second rung is N2, which is not a condition.\n")
    result = run("terminology.py", "doc.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "N1 and N4 are the only N labels" in result.stdout
    assert "doc.md:6" in result.stdout


def test_the_two_conditions_pass_as_labels(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _doc(write, tmp_path, "# Doc\n\nN1 and N4 differ only in enforcement.\n")
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0


def test_a_mismatched_rung_binding_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _doc(write, tmp_path, "# Doc\n\nThe extended condition is `L4 / N1`.\n")
    result = run("terminology.py", "doc.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "only `L1 / N1` and `L4 / N4`" in result.stdout


def test_both_legal_rung_bindings_pass(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _doc(write, tmp_path, "# Doc\n\nThe rungs `L1 / N1` and `L4 / N4` are the two conditions.\n")
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0


def test_a_binding_to_an_unattached_rung_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _doc(write, tmp_path, "# Doc\n\nA middle cell would be `L2 / N2`.\n")
    result = run("terminology.py", "doc.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "L2 / N2" in result.stdout


def test_a_contribution_label_out_of_range_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _doc(write, tmp_path, CLEAN + "\nA seventh contribution would be C7.\n")
    result = run("terminology.py", "doc.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "six ranked contributions" in result.stdout

    _doc(write, tmp_path, "# Doc\n\nC1 through C6 are the ranked contributions.\n")
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0


def test_a_current_label_out_of_range_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _doc(write, tmp_path, "# Doc\n\nThe seventh current would be F7.\n")
    result = run("terminology.py", "doc.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "six field currents" in result.stdout


def test_a_word_that_only_looks_like_a_label_is_not_one(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _doc(write, tmp_path, "# Doc\n\nThe colour is C101 in the slide theme.\n")
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0


def test_a_line_that_names_the_retirement_may_quote_the_old_label(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _doc(write, tmp_path, "# Doc\n\nThe rung formerly called N2 was renamed L2 in November 2026.\n")
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0


def test_a_pruning_heading_excuses_the_rows_under_it(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    body = "# Doc\n\n## 10. What was pruned, and why\n\n| the items N2 and N5 | a source note |\n"
    _doc(write, tmp_path, body)
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0

    live = "# Doc\n\n## 3. The live design\n\n| the items N2 and N5 | a source note |\n"
    _doc(write, tmp_path, live)
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 1


def test_a_frozen_file_is_skipped(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    frozen = "---\nid: old\nstatus: frozen\n---\n\n# Doc\n\nThe rung N2 is what we used to run.\n"
    _doc(write, tmp_path, frozen)
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0


def test_a_label_inside_a_fence_is_a_subscript_not_a_claim(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    fenced = (
        "# Doc\n\n```sh\npixi run render math-slide "
        "'\\mathrm{TSR}_{N4} - \\mathrm{TSR}_{K}'\n```\n"
    )
    _doc(write, tmp_path, fenced)
    assert run("terminology.py", "doc.md", cwd=tmp_path).returncode == 0


def test_a_missing_path_is_a_usage_error(run: Run, tmp_path: pathlib.Path) -> None:
    result = run("terminology.py", "nope.md", cwd=tmp_path)
    assert result.returncode == 2
    assert "missing" in result.stderr


def test_with_no_arguments_the_tree_is_walked(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "thesis/design/deep.md", "# Deep\n\nThe rung N3 is not a condition.\n")
    result = run("terminology.py", cwd=tmp_path)
    assert result.returncode == 1
    assert "thesis/design/deep.md:3" in result.stdout


def test_the_records_are_exempt(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    write(tmp_path, "backlog/tasks/task-1.md", "# Task\n\nThe rung N2 was the plan.\n")
    write(tmp_path, "thesis/literature/fulltexts/paper.md", "# Paper\n\nWe used N2 in our study.\n")
    assert run("terminology.py", cwd=tmp_path).returncode == 0
