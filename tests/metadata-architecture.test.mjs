import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {parseBibtex,publicationFromBib} from '../src/lib/bibtex.mjs';
import {resolve} from 'node:path';
const read=p=>readFileSync(resolve(import.meta.dirname,'..',p),'utf8');
const meta=JSON.parse(read('src/data/publication-meta.json'));
const papers=parseBibtex(read('src/data/publications.bib')).map(x=>publicationFromBib(x,meta[x.id]));
test('publications support multiple research areas and retain selected highlights',()=>{
  const qk=papers.find(x=>x.id==='lim2026quaternion');
  assert.deepEqual(qk.areas,['Quantum Geometry','Band Topology']);
  assert.deepEqual(papers.filter(x=>x.featured).map(x=>x.id).sort(),['lim2023hopf','lim2026quaternion']);
  for(const p of papers)assert.ok(p.areas.length>=1);
});
test('Research and publication filtering reuse areas metadata',()=>{
  const research=read('src/pages/research.astro');
  const pub=read('src/pages/publications.astro');
  assert.match(research,/researchPublications\(section\.area\)/);
  assert.doesNotMatch(research,/ids:\s*\[/);
  assert.match(pub,/paper\.areas\.map/);
  assert.match(read('public/scripts/search-filter.js'),/\.split\('\|'\)\.includes\(area\)/);
});
test('shared publication component has no duplicate PDF or linked title',()=>{
  const card=read('src/components/PaperCard.astro');
  assert.match(card,/<h3 class="paper-title">\{paper\.title\}<\/h3>/);
  assert.doesNotMatch(card,/paper\.pdfUrl/);
});
test('archive note tags are curated and featured selection is optional',()=>{
  const schema=read('src/content.config.ts');
  const home=read('src/pages/index.astro');
  const bv=read('src/content/notes/bv-formalism.md');
  const ncg=read('src/content/notes/noncommutative-geometry.md');
  assert.match(bv, /Algebraic Geometry/);
  assert.match(ncg,/Algebraic Geometry/);
  assert.match(schema,/featured: z\.boolean\(\)\.default\(false\)/);
  assert.match(home,/candidates\.find\(n=>n\.data\.featured\)/);
});
