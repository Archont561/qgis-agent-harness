#!/usr/bin/env python3
"""LaTeX maths -> OMML without pandoc: ``latex2mathml`` -> ``mathml2omml``, with the gaps repaired.

    from mathml_omml import latex_to_omml
    omml = latex_to_omml(r"\\sqrt{x}")        # '<m:oMath>…</m:oMath>', same contract as `omml.py`

Why this file exists: pandoc is a 161 MB Haskell binary, and the slide pipeline used one converter
for two jobs. This is the pandoc-free half — the pair of small pypi packages, plus the seven repairs
they need. Measured against pandoc on 30 formulas: **30/30 produce schema-valid OMML**, 21/30 are
glyph-for-glyph identical, and the nine differences are spacing characters, Unicode styled letters
(double-struck R rather than ``m:scr``) and one relation codepoint. Rendered side by side
through LibreOffice the two sets are visually the same. What is *not* handled is anything pandoc's
LaTeX reader knows and ``latex2mathml`` does not; when a formula comes back wrong here, use the
pandoc backend (``omml.latex_to_omml(..., backend="pandoc")``).

The repairs, in the order they run:

1. **A bare ``&`` is not well-formed XML.** ``latex2mathml`` writes ``<mi>&</mi>`` for the alignment
   marker in ``aligned``, so *every* consumer of its output dies with a SAX parse error. It is
   swapped for a private-use sentinel before parsing, then put back as a literal ``&``, which is
   what Word reads as an alignment point.
2. **ASCII accents are invisible.** ``mathml2omml`` only recognises non-ASCII accent characters,
   and only when the ``<mover>`` is stretchy: ``\\hat{y}`` arrives as ``<mover accent="true">`` with
   ``^`` (U+005E) and comes out as two runs, ``y`` then ``^``. The character is replaced by the
   modifier letter (U+02C6), and both attributes are set.
3. **``mathml2omml``'s ``<mover>`` branch closes ``<m:groupChrPr>`` with ``</m:groupChr>``** — the
   markup cannot be parsed at all. A well-formed ``</m:groupChr>`` is never followed by ``<m:e>``,
   so the swap is unambiguous.
4. **``<msqrt>`` becomes ``<m:rad>`` with neither ``m:deg`` nor ``m:degHide``.** Word then draws
   "√⍰" and drops the radicand; a square root needs an explicit empty degree plus ``degHide``.
5. **An accent arrives as ``m:groupChr``**, a group character rather than an accent; Word writes
   ``m:acc`` for ``\\hat``, and so does the diagram that renders correctly.
6. **``\\lim``, ``\\max``, ``\\min``… arrive as ``m:sSub``.** LibreOffice draws that form with a red
   "¿" error mark; ``m:limLow`` — what pandoc emits — is drawn correctly.
7. **``m:box`` around every ``<mrow>``, and n-ary operators without ``subHide``/``supHide``.** The
   boxes are harmless in Word but make LibreOffice place an indexed radical's degree over the sign;
   without the two flags a sum's limits stay at the side instead of above and below.

``aligned`` gets one more thing: rows are split at the newline into ``m:eqArr``, the shape pandoc
emits, because ``latex2mathml`` flattens the environment into a single ``<mrow>`` and the rows would
otherwise run together into one line.

Run it where the two packages are installed (they are not in the default env)::

    pixi run render mathml-omml '\\frac{a}{b}'
"""

from __future__ import annotations

import argparse
import functools
import re
import xml.sax

import latex2mathml.converter as latex2mathml
import mathml2omml
from lxml import etree

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
MML_NS = "http://www.w3.org/1998/Math/MathML"


def _m(tag: str) -> str:
    return f"{{{MATH_NS}}}{tag}"


def _mml(tag: str) -> str:
    return f"{{{MML_NS}}}{tag}"


SENTINEL = "\ue000"  # private use: marks the alignment marker until the document parses
ACCENT_MAP = {"^": "\u02c6", "~": "\u02dc", "`": "\u02cb", "'": "\u00b4"}
# The modifier letters mathml2omml recognises, plus the arrows it treats as stretched accents.
ACCENT_CHARS = set("\u02c6\u00af\u02dc\u02d9\u00a8\u00b4\u02cb\u02c7\u02d8\u2192\u2190\u2194")
LIMIT_OPS = {"lim", "max", "min", "sup", "inf", "det", "gcd", "arg", "argmin", "argmax"}
ALIGNED = re.compile(r"\s*\\begin\{(?:aligned|align\*?|split|gathered)\}")

