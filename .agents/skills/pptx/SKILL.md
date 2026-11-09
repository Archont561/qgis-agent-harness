---
name: pptx
description: Build, inspect and debug PowerPoint decks in this repo — especially decks that contain equations, where a slide can look perfect in PowerPoint and blank everywhere else. Use this skill whenever a .pptx is created, edited, rendered or checked, whenever a formula has to sit on a slide as an editable equation or as a picture, whenever a deck or a DOCX comes out blank in a previewer, LibreOffice or Word, and whenever someone mentions python-pptx, easypptx, OMML, a14:m, "editable equation", or asks why a slide is empty.
---

# pptx

Two libraries are in the env — `python-pptx` and `easypptx` — and neither has an equation API. That
is the whole subject of this skill: a deck is easy, a deck with maths is a compatibility problem.

`easypptx` is a thin wrapper and hands you python-pptx objects (`Slide.pptx_slide`, and `add_text()`
returns a real `pptx.shapes.autoshape.Shape`), so everything below applies to both. Note
`add_text(text, x=, y=, width=, height=)` takes percentages or `in_()`; `left=`/`top=` are ignored
with a warning.

## The equation has two possible lives

| Form | How it is stored | Who sees it |
|---|---|---|
| **Editable** | `<a14:m><m:oMathPara><m:oMath>…` inside an `a:p` | PowerPoint yes, LibreOffice yes, **every previewer no** — the slide is blank |
| **Picture** | a normal image part under `ppt/media` | everything, everywhere — but uneditable |

A deck with the first form and no `ppt/media` part **is a blank deck** in any preview, any web
viewer, any `python-pptx` text dump. That is not a bug to investigate; it is the format.

So decide per deck: a defence deck that must survive a projector gets the picture; a deck the
examiner will edit gets OMML; `pixi run render omml-slide` (in `.agents/skills/archont561-render/`) writes both branches with
`mc:AlternateContent` (works in PPTX; a dead construct in DOCX — Writer drops it).

## Putting OMML on a slide

```python
from omml import add_equation                     # commands/omml.py, on sys.path already
add_equation(box.text_frame.paragraphs[0], r"\text{MDE} = 3.42\sqrt{\tau^2 + \frac{4950}{r}}")
```

`add_equation` detects the host from the paragraph (DrawingML vs WordprocessingML), so the same call
works on a python-pptx and a python-docx paragraph. `display=False` gives inline maths
(`a14:m` > `m:oMath` with no `m:oMathPara`). `backend="mathml"` swaps pandoc out for the pypi pair.

If you insert the XML yourself, three things decide whether PowerPoint opens the file or offers to
repair it:

- declare `xmlns:a14` and `xmlns:m` **on the inserted element**; a declaration on the document root
  does not survive the part rewrite;
- insert before `a:endParaRPr`, not blindly at the end of `a:p`;
- the OMML must be complete — `m:rad` needs `m:deg` *or* `m:degHide`, `m:f` needs num and den,
  `m:nary` needs sub, sup and e. A missing `m:deg` is drawn as "√⍰" with the radicand gone.

`omml.REQUIRED_CHILDREN` is the checklist the module already enforces; keep it that way.

## The picture branch

```python
from omml import equation_picture
png = equation_picture(r"\frac{a}{b}", Path("build"), dpi=600)   # cropped, transparent
slide.shapes.add_picture(str(png), Inches(0.9), Inches(1.6), height=Inches(0.55))
```

600–900 ppi, transparent, cropped to the ink. Set the **height** and let the width follow, so two
formulas typeset at the same size look the same size on the slide.

## Verifying a deck — the only test that counts

Saving successfully proves nothing. Open the file and count what is inside it:

```bash
python3 -c "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); \
print([n for n in z.namelist() if n.startswith('ppt/media')] or 'NO PICTURE — blank outside PowerPoint')" deck.pptx
```

Then look at it: `soffice --headless --convert-to pdf deck.pptx` and rasterise the PDF. Two missing
packages produce false alarms worth an hour each:

- **`libreoffice-impress`** — without it the deck itself will not load (`Error: source file could not
  be loaded`), which reads like a corrupt file.
- **`libreoffice-math`** — without it the file converts happily and every equation is *empty space*,
  in the OMML branch and in a perfectly good pandoc DOCX alike.

Check both with `dpkg -l libreoffice-impress libreoffice-math` before concluding that the deck is
broken.

`soffice` must run through `start_process` with a fresh `-env:UserInstallation=file:///tmp/lo-profile`;
a second concurrent call on the same profile silently does nothing.

## Reopening and inspecting

`Presentation(path)` round-trips, and `python-pptx` keeps unknown markup intact, so
`paragraph._p.xml` is the honest view of what you wrote. Useful greps on the raw part: `<a14:m>` for
the editable equation, `<p:pic>` for a picture, `mc:AlternateContent` for the hybrid, `ppt/media` for
whether anything is drawable at all.

## References

- `references/omml-recipes.md` — the verbatim insertion snippet, the hybrid XML, the verification
  one-liners, and the reader-compatibility matrix that came out of testing Word, Writer, LibreOffice
  and two previewers.
