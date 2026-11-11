"""What `scripts/repo_facts.py` refuses, and what it lets through.

Four modes, one section each: the quotes in the index documents, the retired vocabulary, the
backlog ids, and the coverage of the alint rules themselves.
"""

from __future__ import annotations

import pathlib

import pytest
from conftest import Run, Write

INDEX = "# thesis index\n\nNothing quoted yet.\n"
README = "# root\n\n| `backlog/` | {tasks} tasks, 0 documents, 0 decisions, 0 milestones |\n"


def _tree(write: Write, root: pathlib.Path, tasks: int, quoted: int) -> None:
    for number in range(1, tasks + 1):
        write(root, f"backlog/tasks/task-{number} - thing.md", "---\nid: TASK-x\n---\n")
    write(root, "README.md", README.format(tasks=quoted))
    write(root, "thesis/README.md", INDEX)


# ── counts ──────────────────────────────────────────────────────────────────────────────────────


def test_counts_accept_a_number_that_matches(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _tree(write, tmp_path, tasks=2, quoted=2)
    done = run("repo_facts.py", "counts", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_counts_report_a_number_that_drifted(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _tree(write, tmp_path, tasks=2, quoted=3)
    done = run("repo_facts.py", "counts", cwd=tmp_path)
    assert done.returncode == 1
    assert "says 3, but backlog tasks counts 2" in done.stdout


def test_counts_leave_a_dated_history_row_alone(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _tree(write, tmp_path, tasks=2, quoted=2)
    write(tmp_path, "README.md", README.format(tasks=2) + "| 7 XI 2026 | 9 tasks |\n")
    done = run("repo_facts.py", "counts", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_counts_report_a_missing_index_document(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "README.md", README.format(tasks=0))
    done = run("repo_facts.py", "counts", cwd=tmp_path)
    assert done.returncode == 1
    assert "thesis/README.md: the index document is missing" in done.stdout


# ── retired ─────────────────────────────────────────────────────────────────────────────────────

STALE = "# A live question\n\nThe series is 1 218 runs.\n"


def test_retired_value_needs_a_marker(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    write(tmp_path, "thesis/design/x.md", STALE)
    done = run("repo_facts.py", "retired", cwd=tmp_path)
    assert done.returncode == 1
    assert "1 218 runs belongs to the retired design" in done.stdout


def test_retired_value_passes_when_the_sentence_marks_it(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "thesis/design/x.md", "# Live\n\nThe retired series was 1 218 runs.\n")
    done = run("repo_facts.py", "retired", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_retired_value_passes_under_a_pruning_heading(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(
        tmp_path,
        "thesis/design/x.md",
        "# Live\n\n## What was cut, and why\n\nThe series is 1 218 runs.\n",
    )
    done = run("repo_facts.py", "retired", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_frozen_file_is_a_record_not_a_document(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "thesis/design/x.md", "---\nstatus: frozen\n---\n" + STALE)
    done = run("repo_facts.py", "retired", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_the_cli_managed_backlog_is_exempt(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    write(tmp_path, "backlog/decisions/decision-9 - old.md", STALE)
    done = run("repo_facts.py", "retired", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_the_myst_build_tree_is_exempt(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    """`myst start` rewrites every page as markdown under _build/, and a generated tree is not prose."""
    write(tmp_path, "_build/site/public/index-a3dad9ecfc933edd0e6e793bd5037052.md", STALE)
    done = run("repo_facts.py", "retired", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


# ── ids ────────────────────────────────────────────────────────────────────────────────────────


def test_dangling_id_is_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    write(tmp_path, "docs/x.md", "# x\n\nSee `TASK-99`.\n")
    done = run("repo_facts.py", "ids", cwd=tmp_path)
    assert done.returncode == 1
    assert "TASK-99 names no file" in done.stdout


def test_live_id_is_accepted(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    write(tmp_path, "backlog/tasks/task-7 - thing.md", "---\nid: TASK-7\n---\n")
    write(tmp_path, "docs/x.md", "# x\n\nSee `TASK-7`.\n")
    done = run("repo_facts.py", "ids", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_archived_id_must_be_called_finished(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "backlog/archive/tasks/task-19 - thing.md", "---\nid: TASK-19\n---\n")
    write(tmp_path, "docs/x.md", "# x\n\nSee `TASK-19`.\n")
    done = run("repo_facts.py", "ids", cwd=tmp_path)
    assert done.returncode == 1
    assert "TASK-19 is archived" in done.stdout


def test_archived_id_passes_once_the_line_says_completed(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "backlog/archive/tasks/task-19 - thing.md", "---\nid: TASK-19\n---\n")
    write(tmp_path, "docs/x.md", "# x\n\n`TASK-19` is completed: it moved the notes.\n")
    done = run("repo_facts.py", "ids", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


# ── coverage ───────────────────────────────────────────────────────────────────────────────────

pytest.importorskip("yaml", reason="coverage mode reads .alint.yml through PyYAML")


def _config(write: Write, root: pathlib.Path, *rules: str) -> None:
    write(root, ".alint.yml", "version: 1\nrules:\n" + "".join(rules))


def _rule(rule_id: str, paths: str) -> str:
    return (
        f"  - id: {rule_id}\n"
        "    kind: command\n"
        "    level: error\n"
        f"    paths: {paths}\n"
        "    command: [python3, scripts/whatever.py]\n"
    )


def test_coverage_reports_a_rule_that_lints_nothing(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _config(write, tmp_path, _rule("dead-rule", '["nowhere/*.yaml"]'))
    done = run("repo_facts.py", "coverage", cwd=tmp_path)
    assert done.returncode == 1
    assert "rule 'dead-rule' selects no file" in done.stdout


def test_coverage_reports_a_sleeping_rule_that_woke_up(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    # `task-card-schema-cards` is the rule still declared sleeping: TASK-15 wakes it by adding the
    # first card. The exemption is what is tested, so the rule named here is the one in SLEEPING.
    write(tmp_path, "experiment/tasks/cards/a.yaml", "id: a\n")
    _config(write, tmp_path, _rule("task-card-schema-cards", '["experiment/tasks/cards/*.yaml"]'))
    done = run("repo_facts.py", "coverage", cwd=tmp_path)
    assert done.returncode == 1
    assert "is declared sleeping" in done.stdout


def test_coverage_reports_a_document_no_rule_lints(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "docs/a.md", "# a\n")
    write(tmp_path, "thesis/b.md", "# b\n")
    _config(
        write,
        tmp_path,
        _rule("markdown-links-resolve", '["docs/**/*.md"]'),
        _rule("markdown-paths-resolve", '["docs/**/*.md"]'),
        _rule("markdown-fragments-resolve", '["docs/**/*.md"]'),
    )
    done = run("repo_facts.py", "coverage", cwd=tmp_path)
    assert done.returncode == 1
    assert "thesis/b.md: no markdown rule covers this document" in done.stdout
    assert "docs/a.md" not in done.stdout


# ── backlog ────────────────────────────────────────────────────────────────────────────────────

CONFIG = """default_status: "To Do"
statuses: ["To Do", "In Progress", "Done"]
labels: ["thesis", "experiment"]
"""

MILESTONE = "---\nid: m-0\ntitle: first\n---\n\n## Description\n\nFirst.\n"


def _backlog(write: Write, root: pathlib.Path, body: str, **fields: str) -> None:
    write(root, "backlog/config.yml", CONFIG)
    write(root, "backlog/milestones/m-0 - first.md", MILESTONE)
    head = "".join(f"{key}: {value}\n" for key, value in fields.items())
    write(root, "backlog/tasks/task-1 - a-task.md", f"---\nid: TASK-1\n{head}---\n\n{body}")


def test_a_sound_task_record_passes(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _backlog(
        write,
        tmp_path,
        "## Acceptance Criteria\n\n- [x] #1 done\n",
        status="Done",
        labels="\n  - thesis",
        milestone="m-0",
    )
    done = run("repo_facts.py", "backlog", cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


def test_a_done_task_with_an_unticked_box_fails(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _backlog(write, tmp_path, "- [ ] #1 not done\n", status="Done", labels="\n  - thesis")
    done = run("repo_facts.py", "backlog", cwd=tmp_path)
    assert done.returncode == 1
    assert "status Done, but an acceptance criterion is still unticked" in done.stdout


def test_a_dependency_that_names_no_task_fails(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _backlog(write, tmp_path, "nothing yet\n", status="To Do", dependencies="\n  - TASK-99")
    done = run("repo_facts.py", "backlog", cwd=tmp_path)
    assert done.returncode == 1
    assert "dependency TASK-99 names no task, here or in the archive" in done.stdout


def test_an_undeclared_label_fails(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _backlog(write, tmp_path, "nothing yet\n", status="To Do", labels="\n  - cartography")
    done = run("repo_facts.py", "backlog", cwd=tmp_path)
    assert done.returncode == 1
    assert "label 'cartography' is not declared" in done.stdout


def test_a_missing_milestone_fails(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _backlog(write, tmp_path, "nothing yet\n", status="To Do", milestone="m-9")
    done = run("repo_facts.py", "backlog", cwd=tmp_path)
    assert done.returncode == 1
    assert "milestone 'm-9' names no file" in done.stdout


def test_a_documentation_path_that_gone_fails(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _backlog(write, tmp_path, "nothing yet\n", status="To Do", documentation="\n  - thesis/gone.md")
    done = run("repo_facts.py", "backlog", cwd=tmp_path)
    assert done.returncode == 1
    assert "documentation thesis/gone.md does not resolve" in done.stdout


def test_a_path_promised_in_the_body_fails_when_it_vanishes(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _backlog(write, tmp_path, "Read `thesis/design/gone.md` first.\n", status="To Do")
    done = run("repo_facts.py", "backlog", cwd=tmp_path)
    assert done.returncode == 1
    assert "the body promises thesis/design/gone.md, which does not exist" in done.stdout
