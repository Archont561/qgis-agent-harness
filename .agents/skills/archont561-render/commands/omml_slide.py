#!/usr/bin/env python3
"""Put a *live* PowerPoint equation (OMML) on a slide, without TeX and without Office.

The conversion itself is *not* here: ``omml.py`` (the ``omml`` command) owns it, as a function any
host can call (``from omml import add_equation``). This module is only the slide around it.

The chain, and why each step exists::

    LaTeX  --pandoc-->  DOCX with OMML  --extract m:oMath-->  OMML  --a14:m-->  PPTX

A PPTX cannot carry MathML and stores equations as OMML (Office Math Markup Language), wrapped for
DrawingML in ``<a14:m><m:oMathPara>``. PowerPoint itself writes exactly that wrapper, which is why
this is an injection into the text frame rather than an image: the result stays an equation the
recipient can edit, re-style and renumber in PowerPoint.

**A live equation is invisible outside PowerPoint**, because no other reader implements the OMML
import — LibreOffice Impress draws nothing for it, under either wrapper. The cure is the one
PowerPoint itself uses when it saves such a slide, and it is applied here by default: the shape is
written as ``mc:AlternateContent``, with the equation in ``mc:Choice Requires="a14"`` and a
**picture of the same formula** in ``mc:Fallback``. PowerPoint reads the choice and gives back the
editable equation; a reader that cannot draw OMML takes the fallback and draws the picture. Verified
by rendering: written this way the formula appears in Impress, written with the bare ``a14:m`` it
does not.

Neither branch is a dependency on LibreOffice. The fallback picture is typeset with typst and
rasterised with PDFium, both inside the renderers environment; LibreOffice is only ever the tool
used to *look* at the result. See ``omml.py`` (the ``omml`` command) for the converter itself — the
repairs it applies and the wrapper each host wants are documented there.

One consequence of two branches: they are produced by different typesetters, so write maths they
agree on. ``4950/r`` is a slash — LaTeX's meaning — in both, while a built-up fraction needs
``\\frac{4950}{r}``; the typst side deliberately does not "improve" a slash into a fraction, because
PowerPoint would then show something else.

Run inside the renderers environment::

    pixi run render omml-slide '\\mathrm{MDE} = 3.42\\sqrt{\\tau^2}'
    pixi run render omml-slide '\\frac{a}{b}' -o eq.pptx --title "Proof"
    pixi run render omml-slide '\\frac{a}{b}' --no-fallback   # OMML only

For a page of aligned maths, let pandoc write a DOCX and copy the equations across: same OMML, a
longer road, and far more tolerant of ``align`` and matrices.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt

# Loaded by the dispatcher by file path, so this directory is not on sys.path; `omml` is the
# sibling module that owns the LaTeX -> OMML conversion.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from omml import add_equation

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
A14_NS = "http://schemas.microsoft.com/office/drawing/2010/main"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"


def picture_fallback(slide, box, latex: str, workdir: Path, height_in: float) -> None:
    """Wrap the equation shape in ``mc:AlternateContent``, with a picture as the fallback branch.

    Same construction PowerPoint writes when it saves a slide carrying an equation: readers that
    cannot draw ``a14:m`` fall through to ``mc:Fallback`` and see a picture instead of an empty box.
    """
    from math_slide import render  # sibling script: LaTeX -> PDF -> cropped, transparent PNG

    _, png = render(latex, workdir, size=22, mode="raster", dpi=900)
    pic = slide.shapes.add_picture(str(png), box.left, box.top, height=Inches(height_in))

    alt = etree.Element(
        f"{{{MC_NS}}}AlternateContent", nsmap={"mc": MC_NS, "a14": A14_NS, "m": MATH_NS}
    )
    slide.shapes._spTree.append(alt)  # python-pptx has no API for a raw shape element
    choice = etree.SubElement(alt, f"{{{MC_NS}}}Choice")
    choice.set("Requires", "a14")
    fallback = etree.SubElement(alt, f"{{{MC_NS}}}Fallback")
    choice.append(box._element)
    fallback.append(pic._element)


def build(
    latex: str,
    out: Path,
    title: str | None = None,
    *,
    fallback: bool = True,
    height_in: float = 0.6,
) -> Path:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    top = Inches(0.6)
    if title:
        caption = slide.shapes.add_textbox(Inches(0.6), top, Inches(9), Inches(0.8))
        caption.text_frame.text = title
        caption.text_frame.paragraphs[0].runs[0].font.size = Pt(28)
        top = Inches(1.6)

    box = slide.shapes.add_textbox(Inches(0.6), top, Inches(9), Inches(1.5))
    add_equation(box.text_frame.paragraphs[0], latex)
    if fallback:
        picture_fallback(slide, box, latex, out.parent / f"{out.stem}-formula", height_in)
    prs.save(out)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LaTeX -> OMML equation on a PPTX slide")
    ap.add_argument("latex", help="the formula, e.g. 'x^2 + 1'")
    ap.add_argument("-o", "--out", type=Path, default=Path("equation.pptx"))
    ap.add_argument("--title", help="optional slide title")
    ap.add_argument(
        "--fallback",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="also write a picture of the formula as the mc:Fallback branch (default: on)",
    )
    ap.add_argument("--height", type=float, default=0.6, help="fallback picture height (0.6 in)")
    args = ap.parse_args(argv)
    if not args.fallback:
        print(
            "warning: no picture fallback — this deck is drawn by PowerPoint only and will show "
            "an empty box in LibreOffice, in a preview pane and in any docx/pptx→HTML converter",
            file=sys.stderr,
        )
    print(build(args.latex, args.out, args.title, fallback=args.fallback, height_in=args.height))
    return 0


def command(ctx, argv: list[str]) -> int:
    """archont561 entry point for ``omml-slide``."""
    return main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
