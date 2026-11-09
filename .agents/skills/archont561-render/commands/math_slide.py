#!/usr/bin/env python3
"""Typeset LaTeX maths once, as a PDF, and put a picture of it on a PowerPoint slide.

Why a picture rather than a live equation: a PPTX can only hold equations as OMML, and OMML is
displayed by PowerPoint and by almost nothing else — LibreOffice Impress and every previewer built
on it draw nothing at all (verified: blank slide under both the ``a14:m`` wrapper and a bare
``m:oMath``). A picture is displayed everywhere. ``omml_slide.py`` (the ``omml-slide`` command)
remains the route for a deck that will be edited in PowerPoint; this command is the route for a
deck that has to *look right*
wherever it is opened, at a quality that survives print.

The chain::

    LaTeX --pandoc--> typst math --typst--> PDF (the vector master, keep it)
                                       |--svg--> EMF  (vector, scales without blur)
                                       |--png--> 600 ppi raster (when EMF is not wanted)

The **raster is the default** on purpose. EMF is a better picture — vector, sharp at any zoom and in
print — but python-pptx 1.0.2 stores an EMF part as ``image/x-wmf`` and cannot read its own file
back (PIL has no metafile reader), so a deck with EMF maths can be *written* once and never reopened
or appended to. A 900 ppi PNG survives every reader and every later edit. Ask for ``--mode vector``
when the deck is a single pass and print quality matters more than being able to change it.

Usage, from the repository root::

    pixi run render math-slide '\\frac{a}{b}' -o slide.pptx
    pixi run render math-slide '\\sum_{i=1}^{n} x_i^2' --mode raster
    pixi run render math-slide '\\hat{y}=\\beta_0' --deck defence.pptx
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

# A fixed, generous page + a crop to the ink afterwards, because typst 0.15 mis-measures the page
# height of a built-up fraction: `height: auto` clips the denominator. Width stays automatic. The
# margin must stay well clear of 1 pt as well — a tall fraction overflows its line box upwards, and
# at a hairline margin the page top clips the numerator and the radical's vinculum.
TYPST_PAGE = """\
#set page(width: auto, height: 5cm, margin: 12pt, fill: none)
#set text(size: {size}pt)
{math}
"""


def _run(cmd: list[str], **kw: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


_MULTI_CHAR_DELIM = re.compile(r'delim: "([^"]{2,})"')


def _one_char_delim(match: re.Match[str]) -> str:
    """typst's ``mat(delim:)`` takes exactly one character — pandoc writes ``"||"`` for vmatrix."""
    chars = match.group(1)
    if set(chars) == {"|"}:
        return 'delim: "\u2016"'  # U+2016 double vertical line, the vmatrix's own bars
    raise ValueError(f"typst cannot express the delimiter {chars!r}: it takes one character")


def latex_to_typst(latex: str) -> str:
    """LaTeX math -> typst math, via pandoc. Keeps matrices, align and accents working."""
    out = _run(["pandoc", "-f", "latex", "-t", "typst"], input=f"${latex}$")
    # pandoc escapes the slash as ``\/`` on purpose: in typst ``/`` builds a fraction, in LaTeX it
    # does not. Left alone, both branches of a hybrid slide agree; ``\frac`` asks for a fraction.
    return _MULTI_CHAR_DELIM.sub(_one_char_delim, out.stdout.strip())


def render(latex: str, workdir: Path, *, size: int, mode: str, dpi: int) -> tuple[Path, Path]:
    """Write the PDF master and the picture; return (pdf, picture)."""
    workdir.mkdir(parents=True, exist_ok=True)
    src = workdir / "formula.typ"
    src.write_text(TYPST_PAGE.format(size=size, math=latex_to_typst(latex)))

    pdf = workdir / "formula.pdf"
    _run(["typst", "compile", "--format", "pdf", str(src), str(pdf)])

    if mode == "vector":
        svg = workdir / "formula.svg"
        _run(["typst", "compile", "--format", "svg", str(src), str(svg)])
        emf = workdir / "formula.emf"
        profile = workdir / "lo-profile"
        _run(
            [
                "soffice",
                f"-env:UserInstallation=file://{profile}",
                "--headless",
                "--norestore",
                "--convert-to",
                "emf",
                "--outdir",
                str(workdir),
                str(svg),
            ]
        )
        if not emf.exists():
            raise RuntimeError(f"LibreOffice produced no EMF for {svg}")
        return pdf, emf

    png = workdir / "formula.png"
    pdf_to_png(pdf, png, dpi=dpi)
    return pdf, png


def pdf_to_png(pdf: Path, png: Path, *, dpi: int) -> None:
    """Rasterise page 1 with PDFium and crop to the ink, so the slide gets no white box.

    typst's own ``--format png`` export drops the radical's vinculum and crops the page; the PDF is
    exact, so the PDF is what gets rasterised.
    """
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf))
    page = doc[0]
    # a non-opaque fill colour is what makes PDFium render into an alpha bitmap
    bitmap = page.render(scale=dpi / 72, fill_color=(255, 255, 255, 0))
    image = bitmap.to_pil().convert("RGBA")
    bbox = image.getbbox()
    if bbox:
        pad = 4
        left, top, right, bottom = bbox
        image = image.crop((max(left - pad, 0), max(top - pad, 0), right + pad, bottom + pad))
    image.save(png)


def add_slide(deck: Path, picture: Path, *, title: str | None, height_in: float) -> None:
    prs = Presentation(deck) if deck.exists() else Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    top = Inches(0.6)
    if title:
        box = slide.shapes.add_textbox(Inches(0.6), top, Inches(9), Inches(0.8))
        box.text_frame.text = title
        box.text_frame.paragraphs[0].runs[0].font.size = Pt(28)
        top = Inches(1.7)
    slide.shapes.add_picture(str(picture), Inches(0.9), top, height=Inches(height_in))
    prs.save(deck)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LaTeX -> PDF -> picture on a PPTX slide")
    ap.add_argument("latex", help="the formula in LaTeX, e.g. '\\frac{a}{b}'")
    ap.add_argument("-o", "--out", type=Path, default=Path("math-slide.pptx"))
    ap.add_argument("--deck", type=Path, help="append to an existing deck instead of a new one")
    ap.add_argument("--title", help="slide title")
    ap.add_argument("--mode", choices=("vector", "raster"), default="raster")
    ap.add_argument("--dpi", type=int, default=900, help="raster resolution (default 900)")
    ap.add_argument("--size", type=int, default=22, help="typographic size in points (default 22)")
    ap.add_argument("--height", type=float, default=0.6, help="picture height in inches (0.6)")
    ap.add_argument(
        "--keep",
        type=Path,
        help="where to keep the PDF master (default: <out>-formula/ beside the deck)",
    )
    args = ap.parse_args(argv)

    for tool in ("pandoc", "typst"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not on PATH — run with `pixi run -e renderers python …`")

    mode = args.mode
    if mode == "vector" and not shutil.which("soffice"):
        print("soffice not found: falling back to the raster", file=sys.stderr)
        mode = "raster"

    out = args.deck or args.out
    work = args.keep or out.parent / f"{out.stem}-formula"
    work.mkdir(parents=True, exist_ok=True)
    pdf, picture = render(args.latex, work, size=args.size, mode=mode, dpi=args.dpi)
    add_slide(out, picture, title=args.title, height_in=args.height)
    print(f"{out}  ({mode}: {picture.name}, {picture.stat().st_size // 1024} kB; pdf: {pdf})")
    return 0


def command(ctx, argv: list[str]) -> int:
    """archont561 entry point for ``math-slide``."""
    return main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
