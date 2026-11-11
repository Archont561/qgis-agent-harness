"""What `scripts/house_style.py` demands of a repository's README and CONTRIBUTING.

The checker has three modes and the split is the interesting part: `invariants` are things every
repository under the account already does, `skeleton` is the README shape the newest ones use,
and `contributing` is the day-to-day loop. Each promise is checked on its own — a good document
passes, and one broken convention is caught while the others stay quiet.
"""

from __future__ import annotations

import pathlib

from conftest import Run, Write

README = """# thing

<p align="center">
  <a href="https://example.invalid/ci"><img src="https://example.invalid/ci.svg" alt="CI"></a>
</p>

**One bold sentence saying what this is.**

> Status: pre-release `0.x` — the shell exists, nothing runs yet.

## What it measures

| Condition | What the gate can see |
| :-- | :-- |
| K | syntax |

```sh
pixi run test
```

## Try it

```sh
pixi install
```

## Develop

```sh
pixi run qa
```

## Documentation

- [Contract](docs/contract.md) — the schema

## License

MIT.
"""

CONTRIBUTING = """# Contributing to thing

## Environment

```sh
pixi install --locked
```

## Commands

| Command | Purpose |
| :-- | :-- |
| `pixi run qa` | the whole gate |

## Commits

Use Conventional Commits.
"""


def _readme(write: Write, root: pathlib.Path, text: str = README) -> pathlib.Path:
    return write(root, "README.md", text)


