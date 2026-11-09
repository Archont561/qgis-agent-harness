---
name: typst
description: Typeset maths, figures and pages to PDF/SVG with typst in this repo, and convert LaTeX to typst maths without surprises. Use this skill whenever a formula, equation, chart or one-page document has to become a PDF or a picture, whenever a .typ file is compiled or debugged, whenever LaTeX has to reach typst or a slide/DOCX needs a vector formula image, and whenever someone says "typst", "typst compile", "PDF maths", "render the formula", or asks why a radical, accent or matrix came out wrong.
---

# typst

Typst is the typesetter this repo uses for anything that must not be laid out by hand: formula
pictures on a slide, one-off PDFs, figures. It is pinned at **0.15.1** in the `renderers` env and it
is a compiler, not a Python library — every call is a subprocess inside `pixi run -e renderers`.

Two different jobs wear the same name here, and mixing them up is the usual source of wasted time:

| Job | Input | Path |
|---|---|---|
| **Formula picture for Office** | LaTeX written for the thesis | `pixi run render math-slide` (the `archont561-render` skill) → `latex_to_typst()` → compile → PDF → PDFium → transparent PNG |
| **A page or figure as an artefact** | your own typst markup | write `.typ`, `typst compile --format pdf` |

## Compile the PDF, never the PNG

`typst compile --format png` drops the radical's vinculum and mis-measures the page height, so a
square root comes out as a bare "√" and the crop is wrong. Always export **PDF** and rasterise it:

```bash
pixi run -e renderers typst compile --format pdf figure.typ figure.pdf
pixi run -e renderers python -c "import pypdfium2 as p; d=p.PdfDocument('figure.pdf'); \
d[0].render(scale=300/72).to_pil().save('figure.png')"   # 300 ppi
```

`scale = dpi / 72`. For a transparent PNG (what a slide wants over a coloured background) pass a
non-opaque fill colour to PDFium; a white box otherwise arrives with the picture.

## A page that fits its contents

For a standalone formula the page is the frame, so size it and then crop to the ink:

```typst
#set page(width: auto, height: 5cm, margin: 12pt, fill: none)
#set text(size: 22pt)
$ frac(a, b) $
```

`height: auto` clips a built-up fraction's denominator, and a 1–2 pt margin clips the numerator —
hence the fixed 5 cm and the 12 pt margin, with a crop to `Image.getbbox()` afterwards. Do not
"fix" a clipped formula by shrinking the maths; fix the page.

## Converting LaTeX

`math-slide`'s `latex_to_typst(latex)` (in `.agents/skills/archont561-render/commands/math_slide.py`) runs `pandoc -f latex -t typst` with the formula in
`$…$` and returns typst maths including its own delimiters. Use it rather than hand-translating:
pandoc is the only converter here that knows matrices, `align`, `cases` and accents.

**The failure to watch for is silent.** When pandoc does not recognise a macro it hands the LaTeX
back as *plain text*; nothing raises and the picture shows a monospace `\textcolor{blue}{x}`. When
you convert anything that came from a document, check the result starts with `$` before compiling.
Nineteen commands are known to fall back — see `references/latex-coverage.md` before assuming a
formula converted cleanly.

Two things inside `latex_to_typst` are load-bearing and easy to delete by accident:

- `mat(delim: "||")` — pandoc's output for `vmatrix`/`Vmatrix` — **fails to compile**, because
  typst's `delim:` takes exactly one character. `_one_char_delim` rewrites it to `‖` (U+2016).
- pandoc escapes `/` to `\/` on purpose: in typst a bare `/` builds a fraction, in LaTeX it does not.

## Write maths that both typesetters agree on

A formula on a slide can be drawn by typst *and* stored as OMML in the same deck. Since the two
engines are different, the LaTeX has to mean the same thing to both:

- `\text{MDE}` gives one upright run. `\mathrm{MDE}` gives a run per letter and reads "M D E".
- `4950/r` is a slash in both. `\frac{4950}{r}` is a stacked fraction in both. Pick deliberately.

## Authoring typst directly

Fine for one-offs nobody will edit — a specimen page, a hand-tuned figure, a poster. It is not a
route for thesis formulas, because the same LaTeX has to feed the editable equation as well; two
syntaxes per formula is one syntax too many.

Things that bite when you write typst by hand:

- **Markup eats backslashes.** `\color` in prose disappears; wrap LaTeX in backticks — `` `\color` ``
  — or `#raw("\\color")`.
- Generating `.typ` from Python: use `"` for string literals (Python's `repr` gives `'`) and double
  backslashes exactly once. Double-escaping is the usual cause of `error: the character '\' is not
  valid in code`.
- Check the page count, not just the exit code: `len(pypdfium2.PdfDocument(pdf))`. A footnote that
  spills onto page 2 is a layout bug, and an empty second page is the commonest one.

## Verify visually, always

A `.typ` that compiles is not a `.typ` that is right. After compiling, rasterise the page and look
at it — fractions, radicals, matrices, accents and `cases` all fail in ways the compiler accepts.
For a formula picture, the equivalent check is the PNG itself: something must be non-blank and the
margins must be tight.

## References

- `references/latex-coverage.md` — what survives LaTeX → typst, the 19 commands that fall back to raw
  text, what degrades silently, and the probe numbers behind the table. Read it before converting a
  formula whose source you did not write.
