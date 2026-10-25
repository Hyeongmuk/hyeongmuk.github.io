import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseBibtex, publicationFromBib } from '../src/lib/bibtex.mjs';

test('parses verified paper records', () => {
  const bib = readFileSync(new URL('../src/data/publications.bib', import.meta.url), 'utf8');
  const records = parseBibtex(bib);
  assert.equal(records.length, 4);
  assert.equal(records.find(r => r.id === 'lim2026quaternion').title,
    'Quaternion-Kähler geometry of time reversal symmetric crystals');
  assert.equal(publicationFromBib(records[0]).authors[0], 'Hyeongmuk Lim');
  assert.equal(publicationFromBib(records[0]).arxivUrl,
    'https://arxiv.org/abs/2608.03178');
});
test('keeps nested braces and quoted strings intact', () => {
  const p = parseBibtex('@article{key,title={A {Hopf} insulator}, author="Ada Lovelace and Emmy Noether",year=2026}');
  assert.equal(p[0].title, 'A Hopf insulator');
  assert.equal(publicationFromBib(p[0]).authors.length, 2);
});
