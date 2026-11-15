import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
test('shared filter script drives the archive controls',()=>{
  // The filter markup on both archive pages is checked on the built pages (scripts/verify-built-site.mjs).
  assert.match(read('public/scripts/search-filter.js'),/data-search-controls/);
});
test('site is indexable and uses one stylesheet',()=>{
  const layout=read('src/layouts/SiteLayout.astro');
  assert.match(layout,/site.css/);
  assert.doesNotMatch(layout,/noindex/);
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
