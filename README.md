# Mook — Academic Website (Astro prototype)

This is an Astro-based academic website for **Hyeongmuk Lim**. It is a prototype derived from the existing `hyeongmuk.github.io` repository and its public learning notebook.

**Default publication URL:** `https://hyeongmuk.github.io/`. The desired address `mook.github.io` is already claimed by a different GitHub user. The site *branding* can still be "mook". If a custom domain is purchased, update `site` in `astro.config.mjs` and configure GitHub Pages/DNS.

## Preview without installation

Open `preview/index.html` in a web browser after unzipping. This is a **static visual mockup**, not the final Astro production build. Other offline preview pages are also linked in the preview navigation.

## Local Astro development

Install Node.js 20.19+ or 22+, then run in the project folder:

```bash
npm install
npm run dev
```

Visit the local URL printed in the terminal, usually `http://localhost:4321`.

```bash
npm test
npm run build
```

Because this file package was generated without access to the npm registry, an end-to-end Astro build could not be run here. The included BibTeX parser tests **were** run successfully with Node. Run `npm install`, `npm test`, and `npm run build` locally or in GitHub Actions before production publishing. Commit `package-lock.json` after installing for reproducibility; you may then switch the deployment action to `npm ci`.

## Deploy using GitHub Desktop

1. Make a backup branch of your current website repository (recommended: `backup-html-v1`).
2. Open GitHub Desktop, clone `hyeongmuk/hyeongmuk.github.io` (or use your actual owner name), and create a branch such as `astro-preview`.
3. Copy the **contents** of this folder (not the outer folder, and not the zip itself) into that clone's root. The new Astro project replaces the old root HTML design. Preserve anything important before deleting old files.
4. In GitHub Desktop inspect the changes; commit with a message such as `Migrate homepage to Astro`; push branch.
5. Merge the branch into `main` when ready (GitHub pull request is ideal).
6. At GitHub repository **Settings → Pages**, change **Source** from `Deploy from a branch` to **GitHub Actions**. This is mandatory for Astro source projects; do not use `main /(root)` deployment.
7. On push to `main`, `.github/workflows/deploy.yml` installs dependencies, runs BibTeX parser tests, builds Astro, and publishes `dist/` to GitHub Pages.
8. Check the **Actions** tab for build errors. Do not assume publication succeeded until the action is green and the live URL works.

**Never upload only Astro source to branch-root Pages deployment**: it needs a build step first.

## Papers — BibTeX driven (not Google Scholar scraping)

Edit `src/data/publications.bib` to add papers. The `src/lib/bibtex.mjs` parser reads these entries automatically at site build; they appear on the home and Publications pages in descending year order. Paper metadata such as `featured` and a short `summary` belongs in `src/data/publication-meta.json`, indexed by BibTeX key.

Example:

```bibtex
@article{mynewpaper2027,
  author = {Hyeongmuk Lim and Collaborator Name},
  title = {Paper title},
  year = {2027},
  eprint = {2701.00000},
  journal = {Physical Review B},
  doi = {10.1103/....},
  keywords = {Quantum geometry, Topology}
}
```

Update the `.bib` file and push through GitHub Desktop → GitHub Actions rebuilds the website **automatically**. This is **not** scheduled syncing from Google Scholar: Google Scholar blocked automated access, and this first release intentionally does not scrape it. Metadata from arXiv/DOI can be used when importing or updating BibTeX entries manually; make sure not to import papers by different people with the same name.

The four seeded physics works have been cross-checked against the lab's public publication list and arXiv. They may not be the user's complete Google Scholar profile, because that page returned HTTP 429. See `PUBLICATION_SOURCES.md`.

The built-in parser handles ordinary BibTeX fields, nested braces and quotes, not every advanced BibLaTeX construct (macros, crossref, concatenated field values). Use flattened BibTeX if importing complex exports.

## Notes — web reader + downloads

- Add a **Markdown** file to `src/content/notes/`: its prose and LaTeX math will render to an online reader automatically.
- Add public PDFs/IPYNBs/other originals under `public/downloads/`.
- Put download links in note frontmatter. Put `pdf: '/downloads/file.pdf'` in frontmatter to embed an inline PDF viewer and show a PDF download button.
- Set `status: draft` for anything you do **not** want to publish. Keep sensitive/private work **out of the public GitHub repository entirely**, including history, before committing.

Sample note frontmatter:

```yaml
---
title: 'An introduction to quantum field theory'
description: 'An example explanation'
date: 2026-10-25
topic: 'Quantum field theory'
status: published
pdf: '/downloads/qft-note.pdf'
downloads:
  - label: 'PDF'
    href: '/downloads/qft-note.pdf'
---
```

If you add a PDF only, create a small Markdown file with the metadata above and a short introduction. The PDF itself need not be converted. If you have a TeX document, convert it to PDF locally or in your TeX workflow first. The included cluster-model `.ipynb` notebook is converted to a browser-readable Markdown page by `scripts/import_notebook.py`. Its recorded outputs were empty; the page therefore does not contain generated plot images. The included PDF is a **reading excerpt** of its explanatory markdown cells, not the entire executable notebook.

To convert additional notebooks automatically, adapt `scripts/import_notebook.py` (currently specialized for the public cluster SPT example). Do not publish notebooks with tokens, emails, or private data in their outputs or metadata.

## Directory structure

```text
astro.config.mjs
.github/workflows/deploy.yml
src/
  data/publications.bib             # paper source of truth
  data/publication-meta.json        # optional display summaries
  lib/bibtex.mjs                     # BibTeX parser
  content/notes/                    # browser-readable notes
  pages/                             # Astro pages
  components/                        # site UI
  styles/global.css                 # visual design
public/downloads/                   # public PDFs, notebooks, Markdown
preview/                            # open-in-browser static mockup
```

## Things to review before publishing

- The QFT Notion URL still points outside this website; check its public sharing permissions.
- Review publication titles, authors, years, journals and any missing Scholar entries.
- Decide whether to publish personal contact email and research notes (both already existed in the provided public repository).
- Confirm the chosen GitHub owner and URL; edit `astro.config.mjs` if different.
- For repositories named something other than `<owner>.github.io`, configure Astro `base: '/repository-name'` and prefix internal site links appropriately. This prototype specifically targets **the existing root user-site repository**.
