# LaTeX → typst: what actually converts

Measured through `math_slide.latex_to_typst()` (`.agents/skills/archont561-render/commands/`) + `typst compile` on **152 probe formulas**
(64 realistic, then 88 single commands): **118 compiled**. Every failure was the same failure — so
the table is really about recognising it.

## The silent failure

pandoc does not error on a macro it does not know. It emits the LaTeX back as **plain text**, which
compiles fine and renders as a monospace string where the maths should be:

```
$\textcolor{blue}{x} + y$      $\fbox{x}$      $\eqref{eq:one}$
$\begin{dcases} a & x>0 \\ b & e \end{dcases}$
```

Nothing draws attention to it. Guard with `if not out.lstrip().startswith("$"): raise` whenever the
LaTeX was not written for this pipeline.

## Falls back to raw text (19 commands)

`\textcolor`, `\fbox`, `\cancelto`, `\hphantom`, `\vphantom`, `\vspace`, `\eqref`, `\intertext`,
`\emph`, `\mbox`, `\hbox`, `\mathchoice`, `\leftroot`/`\uproot`, `\dbinom`, `\cfrac`, mathtools'
`dcases` and `rcases`, a bare `\hline`, and `\def`/`\newcommand` inside the maths.

## Silently degraded (compiles, subtly wrong)

| Command | What happens |
---|---|---
| `\color`, `\tag` | dropped without a trace |
| `\label` | becomes a typst label *outside* the maths — not a cross-reference |
| `array`, `matrix`, `smallmatrix` | the column gap collapses: pandoc writes a bare `&`, which typst reads as an alignment point, not a separator |
| `\hline` inside an array | dropped |
| `\setminus` | comes out as a doubled backslash, i.e. a line break |
| `\mathrm{TSR}` | `upright(T S R)` → "T S R"; write `\text{TSR}` |

## Survives

Fractions (including nested), every root, `\sum` `\int` `\prod` `\oint` `\bigcup` with limits, `\lim`
`\limsup` `\liminf`, `\binom`, `cases`, `aligned` `align` `align*` `gather*`, all five matrix
variants (`matrix`, `pmatrix`, `bmatrix`, `Bmatrix`, `vmatrix`, `Vmatrix`), `\overset` `\underset`
`\stackrel`, `\operatorname*`, `\substack`, the accent and font alphabets (`\hat` `\bar` `\vec`
`\tilde` `\dot` `\ddot` `\acute` `\grave` `\breve` `\check` `\mathring`, `\mathfrak` `\mathcal`
`\mathbb` `\mathbf` `\mathsf` `\mathtt`), `\overbrace` `\underbrace`, `\boxed`, `\phantom`, `\hspace`,
`\cancel`, `\Big`/`\bigg`/`\Bigg` sizes, `\middle`, `\colon`, `\%`.

## The one-character fix

`vmatrix` and `Vmatrix` compile only because `_one_char_delim` rewrites pandoc's `delim: "||"` to
`‖` (U+2016). typst's `mat(delim:)` accepts exactly one character; the error otherwise reads
`expected exactly one character`, which is easy to misread as a problem with the matrix.

## Handy check

```bash
pixi run -e renderers python -c "
import sys; sys.path.insert(0,'scripts')
from math_slide import latex_to_typst
print(latex_to_typst(r'\frac{a}{b}'))"     # must start with '\$'
```
