import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
test('both archives share the same search and keyword-filter component',()=>{
  for(const page of ['src/pages/notes/index.astro','src/pages/publications.astro']){
    assert.match(read(page),/import SearchFilter from/);
    assert.match(read(page),/<SearchFilter /);
    assert.match(read(page),/data-filter-item/);
    assert.match(read(page),/data-keywords=/);
  }
  assert.match(read('src/components/SearchFilter.astro'),/data-keyword-filter/);
  assert.match(read('public/scripts/search-filter.js'),/data-search-controls/);
});
test('site uses B sidebar and A editorial cards with a single stylesheet stack',()=>{
  const layout=read('src/layouts/SiteLayout.astro');
  assert.match(layout,/design-b design-h/);
  assert.match(layout,/site.css/);
  assert.match(read('src/styles/site.css'),/PRODUCTION.CSS/);
  assert.doesNotMatch(layout,/noindex/);
  assert.match(read('src/components/Header.astro'),/desktop-nav/);
  assert.match(read('src/components/NoteCard.astro'),/note-row/);
  assert.match(read('src/components/PaperCard.astro'),/paper-row/);
});
test('published study PDFs exist and their notes are categorized',()=>{
  const slugs=['bv-formalism','noncommutative-geometry','haldane-gap-lsm'];
  for(const slug of slugs){
    const raw=read(`src/content/notes/${slug}.md`);
    assert.match(raw,/category: '(qft|mathematics|condensed)'/);
    assert.match(raw,/tags:/);
    const m=raw.match(/pdf:\s*'([^']+)'/);
    assert.ok(m,`missing pdf in ${slug}`);
    const bytes=fs.readFileSync(path.join(root,'public',m[1].replace(/^\//,'')));
    assert.equal(bytes.subarray(0,5).toString(),'%PDF-');
  }
  assert.ok(!fs.existsSync(path.join(root,'src/content/notes/cluster-model.md')));
});
test('domain and automated deployment preserved',()=>{
 assert.match(read('astro.config.mjs'),/https:\/\/mookphysics\.org/);
 assert.match(read('.github/workflows/deploy.yml'),/npm run build/);
 assert.match(read('.github/workflows/deploy.yml'),/upload-pages-artifact/);
});
