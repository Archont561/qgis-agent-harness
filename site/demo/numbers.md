---
title: Numbers
---

# Numbers

A results table is the thing this site will be judged on, so the placeholder is a table rather than a
paragraph. The numbers are invented and mean nothing.

| Arm | Runs | Tool success rate | Task success rate |
|---|---|---:|---:|
| MCP tools | 960 | 0.412 | 0.318 |
| PyQGIS code | 960 | 0.397 | 0.304 |

A markdown table cannot carry a class, so the cells above are plain. The real tables will be
`{list-table}` directives, which take `:class:`, and this is what the class gives — tabular figures
in the mono face, so the columns line up: <span class="site-numeric">0.412</span> against
<span class="site-numeric">0.397</span>.

```{note}
No number produced by `experiment/` counts until the measures are frozen — milestone `m-0`, gate G1
not passed. The figures above are placeholders, not results.
```

## Reading the table

The comparison is pre-registered and scored by spatial predicates, so a cell is a rate over 960 runs
rather than a judgement. When the real table lands, the same columns hold the same meaning, and the
confidence intervals go beside them rather than in the footnotes.
