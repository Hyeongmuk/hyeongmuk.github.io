# Instructions for Claude — Mook Academic Website

**Read first:** `docs/claude-context.md` — edit history, past mistakes and CI failures, page/data map, technical debt, browser QA checklist (condensed from the handoff documents `01_WEBSITE_HANDOFF_KO.md` and `03_QA_AND_WORKFLOW.md`). The living source of truth is the actual repository HEAD; that context was prepared against `main` commit `8784e2a36e68e14ba2253eeae5780a23b4abe2a0` (2026-10-29 18:34 KST).

## Non-negotiable rules

- **Only implement explicitly requested changes.** Never opportunistically change prose, scientific claims, typography, figure labels, SVG coordinates, captions, navigation, or unrelated pages. Propose incidental improvements separately.
- Preserve the established H website design: fixed left sidebar on desktop, compact mobile nav, calm editorial cards for papers and notes, readable typography.
- The author-provided `public/research/quaternion-kahler-geometry.svg` and its original caption are protected assets. Do not modify or redraw either without an explicit user request. Reference baseline: commit `18f71e41d8de66483cba4b8add7b4ff445b0eba0`. In particular, do not add `figure-explainer`, move text coordinates or overlap mathematical labels.
- Do not show developer-only maintenance text to visitors, e.g. `Publication metadata is maintained in BibTeX` or instructions to edit `src/data/publications.bib`. Do not reintroduce `Browse study notes ↗` on Students.
- Internal navigation `→`, actual new-tab links `↗`. Use user-facing language, not source-code jargon.
- Do not overclaim physics: the quaternionic geometry framework is not itself a demonstrated correlated phase; distinguish established findings from future many-body interests.
- No destructive Git operations, unapproved changes to `main`, or large source overwrites. Preserve all local user changes and existing PDFs/assets.
- First inspect `git status --short` and current HEAD. Work on a topic branch when appropriate. Finish with tests and `git diff` review; verify visuals in a browser if applicable.

## Relevant code

- Pages: `src/pages/{index,research,publications,about}.astro`, `src/pages/notes/`, `src/pages/students/`.
- Publications: `src/data/publications.bib`, `src/data/publication-meta.json`, `src/lib/publications.mjs`, `src/components/PaperCard.astro`.
- Notes: `src/content/notes/*.md`, `src/content.config.ts`, `public/downloads/`.
- Shared filters: `src/components/SearchFilter.astro`, `public/scripts/search-filter.js`.
- Site design: `src/layouts/SiteLayout.astro`, `src/styles/site.css`; Students has `src/styles/students.css`.
- Build/deploy: `package.json`, `.github/workflows/`, `tests/`, `scripts/verify-*.mjs`.

## Verification

```bash
npm test
node scripts/verify-site-source.mjs
npm run build
node scripts/verify-built-site.mjs
node scripts/verify-visitor-site.mjs
git diff --check
```

Latest verified Actions run: `41192279041` (2026-10-31, PR #31) — 30/30 tests, build and GitHub Pages deployment passed. **Do not conflate CI success with a completed manual visual audit.**

When reporting, use Korean. State exact files changed, expected impact, tests actually run, browser QA actually done, remaining risks, and how to review/undo. Do not modify anything if the user has only asked for a status report.