# Required children of every OMML construct these two packages can emit — the same table omml.py
# enforces, kept here so this module stands alone.
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
    "acc": ("e", "accPr"),
    "box": ("e",),
    "d": ("e",),
    "eqArr": ("e",),
    "groupChr": ("e",),
}


# ─────────────────────────────────────────────────────────── MathML side ──


def _mark_stray_amp(mml: str) -> str:
    """Repair 1, first half: a bare ``&`` becomes a sentinel so the XML parser accepts the text.

    An entity (``\\&``) arrives as ``&#x00026;`` and must be left alone, which is why this replaces
    only the unescaped ones.
    """
    return re.sub(r"&(?!#\d+;|#x[0-9A-Fa-f]+;|[A-Za-z][A-Za-z0-9]*;)", SENTINEL, mml)


def _restore_sentinels(root: etree._Element) -> None:
    """Repair 1, second half: the marker is a literal ``&`` again, which Word reads as alignment."""
    for element in root.iter():
        if element.text and SENTINEL in element.text:
            element.text = element.text.replace(SENTINEL, "&")


def _fix_accents(root: etree._Element) -> None:
    """Repair 2: ``mover``/``munder`` over an accent character, made recognisable and stretchy."""
    for tag in (_mml("mover"), _mml("munder")):
        for node in root.iter(tag):
            children = list(node)
            if len(children) < 2:
                continue
            accent = children[-1]
            if accent.tag != _mml("mo") or not accent.text:
                continue
            char = ACCENT_MAP.get(accent.text, accent.text)
            if char not in ACCENT_CHARS:
                continue
            accent.text = char
            accent.set("accent", "true")
            accent.set("stretchy", "true")


# ──────────────────────────────────────────────────────────── OMML side ──


def _repair_groupchr(text: str) -> str:
    """Repair 3: a closing tag typo in ``mathml2omml``'s ``MOver.to_str``."""
    return text.replace("</m:groupChr><m:e>", "</m:groupChrPr><m:e>")


def _mml_to_omml(mml: etree._Element) -> etree._Element:
    text = _repair_groupchr(mathml2omml.convert(etree.tostring(mml, encoding="unicode")))
    if "xmlns:m=" not in text[:200]:  # the package emits prefixed markup with no declaration
        text = text.replace("<m:oMath", f'<m:oMath xmlns:m="{MATH_NS}"', 1)
    return etree.fromstring(text)


def _fix_radicals(root: etree._Element) -> None:
    """Repair 4: a square root needs an empty ``m:deg`` and ``degHide``, or the radicand drops."""
    for rad in root.iter(_m("rad")):
        if rad.find(_m("deg")) is not None:
            continue
        properties = etree.Element(_m("radPr"))
        etree.SubElement(properties, _m("degHide")).set(_m("val"), "on")
        rad.insert(0, properties)
        rad.insert(1, etree.Element(_m("deg")))


def _groupchr_to_acc(root: etree._Element) -> None:
    """Repair 5: a ``groupChr`` with an accent draws as a group char; ``m:acc`` is an accent."""
    for group in list(root.iter(_m("groupChr"))):
        properties = group.find(_m("groupChrPr"))
        char = properties.find(_m("chr")) if properties is not None else None
        if char is None or char.get(_m("val")) not in ACCENT_CHARS:
            continue
        accent = etree.Element(_m("acc"))
        accent_properties = etree.SubElement(accent, _m("accPr"))
        etree.SubElement(accent_properties, _m("chr")).set(_m("val"), char.get(_m("val")))
        for child in group:
            if child is not properties:
                accent.append(child)
        group.getparent().replace(group, accent)


def _ssub_to_limlow(root: etree._Element) -> None:
    """Repair 6: a limit under an operator name is ``m:limLow``; ``m:sSub`` draws an error mark."""
    for subscript in list(root.iter(_m("sSub"))):
        base = subscript.find(_m("e"))
        under = subscript.find(_m("sub"))
        if base is None or under is None:
            continue
        if "".join(base.itertext()).strip() not in LIMIT_OPS:
            continue
        low = etree.Element(_m("limLow"))
        low.append(base)
        limit = etree.SubElement(low, _m("lim"))
        limit.extend(list(under))
        subscript.getparent().replace(subscript, low)


def _unwrap_boxes(root: etree._Element) -> None:
    """Repair 7a: ``mathml2omml`` wraps every ``<mrow>`` in ``<m:box>``; pandoc emits none."""
    for box in list(root.iter(_m("box"))):
        inner = box.find(_m("e"))
        if inner is None or len(box) != 1:
            continue
        parent = box.getparent()
        at = list(parent).index(box)
        for offset, child in enumerate(list(inner)):
            parent.insert(at + offset, child)
        parent.remove(box)


