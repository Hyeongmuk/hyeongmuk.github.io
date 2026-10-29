import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '..');
const read = path => readFileSync(resolve(root, path), 'utf8');

test('public pages never reveal site maintenance instructions', () => {
  const pages = [read('src/pages/publications.astro'), read('src/pages/notes/index.astro')];
  for (const page of pages) {
    assert.doesNotMatch(page, /Publication metadata is maintained in BibTeX/);
    assert.doesNotMatch(page, /New papers are added by editing/);
    assert.doesNotMatch(page, /src\/data\/publications\.bib/);
    assert.doesNotMatch(page, /Browse study notes ↗/);
  }
  assert.match(pages[0], /Google Scholar ↗/);
});

test('archive search provides an accessible visible reset for active filters', () => {
  for (const path of ['src/pages/publications.astro', 'src/pages/notes/index.astro']) {
    assert.match(read(path), /data-filter-reset-all hidden/);
  }
  const controller = read('public/scripts/search-filter.js');
  assert.match(controller, /resetAll\.hidden/);
  assert.match(controller, /resetAll\.addEventListener/);
  assert.match(controller, /Keyword: /);
});

test('all navigation symbols reflect destinations', () => {
  const home = read('src/pages/index.astro');
  assert.match(home, /Explore research →/);
  assert.match(home, /Academic CV ↗/);
  assert.doesNotMatch(home, /Browse study notes/);
  const header = read('src/components/Header.astro');
  assert.doesNotMatch(header, /Email ↗/);
  const layout = read('src/layouts/SiteLayout.astro');
  assert.doesNotMatch(layout, /Email ↗/);
});

test('shared styles improve body copy legibility and preserve single CSS stack', () => {
  const css = read('src/styles/site.css');
  assert.match(css, /VISITOR POLISH · 2026-10-29/);
  assert.match(css, /\.design-h \.home-hero-portrait \.hero-copy \{ font-size: 17px/);
  assert.match(css, /\.design-h \.paper-title:hover \{ color: var\(--ink\); \}/);
  assert.match(read('src/layouts/SiteLayout.astro'), /import '\.\.\/styles\/site\.css'/);
});

test('Research preserves the original illustration and caption', () => {
  const svg = read('public/research/quaternion-kahler-geometry.svg');
  assert.match(svg, />Kähler geometry<\/text>/);
  assert.match(svg, />Quaternion<\/text>/);
  const research = read('src/pages/research.astro');
  assert.match(research, /figure-comparison/);
  assert.match(research, /View larger ↗/);
  assert.doesNotMatch(research, /figure-explainer/);
});
