---
id: doc-4
title: 'Specification of `experiment/`: the instrument code'
type: specification
created_date: '2026-11-07T19:53:00Z'
updated_date: '2026-11-07T20:09:00Z'
---
A pointer, not a copy. The instrument code is written in `experiment/`; the source of truth for the design are the notes in `thesis/`.

## Modules and their tasks

| Module | What it does | Task |
|---|---|---|
| cards | YAML -> card object, schema validation | TASK-15 |
| register | JSONL writing, 13 fields, validation at write time | TASK-16 |
| CLI | `matrix` / `run` / `score` | TASK-17 |
| sandbox | run isolation, turn limit, seed determinism | TASK-18 |
| MCP server | 9 operations, gates N1/N4, handle with georeferencing | TASK-5 |
| code arm | PyQGIS + parity table | TASK-6 |
| harness | pinned loop, two loop implementations, budget | TASK-7 |
| oracle | predicates with tolerances, deterministic verdict | TASK-2 |

## Contracts that must not change after G1

- **Run record:** 13 fields, including `run_id`, `stop_reason`, `detected_by`, `artifact_hash` - a run without `stop_reason` is void, not zero.
- **Handle:** `{handle, crs, transform, nodata, dtype, shape}` - an intermediate result carries its georeferencing, because the array does not.
- **Parity:** every catalogue operation has a library equivalent with a version; the same script yields the same artefact hash in both arms.

## Constraints

QGIS 3.44 (LTR), Python 3.12, a budget of 30 turns per run, one seed per run, no network during a run. The language model, the SDK version and the protocol revision are pinned in `pixi.toml` and in the pre-registration.

## Further reading

`thesis/design/runs.md` · `thesis/design/harness.md` · `thesis/design/tool-surface.md` · `thesis/writing/key-concepts.md` · `experiment/README.md` · the pre-registration (TASK-1).
