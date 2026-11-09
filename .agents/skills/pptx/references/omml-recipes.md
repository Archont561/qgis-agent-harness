# OMML recipes for PPTX

## Reader compatibility (measured, not assumed)

| Container | Word / PowerPoint | LibreOffice (Writer / Impress) | docx→HTML previewers (mammoth, docx-preview) |
|---|---|---|---|
| DOCX, bare `m:oMath` | ✔ editable | ✔ | ✘ silently blank |
| DOCX, OMML + picture in `mc:AlternateContent` | ✔ | ✘ Writer drops the whole construct | ✔ (picture) |
| DOCX, picture only | ✔ | ✔ | ✔ |
| PPTX, `a14:m` only | ✔ editable | ✔ (needs `libreoffice-math`) | ✘ blank slide |
| PPTX, `mc:AlternateContent` (`a14:m` + picture) | ✔ editable | picture branch | picture branch |
| PPTX, picture only | ✔ | ✔ | ✔ |

The rule that falls out of it: **a deck that will be previewed anywhere must contain a
`ppt/media` part.**

## Minimal insertion (python-pptx or easypptx)

```python
import subprocess, tempfile, zipfile
from pathlib import Path
from lxml import etree
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn

MATH = "http://schemas.openxmlformats.org/officeDocument/2006/math"
A14 = "http://schemas.microsoft.com/office/drawing/2010/main"
NSDECL = f'xmlns:a14="{A14}" xmlns:m="{MATH}"'


def omml_from_latex(latex: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        tex, docx = Path(tmp) / "e.tex", Path(tmp) / "e.docx"
        tex.write_text(f"\\[{latex}\\]\n")
        subprocess.run(["pandoc", "-f", "latex", "-t", "docx", str(tex), "-o", str(docx)],
                       check=True, capture_output=True)
        body = etree.fromstring(zipfile.ZipFile(docx).read("word/document.xml"))
    src = body.findall(f".//{{{MATH}}}oMath")[0]
    clean = etree.Element(f"{{{MATH}}}oMath", nsmap={"m": MATH})   # drop pandoc's w:/r:/o: decls
    clean.extend(list(src))
    return etree.tostring(clean, encoding="unicode")


def add_equation(paragraph, latex: str, display: bool = True) -> None:
    inner = f"<m:oMathPara>{omml_from_latex(latex)}</m:oMathPara>" if display else omml_from_latex(latex)
    el = parse_xml(f"<a14:m {NSDECL}>{inner}</a14:m>")
    end = paragraph._p.find(qn("a:endParaRPr"))     # schema order: runs, maths, endParaRPr
    (end.addprevious if end is not None else paragraph._p.append)(el)
```

The repo's `omml` command (`.agents/skills/archont561-render/commands/omml.py`) is this, plus validation, caching and both hosts — prefer it.

## Hybrid that keeps both branches (PPTX only)

```xml
<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
  <mc:Choice Requires="a14">
    <a14:m xmlns:a14="…" xmlns:m="…"><m:oMathPara>…</m:oMathPara></a14:m>
  </mc:Choice>
  <mc:Fallback><p:pic>… picture of the same formula …</p:pic></mc:Fallback>
</mc:AlternateContent>
```

`mc:AlternateContent` survives in a PPTX and does not survive in a DOCX: Word shows the first branch
and LibreOffice's Writer drops the construct instead of reading the fallback. In Word, use one branch
or the other — `omml.py`'s `equation_picture()` exists for exactly that.

## Verification one-liners

```bash
# what is actually inside
python3 -c "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); n=z.namelist(); \
print('media:', [x for x in n if x.startswith('ppt/media')] or 'NONE'); \
print('slides:', len([x for x in n if x.startswith('ppt/slides/slide')]))" deck.pptx

# does it draw
soffice --headless --norestore -env:UserInstallation=file:///tmp/lo-p --convert-to pdf deck.pptx
pixi run -e renderers python -c "import pypdfium2 as p; d=p.PdfDocument('deck.pdf'); \
[d[i].render(scale=1.5).to_pil().save(f'p{i}.png') for i in range(len(d))]"
```

Count the pages as well as looking at them: a deck whose formulas overflow pushes content onto extra
slides and the numbers stop matching the plan.

## Budgets that read well on a 16:9 slide

Slide 13.333 × 7.5 in. A display formula at `height=Inches(0.55)` sits comfortably in a text column;
`0.45` if it must share a row. Keep 600 ppi minimum — at 0.55 in tall that is ~330 px, enough for a
projector and for print in an appendix.
