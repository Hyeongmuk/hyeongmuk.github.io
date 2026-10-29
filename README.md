# Mook · Hyeongmuk Lim — academic website

Astro-based personal academic website at **https://mookphysics.org**.

The current design uses a left sidebar (desktop), a compact mobile menu, editorial publication and note rows, and a shared search/filter component for publications and study notes.

## Build locally

Requires Node.js 22 or a compatible Astro 5 version.

```bash
npm ci
npm test
npm run build
npm run dev
```

To deploy to GitHub Pages, merge tested changes into `main`. GitHub Actions builds and publishes the static output automatically. Custom domain and site origin live in `astro.config.mjs` and repository Pages settings.

## Content maintenance

- Publications: edit `src/data/publications.bib` and, for manually curated featured selection / summaries / categories / tags, `src/data/publication-meta.json`.
- Study notes: add one frontmatter Markdown file in `src/content/notes/`, and add its source PDF under `public/downloads/`. Only `status: published` notes appear on the site. `complete: true` indicates a completed study manuscript, not independent peer review.
- Shared search UI: `src/components/SearchFilter.astro`. Both archives generate keyword lists from their source metadata; do not edit the keyword buttons manually.
- Profile photo: `public/profile-hyeongmuk-lim.webp`, optimized from the author's provided portrait.
- Academic CV: `public/downloads/Hyeongmuk_Lim_CV.pdf`. Keep it in sync with the author's current canonical CV file.
- Website research prose: `src/pages/index.astro`, `src/pages/research.astro`, `src/pages/about.astro`.
- Layout: `src/layouts/SiteLayout.astro` and the single production stylesheet `src/styles/site.css`. The bottom **VISITOR POLISH** section documents final typography and responsive overrides; consolidate related rules when refactoring, rather than adding more layers.
- Research figure: `public/research/quaternion-kahler-geometry.svg` (original scientific content preserved, title typography repaired).
- Search indexing: `src/pages/sitemap.xml.ts`, `public/robots.txt`, and metadata/JSON-LD in the layout.

## Verification

Use `npm test`, `npm run build`, and `node scripts/verify-visitor-site.mjs` for every pull request. CI runs these automatically. `.gitignore` excludes dependencies and generated files from future commits, but already-tracked copies require a **separate explicit** `git rm --cached` cleanup. Confirm in a browser: left navigation, 2 featured publications, all published notes, PDF download, photo mobile/desktop layout, About CV links, search and keyword filtering, and sitemap.

See `RELEASE_NOTES_2026-10-26_ko.md` and `CONTENT_REVIEW_EN.md` for current revision details and editorial wording.
