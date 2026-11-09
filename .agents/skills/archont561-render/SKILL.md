---
name: archont561-render
description: Render LaTeX maths and thesis artefacts inside this repo's renderers environment — a formula as an editable OMML equation in a PPTX or DOCX, as a picture on a slide, or as pandoc-free OMML via the pypi pair. Use this skill whenever an equation has to reach a deck, a document or a PNG, whenever a slide shows a blank box where maths should be, and whenever someone asks to render, typeset or place a formula.
license: MIT
metadata:
  author: Archont561
  version: "1.0.0"
  namespace: archont561
---

# archont561-render

The rendering commands of this repository are **skill commands**, not loose scripts: the
`archont561` runtime discovers `commands/*.py` here and dispatches `pixi run render <command>`.
Each command module follows the runtime contract `def command(ctx, argv) -> int` and is also
runnable on its own (`python commands/math_slide.py …`) for debugging.

## Commands

| Command | Produces | Module |
| :-- | :-- | :-- |
| `math-slide` | a picture of the formula on a PowerPoint slide (typst → PDF → PNG/EMF) | `commands/math_slide.py` |
| `omml-slide` | a *live* equation on a slide, wrapped in `mc:AlternateContent` with a picture fallback | `commands/omml_slide.py` |
| `omml` | the OMML itself, raw or wrapped for a PPTX/DOCX paragraph | `commands/omml.py` |
| `mathml-omml` | the same OMML with no pandoc, via `latex2mathml` → `mathml2omml` | `commands/mathml_omml.py` |

Everything must run in the **renderers** environment, which is what `pixi run render` resolves to:

```bash
pixi run render math-slide '\frac{a}{b}' -o slide.pptx
pixi run render omml-slide '\mathrm{MDE} = 3.42\sqrt{\tau^2}' -o eq.pptx --title "MDE"
pixi run render omml '\sqrt{x}' --format docx
pixi run render mathml-omml '\frac{a}{b}'
pixi run render list          # the runtime's own command list
```

## Which route to pick

- **A deck that must look right anywhere** → `math-slide`. No previewer, LibreOffice or PDF export
  draws OMML, so a picture is the only form that survives.
- **A deck that will be edited in PowerPoint** → `omml-slide`. PowerPoint gets the editable
  equation, everyone else gets the picture through `mc:Fallback`.
- **A document (DOCX) or a bare equation** → `omml` (pandoc backend) or `mathml-omml` (no pandoc,
  two small pypi packages).
- **Write maths both typesetters agree on** when a picture and an equation sit side by side:
  `4950/r` is a slash in both, a built-up fraction needs `\frac{4950}{r}`, and `\text{MDE}` gives one
  upright run where `\mathrm{MDE}` gives one per letter.

The measured details — the seven repairs `mathml-omml` applies, why `typst compile --format png`
drops the radical's vinculum, why EMF cannot be reopened by python-pptx — stay in the module
docstrings they belong to, and in [docs/environments.md](../../../docs/environments.md).
