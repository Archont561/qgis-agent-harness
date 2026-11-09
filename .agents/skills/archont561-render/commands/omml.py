#!/usr/bin/env python3
"""LaTeX maths -> OMML, as a function. No slide, no deck, no Office, no TeX.

    from omml import latex_to_omml

    omml = latex_to_omml(r"\\frac{a}{b}")     # '<m:oMath>…</m:oMath>'

That is the whole contract: a LaTeX string in, an OMML string out. OMML (Office Math Markup
Language) is what Word and PowerPoint actually store for an equation, so the result can be dropped
into a DOCX or a PPTX and stays editable there.

Between the string and the slide sit four things worth knowing:

* **pandoc is the converter.** ``pandoc -f latex -t docx`` writes the OMML Word itself consumes, and
  the ``m:oMath`` element is lifted out of the throwaway document. The older
  ``latex2mathml`` → ``mathml2omml`` pair is not used: it omitted the ``m:deg`` a square root
  requires (the radicand then vanished and the root drew as "√⍰") and it emitted markup for
  ``\\bar``/``\\vec`` that does not close.
* **Two repairs are still applied**, because they cost nothing and catch a regression:
  ``normalise_omml`` inserts a missing ``m:deg``, and ``REQUIRED_CHILDREN`` refuses to return an
  equation missing a child the schema requires (``m:f`` without ``m:den``, and so on).
* **OMML is only drawn by Office and by LibreOffice.** A DOCX preview built on a docx→HTML
  converter (mammoth, docx-preview — what most web previews use) keeps the prose and drops the
  equation silently; verified: mammoth turned a document with two equations into one paragraph of
  text and nothing else. ``equation_picture`` renders the same LaTeX to a PNG for those cases —
  ``equation_picture(latex, workdir)``, then ``run.add_picture(path)``. Word keeps the equation,
  the picture keeps the preview: pick per document.
* **The wrapper depends on the host.** PowerPoint wants ``<a14:m>`` around the maths inside a
  DrawingML paragraph; Word wants the maths bare inside a ``w:p``. ``pptx_equation`` and
  ``docx_equation`` return the right one, and ``add_equation`` picks it from the paragraph you hand
  it, so the same call works on a python-pptx and a python-docx paragraph alike.
* **Results are cached per string.** pandoc is a subprocess, so a repeated formula is converted once
  per process; elements are re-parsed per call, because lxml elements are mutable and an equation
  element can only sit in one place in a tree.

Write maths both typesetters agree on if a picture of the same formula will sit beside it:
``4950/r`` is a slash, ``\\frac{4950}{r}`` is a stacked fraction, and ``\\text{MDE}`` gives one
upright run where ``\\mathrm{MDE}`` gives a run per letter.

Run inside the renderers environment (pandoc lives there)::

    pixi run render omml '\\frac{a}{b}'            # print the OMML
    pixi run render omml '\\sqrt{x}' --format docx  # Word's wrapper
"""

from __future__ import annotations

import argparse
import functools
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree

# The dispatcher imports command modules by file path, so this directory is not on sys.path; the
# pandoc-free backend below is a sibling module and is found only because of this line.
sys.path.insert(0, str(Path(__file__).resolve().parent))

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
A14_NS = "http://schemas.microsoft.com/office/drawing/2010/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

__all__ = [
    "add_equation",
    "docx_equation",
    "equation_picture",
    "latex_to_omml",
    "omml_element",
    "pptx_equation",
]

# Required children of every OMML construct this toolchain can emit. Elements are required even
# when empty (an empty m:deg means "square root"), which is what the retired converter got wrong.
REQUIRED_CHILDREN: dict[str, tuple[str, ...]] = {
    "rad": ("deg", "e"),
    "f": ("num", "den"),
    "sSup": ("e", "sup"),
    "sSub": ("e", "sub"),
    "sSubSup": ("e", "sub", "sup"),
    "nary": ("sub", "sup", "e"),
    "func": ("fName", "e"),
    "limLow": ("e", "lim"),
    "limUpp": ("e", "lim"),
    "bar": ("e",),
    "acc": ("e",),
    "box": ("e",),
    "d": ("e",),
    "eqArr": ("e",),
    "groupChr": ("e",),
}


def _m(tag: str) -> str:
    return f"{{{MATH_NS}}}{tag}"


def normalise_omml(document_xml: bytes) -> etree._Element:
    """Pull the first ``m:oMath`` out of a DOCX body, repair it, refuse it if still invalid."""
    body = etree.fromstring(document_xml)
    maths = body.findall(".//" + _m("oMath"))
    if not maths:
        raise ValueError("no OMML in pandoc's DOCX — is the formula really in math mode?")
    root = maths[0]

    for rad in root.iter(_m("rad")):
        if rad.find(_m("deg")) is not None:
            continue
        rad_pr = etree.Element(_m("radPr"))
        etree.SubElement(rad_pr, _m("degHide")).set(_m("val"), "1")
        rad.insert(0, rad_pr)
        rad.insert(1, etree.Element(_m("deg")))

    missing = [
        f"{tag} lacks {', '.join(gone)}"
        for tag, kids in REQUIRED_CHILDREN.items()
        for el in root.iter(_m(tag))
        if (gone := [k for k in kids if el.find(_m(k)) is None])
    ]
    if missing:
        raise ValueError("OMML still invalid after repair: " + "; ".join(missing))
    # The subtree inherits pandoc's w:, r:, o:, v: declarations from the document root, and lxml
    # re-emits them. Rebuilding the root with the one namespace an equation needs drops them.
    clean = etree.Element(_m("oMath"), nsmap={"m": MATH_NS})
    clean.attrib.update(root.attrib)
    clean.extend(list(root))
    return clean


