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
  // The reset sits with the search controls in the shared SearchFilter used by both archives.
  assert.match(read('src/components/SearchFilter.astro'), /data-filter-reset-all hidden/);
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

test('shared styles keep a single CSS stack', () => {
  // Hero copy size and paper-title hover colour are checked on the built CSS (scripts/verify-built-site.mjs).
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
  assert.match(read('src/data/research.json'), /"caption": "Comparison of Kähler geometry in Chern bands with quaternion-Kähler geometry of Kramers pairs\."/);
});