def test_a_conforming_readme_passes(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _readme(write, tmp_path)
    result = run("house_style.py", "readme", "README.md", cwd=tmp_path)
    assert result.returncode == 0, result.stdout
    assert result.stdout == ""


def test_a_conforming_contributing_passes(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    write(tmp_path, "CONTRIBUTING.md", CONTRIBUTING)
    result = run("house_style.py", "contributing", "CONTRIBUTING.md", cwd=tmp_path)
    assert result.returncode == 0, result.stdout


def test_front_matter_before_the_h1_is_not_a_violation(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _readme(write, tmp_path, "---\nid: thing\n---\n" + README)
    result = run("house_style.py", "readme", "README.md", cwd=tmp_path)
    assert result.returncode == 0, result.stdout


def test_missing_h1_is_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _readme(write, tmp_path, README.replace("# thing\n", ""))
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "no H1" in result.stdout


def test_a_badge_without_alt_is_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    broken = README.replace(' alt="CI"', "")
    _readme(write, tmp_path, broken)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "without alt" in result.stdout


def test_a_table_without_an_alignment_row_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    broken = README.replace("| :-- | :-- |\n", "")
    _readme(write, tmp_path, broken)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "alignment row" in result.stdout


def test_an_untagged_fence_is_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    broken = README.replace("```sh\npixi install\n```", "```\npixi install\n```")
    _readme(write, tmp_path, broken)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "no language" in result.stdout


def test_an_unknown_fence_language_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    broken = README.replace("```sh\npixi install\n```", "```klingon\npixi install\n```")
    _readme(write, tmp_path, broken)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "unknown fence language" in result.stdout


def test_a_myst_directive_fence_counts_as_named(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    """A MyST page tags a fence with a directive, not a language — the fence is still named."""
    with_directive = README.replace(
        "```sh\npixi install\n```", "```{note}\nNothing to install yet.\n```"
    )
    _readme(write, tmp_path, with_directive)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 0, result.stdout


def test_emoji_is_reported_and_a_fence_is_not_scanned_for_it(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    with_emoji = README.replace("## Develop", "## Develop ✅")
    _readme(write, tmp_path, with_emoji)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "emoji" in result.stdout

    in_fence = README.replace("pixi run qa", "echo ✅")
    _readme(write, tmp_path, in_fence)
    assert run("house_style.py", "invariants", "README.md", cwd=tmp_path).returncode == 0


def test_a_check_mark_that_carries_data_passes_while_a_pictograph_fails(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    data = (
        README.replace("| What the gate can see |", "| What the gate can see | OK |")
        .replace("| :-- | :-- |", "| :-- | :-- | :-- |")
        .replace("| K | syntax |", "| K | syntax | \u2714 |")
    )
    _readme(write, tmp_path, data)
    assert run("house_style.py", "invariants", "README.md", cwd=tmp_path).returncode == 0

    decorative = README.replace("## Develop", "## Develop \U00002705")
    _readme(write, tmp_path, decorative)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "emoji" in result.stdout


def test_a_heading_ending_in_punctuation_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _readme(write, tmp_path, README.replace("## Documentation", "## Documentation."))
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "ends with punctuation" in result.stdout


def test_a_skipped_heading_level_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    broken = README.replace("### nothing", "") + "\n#### Deep\n"
    _readme(write, tmp_path, broken)
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "skip a level" in result.stdout


def test_a_section_after_the_licence_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _readme(write, tmp_path, README + "\n## Afterword\n\nlate.\n")
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "last section" in result.stdout


def test_the_british_spelling_of_the_licence_heading_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    _readme(write, tmp_path, README.replace("## License", "## Licence"))
    result = run("house_style.py", "invariants", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "the heading is `License`" in result.stdout


def test_the_skeleton_is_opt_in_so_a_plain_readme_still_passes_invariants(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    plain = """# thing

A plain document with no badges, no tagline and no status line.

## License

MIT.
"""
    _readme(write, tmp_path, plain)
    assert run("house_style.py", "invariants", "README.md", cwd=tmp_path).returncode == 0
    skeleton = run("house_style.py", "skeleton", "README.md", cwd=tmp_path)
    assert skeleton.returncode == 1
    assert "badge block" in skeleton.stdout


def test_the_skeleton_reports_each_missing_piece(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    broken = (
        README.replace('<p align="center">', "<p>")
        .replace("**One bold sentence saying what this is.**", "One bold sentence.")
        .replace("> Status:", "Status:")
    )
    _readme(write, tmp_path, broken)
    result = run("house_style.py", "skeleton", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "badge block" in result.stdout
    assert "bold tagline" in result.stdout
    assert "status line" in result.stdout


def test_a_missing_skeleton_section_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    broken = README.replace("## Develop\n\n```sh\npixi run qa\n```\n", "")
    _readme(write, tmp_path, broken)
    result = run("house_style.py", "skeleton", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "no `## Develop` section" in result.stdout


def test_out_of_order_sections_are_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    swapped = README.replace(
        "## Try it\n\n```sh\npixi install\n```\n\n## Develop\n\n```sh\npixi run qa\n```",
        "## Develop\n\n```sh\npixi run qa\n```\n\n## Try it\n\n```sh\npixi install\n```",
    )
    _readme(write, tmp_path, swapped)
    result = run("house_style.py", "skeleton", "README.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "out of order" in result.stdout


def test_a_contributing_h1_must_name_the_document(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    write(tmp_path, "CONTRIBUTING.md", CONTRIBUTING.replace("# Contributing to thing", "# Notes"))
    result = run("house_style.py", "contributing", "CONTRIBUTING.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "Contributing to <repository>" in result.stdout


def test_a_commands_section_without_a_table_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    broken = CONTRIBUTING.replace(
        "| Command | Purpose |\n| :-- | :-- |\n| `pixi run qa` | the whole gate |\n",
        "Run the gate.\n",
    )
    write(tmp_path, "CONTRIBUTING.md", broken)
    result = run("house_style.py", "contributing", "CONTRIBUTING.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "carries no table" in result.stdout


def test_a_missing_contributing_section_is_reported(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    broken = CONTRIBUTING.replace("## Commits\n\nUse Conventional Commits.\n", "")
    write(tmp_path, "CONTRIBUTING.md", broken)
    result = run("house_style.py", "contributing", "CONTRIBUTING.md", cwd=tmp_path)
    assert result.returncode == 1
    assert "no `## Commits` section" in result.stdout


def test_an_unknown_mode_is_a_usage_error(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    _readme(write, tmp_path)
    result = run("house_style.py", "loud", "README.md", cwd=tmp_path)
    assert result.returncode == 2
    assert "usage:" in result.stderr


def test_a_missing_file_is_a_usage_error(run: Run, tmp_path: pathlib.Path) -> None:
    result = run("house_style.py", "readme", "nope.md", cwd=tmp_path)
    assert result.returncode == 2
    assert "missing" in result.stderr