def latex_to_omml(latex: str, *, backend: str = "pandoc") -> str:
    """LaTeX -> a schema-valid ``<m:oMath>`` as a string. The rest of this module builds on it.

    ``backend="pandoc"`` is the default and the more capable one: pandoc's LaTeX reader knows
    ``align``, ``cases``, mathtools environments and macro definitions. ``backend="mathml"`` runs
    ``mathml_omml.latex_to_omml`` instead — no pandoc, no subprocess, two small pypi packages — and
    matches pandoc on the core amsmath subset; reach for it when the binary is the problem, not the
    formula.
    """
    if backend == "pandoc":
        return _latex_to_omml_pandoc(latex)
    if backend == "mathml":
        from mathml_omml import latex_to_omml as maths_only  # sibling script: no pandoc

        return maths_only(latex)
    raise ValueError(f"unknown backend {backend!r}: use 'pandoc' or 'mathml'")


@functools.lru_cache(maxsize=256)
def _latex_to_omml_pandoc(latex: str) -> str:
    """The pandoc half: a throwaway DOCX, and the ``m:oMath`` lifted out of it."""
    with tempfile.TemporaryDirectory(prefix="omml-") as tmp:
        tex = Path(tmp) / "equation.tex"
        docx = Path(tmp) / "equation.docx"
        tex.write_text(f"\\[{latex}\\]\n")
        try:
            subprocess.run(
                ["pandoc", "-f", "latex", "-t", "docx", str(tex), "-o", str(docx)],
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("pandoc is not on PATH — run in the renderers env") from exc
        except subprocess.CalledProcessError as exc:
            raise ValueError(f"pandoc rejected the formula: {exc.stderr.strip()}") from exc
        with zipfile.ZipFile(docx) as archive:
            body = archive.read("word/document.xml")
    return etree.tostring(normalise_omml(body), encoding="unicode")


def omml_element(latex: str, *, backend: str = "pandoc") -> etree._Element:
    """The same equation as a fresh lxml element — mutate or move it without harming the cache."""
    return etree.fromstring(latex_to_omml(latex, backend=backend))


def pptx_equation(latex: str, *, display: bool = True, backend: str = "pandoc") -> etree._Element:
    """``a14:m`` > ``m:oMathPara`` > ``m:oMath`` (display) — the wrapper PowerPoint writes."""
    wrapper = etree.Element(f"{{{A14_NS}}}m", nsmap={"a14": A14_NS, "m": MATH_NS})
    maths = omml_element(latex, backend=backend)
    if display:
        etree.SubElement(wrapper, _m("oMathPara")).append(maths)
    else:
        wrapper.append(maths)
    return wrapper


def docx_equation(latex: str, *, display: bool = True, backend: str = "pandoc") -> etree._Element:
    """``m:oMathPara`` > ``m:oMath`` (display) or bare ``m:oMath`` (inline), for a ``w:p``."""
    maths = omml_element(latex, backend=backend)
    if not display:
        return maths
    para = etree.Element(_m("oMathPara"), nsmap={"m": MATH_NS})
    para.append(maths)
    return para


def add_equation(
    paragraph, latex: str, *, display: bool = True, backend: str = "pandoc"
) -> etree._Element:
    """Append the equation to a python-pptx *or* python-docx paragraph; the host is detected.

    ``paragraph`` is what ``shape.text_frame.paragraphs[0]`` or ``document.add_paragraph()`` gives
    you. Returns the element it appended, so a caller can position or inspect it.
    """
    host = "pptx" if paragraph._p.tag.startswith(f"{{{DRAWING_NS}}}") else "docx"
    element = (
        pptx_equation(latex, display=display, backend=backend)
        if host == "pptx"
        else docx_equation(latex, display=display, backend=backend)
    )
    paragraph._p.append(element)
    return element


def equation_picture(latex: str, workdir: Path, *, dpi: int = 600, size: int = 22) -> Path:
    """Render the same LaTeX to a cropped, transparent PNG and return its path.

    For hosts that cannot draw OMML: a DOCX preview (mammoth, docx-preview) and any reader that is
    not Office or LibreOffice will show a gap where the equation is. Insert the PNG with whatever
    the document library offers — ``run.add_picture(path, width=…)``, ``shapes.add_picture(…)`` —
    and the formula appears there at 600 ppi, uneditable, which is the trade.

    Needs typst and PDFium, i.e. the renderers env, and the sibling ``math_slide`` script.
    """
    from math_slide import render  # sibling script: LaTeX -> typst -> PDF -> cropped PNG

    _, png = render(latex, Path(workdir), size=size, mode="raster", dpi=dpi)
    return png


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LaTeX -> OMML, printed (no slide, no document)")
    ap.add_argument("latex", help="the formula, e.g. '\\frac{a}{b}'")
    ap.add_argument(
        "--format",
        choices=("raw", "pptx", "docx"),
        default="raw",
        help="raw m:oMath (default), or wrapped for a PPTX / DOCX paragraph",
    )
    ap.add_argument("--inline", action="store_true", help="inline instead of display maths")
    ap.add_argument(
        "--backend",
        choices=("pandoc", "mathml"),
        default="pandoc",
        help="pandoc (default) or the pypi pair in ``mathml_omml.py``, which needs no pandoc",
    )
    args = ap.parse_args(argv)

    if args.format == "raw":
        print(latex_to_omml(args.latex, backend=args.backend))
    else:
        wrapper = pptx_equation if args.format == "pptx" else docx_equation
        built = wrapper(args.latex, display=not args.inline, backend=args.backend)
        print(etree.tostring(built, encoding="unicode"))
    return 0


def command(ctx, argv: list[str]) -> int:
    """archont561 entry point for ``omml``."""
    return main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