def _nary_flags(root: etree._Element) -> None:
    """Repair 7b: without ``subHide``/``supHide`` a sum's limits stay at the side of the sign."""
    for nary in root.iter(_m("nary")):
        properties = nary.find(_m("naryPr"))
        if properties is None:
            continue
        for tag, part in (("subHide", _m("sub")), ("supHide", _m("sup"))):
            if nary.find(part) is not None and properties.find(_m(tag)) is None:
                etree.SubElement(properties, _m(tag)).set(_m("val"), "off")


# ──────────────────────────────────────────────────────── aligned rows ──


def _row_omml(children: list[etree._Element]) -> etree._Element:
    """One aligned row as an ``<m:e>``, with ``mathml2omml`` doing the insides."""
    wrapper = etree.Element(_mml("math"), nsmap={None: MML_NS})
    row = etree.SubElement(wrapper, _mml("mrow"))
    row.extend(children)
    maths = _mml_to_omml(wrapper)
    box = maths.find(_m("box"))
    holder = box.find(_m("e")) if box is not None else maths
    cell = etree.Element(_m("e"))
    cell.extend(list(holder) if holder is not maths else list(maths))
    return cell


def _aligned_to_eqarr(latex: str) -> etree._Element | None:
    """``aligned`` and friends -> ``m:eqArr``: one ``<m:e>`` per line, ``&`` kept as the marker."""
    if not ALIGNED.match(latex):
        return None
    mml = etree.fromstring(_mark_stray_amp(latex2mathml.convert(latex)).encode())
    _restore_sentinels(mml)
    _fix_accents(mml)
    breaks = [node for node in mml.iter(_mml("mspace")) if node.get("linebreak") == "newline"]
    if not breaks:
        return None
    rows: list[list[etree._Element]] = [[]]
    for child in breaks[0].getparent():
        if child.tag == _mml("mspace") and child.get("linebreak") == "newline":
            rows.append([])
        else:
            rows[-1].append(child)
    equation_array = etree.Element(_m("eqArr"))
    for row_children in rows:
        if row_children:
            equation_array.append(_row_omml(row_children))
    return equation_array if len(equation_array) else None


# ──────────────────────────────────────────────────────────────── public ──


def _post_process(root: etree._Element) -> None:
    _fix_radicals(root)
    _groupchr_to_acc(root)
    _ssub_to_limlow(root)
    _unwrap_boxes(root)
    _nary_flags(root)


def _validate(root: etree._Element) -> None:
    missing = [
        f"{tag} lacks {', '.join(gone)}"
        for tag, children in REQUIRED_CHILDREN.items()
        for element in root.iter(_m(tag))
        if (gone := [child for child in children if element.find(_m(child)) is None])
    ]
    if missing:
        raise ValueError("OMML invalid: " + "; ".join(missing))


@functools.lru_cache(maxsize=256)
def latex_to_omml(latex: str) -> str:
    """LaTeX -> a schema-valid ``<m:oMath>`` string, converted in-process. Same contract as the
    pandoc backend in ``omml.py``, so the two are interchangeable at the call site."""
    equation = _aligned_to_eqarr(latex)
    if equation is not None:
        root = etree.Element(_m("oMath"), nsmap={"m": MATH_NS})
        root.append(equation)
        _post_process(root)
        _validate(root)
        return etree.tostring(root, encoding="unicode")

    mml = etree.fromstring(_mark_stray_amp(latex2mathml.convert(latex)).encode())
    _restore_sentinels(mml)
    _fix_accents(mml)
    try:
        root = _mml_to_omml(mml)
    except xml.sax.SAXParseException as error:  # reported by the package's SAX handler
        raise ValueError(f"mathml2omml rejected the markup: {error}") from error
    _post_process(root)
    _validate(root)
    clean = etree.Element(_m("oMath"), nsmap={"m": MATH_NS})
    clean.extend(list(root))
    return etree.tostring(clean, encoding="unicode")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("latex", help="the formula, e.g. '\\frac{a}{b}'")
    parser.add_argument("--wrapped", action="store_true", help="also wrap for PowerPoint (a14:m)")
    arguments = parser.parse_args(argv)
    omml = latex_to_omml(arguments.latex)
    print(omml)
    if arguments.wrapped:
        print(
            f'<a14:m xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main"'
            f' xmlns:m="{MATH_NS}"><m:oMathPara>{omml}</m:oMathPara></a14:m>'
        )
    return 0


def command(ctx, argv: list[str]) -> int:
    """archont561 entry point for ``mathml-omml``."""
    return main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
