import { defineConfig, presetUno, transformerDirectives, transformerVariantGroup } from 'unocss'

/**
 * Design tokens for the documentation site, and the only place they are written down.
 *
 * MyST's single styling hook is `site.options.style`: one stylesheet, merged into `myst-theme.css`
 * at build time. The paths below are relative to this directory, so the site can be picked up and
 * moved without a second thing to edit. So the tokens are emitted as custom properties on `:root` and overridden under
 * `.dark`, which is the class the theme's own toggle puts on `html` — a utility like `text-ink`
 * therefore follows the reader's theme without a second set of rules.
 *
 * The theme is left alone: these tokens style the markup *we* write (raw HTML blocks in MyST, the
 * chart wrappers, the command palette), while the article itself keeps the book theme's typography.
 * Once the built stylesheet shows which `--myst-*` variables the theme exposes, a bridge block here
 * can set those from these tokens; inventing their names now would be guessing.
 */
export default defineConfig({
  presets: [presetUno()],
  // `--uno:` in hand-written CSS, and `hover:(bg-surface text-ink)` groups in markup.
  transformers: [transformerDirectives(), transformerVariantGroup()],
  // The task runs `unocss` with no arguments, so the globs live here, in the CLI's own entry:
  // `content.pipeline.include` is what the bundler plugins read, and nothing in this repository
  // runs one. One place to add a content directory, and the stylesheet cannot fall out of step.
  cli: {
    entry: [
      {
        patterns: [
          '**/*.md', // MyST pages: classes in raw HTML blocks and in `:class:` options
          '**/*.ipynb', // a page that is a notebook
          '**/*.html', // widgets the pages iframe or include
          // Two trees inside this directory are not content, and a bare `**` walks both:
          // node_modules (the workspace's own dependencies) and _build (MyST's output, which is
          // the pages again, rewritten). Scanning either costs utilities that are already here.
          '!**/node_modules/**',
          '!_build/**',
          // This file itself, so the tokens are emitted even while there is no content to
          // scan: the CLI writes nothing at all when every pattern matches zero files, and a
          // myst.yml pointing at a stylesheet that was never generated is a broken build.
          'uno.config.ts',
        ],
        outFile: 'assets/site.css', // what myst.yml names as site.options.style
      },
    ],
  },
  theme: {
    colors: {
      paper: 'var(--site-paper)',
      surface: 'var(--site-surface)',
      ink: 'var(--site-ink)',
      muted: 'var(--site-muted)',
      line: 'var(--site-line)',
      accent: 'var(--site-accent)',
      pass: 'var(--site-pass)',
      fail: 'var(--site-fail)',
    },
    fontFamily: {
      serif: 'var(--site-font-serif)', // the thesis register: prose is set in a serif
      sans: 'var(--site-font-sans)', // interface: the palette, the toolbar, the tables
      mono: 'var(--site-font-mono)', // commands, paths, digests
    },
    fontSize: {
      'step--1': 'var(--site-step--1)',
      'step-0': 'var(--site-step-0)',
      'step-1': 'var(--site-step-1)',
      'step-2': 'var(--site-step-2)',
      'step-3': 'var(--site-step-3)',
    },
    spacing: {
      token: 'var(--site-space-1)',
      'token-2': 'var(--site-space-2)',
      'token-3': 'var(--site-space-3)',
      'token-4': 'var(--site-space-4)',
    },
    borderRadius: {
      token: 'var(--site-radius)',
      'token-lg': 'var(--site-radius-lg)',
    },
  },
  // Markup that exists only at run time — the command palette, injected after the build — is
  // scanned by nobody, so its classes have to be listed here as they are written.
  safelist: [],
  preflights: [
    {
      getCSS: () => `
:root {
  --site-paper: #fbfaf8;
  --site-surface: #ffffff;
  --site-ink: #1a1c1f;
  --site-muted: #5b6068;
  --site-line: #e3e0d9;
  --site-accent: #2f6f4f;
  --site-pass: #2f6f4f;
  --site-fail: #a63d40;

  --site-font-serif: Charter, 'Source Serif 4', 'Iowan Old Style', Georgia, serif;
  --site-font-sans: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --site-font-mono: 'JetBrains Mono', 'SF Mono', ui-monospace, monospace;

  --site-step--1: 0.875rem;
  --site-step-0: 1rem;
  --site-step-1: 1.25rem;
  --site-step-2: 1.5625rem;
  --site-step-3: 1.9531rem;

  --site-space-1: 0.25rem;
  --site-space-2: 0.5rem;
  --site-space-3: 0.75rem;
  --site-space-4: 1rem;

  --site-radius: 0.375rem;
  --site-radius-lg: 0.75rem;
}

.dark {
  --site-paper: #14161a;
  --site-surface: #1b1e23;
  --site-ink: #e8e6e1;
  --site-muted: #a2a8b0;
  --site-line: #2a2e35;
  --site-accent: #6cc28f;
  --site-pass: #6cc28f;
  --site-fail: #e08b8e;
}

/* Result tables carry numbers that have to line up in columns to be readable. */
.site-numeric { font-variant-numeric: tabular-nums; font-family: var(--site-font-mono); }
`,
    },
  ],
})
