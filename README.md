# Mook — academic website (Astro)

An Astro-based personal website for **Hyeongmuk Lim**, targeting **https://mookphysics.org**. This project implements the approved hybrid design: **B's fixed desktop sidebar / mobile menu and A's publications and study-note cards**.

## Publishing safely with GitHub Desktop

1. Open the repository `Hyeongmuk/hyeongmuk.github.io` in GitHub Desktop. Select `main` and **Pull origin**.
2. Create a fresh branch, such as `hybrid-design-release`.
3. **Back up any newer site-specific changes** that are not in this package. Unzip this package, then copy the **contents** (not the enclosing folder) to the root of your GitHub Desktop checkout. Replace same-named files. **Never replace/delete `.git/`.**
4. Remove old files superseded by this release if still present: `src/styles/global.css`, `src/styles/notes-compact.css`, `src/content/notes/cluster-model.md`, old `public/downloads/cluster_*`, and any obsolete `preview/` content. These legacy files should not be used in the published website. Only delete them if you are sure they're no longer needed.
5. In GitHub Desktop **Changes** inspect the actual modifications, especially `src/layouts/SiteLayout.astro`, `src/components/`, `src/pages/`, `src/styles/`, `public/scripts/`, `public/downloads/` and `src/content/notes/`.
6. Commit to the new branch, **Push/Publish branch**, create a pull request to `main`, and wait for **Verify Astro pull request** to report a successful build. Merge only after verification.
7. A push to `main` triggers GitHub Pages deployment. Check Actions for a green **Deploy academic homepage** run; then hard refresh https://mookphysics.org.

This source archive is **not** itself a compiled `dist/` directory. GitHub Actions compiles it. Keep `Settings → Pages → Source: GitHub Actions`, with the custom domain configured as `mookphysics.org`.

## Content management

### Publications

- `src/data/publications.bib` is the source of truth for citation details. All publication cards derive from BibTeX at build time.
- `src/data/publication-meta.json` stores supplementary display metadata: `featured`, `summary`, `area`, `tags`. Key these fields by the BibTeX citation key. They can be changed without modifying the citation details.
- The **area chips** on Publications are based on the area values used in `src/data/categories.mjs`, and **keyword chips** are automatically derived from `tags` (or BibTeX `keywords` when extra metadata tags are absent).
- After adding a paper, run `npm test && npm run build` (or rely on PR Actions checks) before publishing. Google Scholar automatic scraping/synchronization is not implemented.

### Study notes

- Add a Markdown file under `src/content/notes/` containing `title`, `description`, `date`, `topic`, `category`, `tags`, `status`, and optionally `complete`, `pages`, `pdf` and `downloads`.
- PDF originals go under `public/downloads/`. The site creates notes and detail pages from the Markdown metadata.
- Valid categories: `qft`, `mathematics`, `condensed`. Do not place private drafts or unpublished private files anywhere in the public GitHub repo.
- `status: published` displays a note. `status: draft` does **not** create a page or listing. A draft's linked PDF should **not** be uploaded into `public/downloads/` because public assets remain accessible directly.
- Notes have direct **Read PDF** links (new tab) and a **Download** link.

Example:

```yaml
---
title: 'Lecture notes on TQFT'
description: 'Notes on state-sum constructions.'
date: 2026-10-25
topic: 'Topological Field Theory'
category: 'qft'
tags: ['TQFT', 'Topology', 'Category Theory']
complete: false
status: published
pdf: '/downloads/tqft.pdf'
---
```

## Design system / reusable UI

- `src/components/Header.astro`: responsive fixed sidebar and mobile navigation
- `src/components/SearchFilter.astro`: **one shared component** on Publications and Notes. Same typography, spacings, search input, area chips, keyword chips, accessible pressed states, and empty-state behavior
- `public/scripts/search-filter.js`: one shared behavior: simultaneous text, area, and keyword filters; one selected area and one selected keyword at a time; Clear filters; counters and hidden empty groups
- `src/components/PaperCard.astro` / `NoteCard.astro`: A-style editorial content cards
- `src/styles/base.css`, `b.css`, `hybrid.css`, `production.css`: design foundations and production overrides. All imported centrally in `src/layouts/SiteLayout.astro`.

## Local developer commands

Requires Node 22+ and a network connection to the npm registry on first install.

```sh
npm install
npm test
npm run dev
npm run build
```

`npm test` includes publication parser and site structure tests. GitHub Actions additionally runs a production Astro build. GitHub Actions is responsible for producing `dist/` and deploying it.

## Verification and limitations

- This package passed local BibTeX tests, source/asset metadata tests and JavaScript syntax checks in the authoring environment.
- Astro's full npm installation/build and screenshot browser checks could not run in that environment due to outbound-network/browser restrictions. **The PR build must succeed before merging.**
- Four publication records come from the preexisting verified BibTeX file, not a full synced Google Scholar export. No new bibliography entries were invented.
- The three PDF files correspond to the original study notes; verify academic accuracy, attribution and references before public dissemination.
