---
title: Design tokens
---

# Design tokens

The block below is raw HTML, and its classes are the ones `uno.config.ts` maps onto the tokens. They
are only in the stylesheet because `pixi run site-css` scanned this page and found them — a class
that no page uses is never emitted.

<div class="bg-surface text-ink rounded-token p-token-4 border border-line">
  <p class="font-sans text-step-0">Surface on ink, with a token radius and one step of padding.</p>
  <p class="font-mono text-step--1 text-muted">pixi run site-css</p>
</div>

Switch the theme with the control in the header: the tokens are custom properties on `:root`,
overridden under `.dark`, so the same classes produce both.

## What is not here yet

The stylesheet is merged into `myst-theme.css`, which means it is loaded *before* the theme's own
rules in some places and after them in others. Which of the theme's variables a page may safely
override is still unmeasured — the built sheet is the place to look, and guessing the names costs
more than waiting.
