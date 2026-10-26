import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
const read = path => readFileSync(new URL('../'+path, import.meta.url),'utf8');
test('single H design stylesheet with original layer order',()=>{
 const layout=read('src/layouts/SiteLayout.astro');
 const css=read('src/styles/site.css');
 assert.match(layout,/import '\.\.\/styles\/site\.css'/);
 assert.doesNotMatch(layout, /styles\/(base|b|hybrid|production|refinement)\.css/);
 for(const section of ['BASE.CSS','B.CSS','HYBRID.CSS','PRODUCTION.CSS','REFINEMENT.CSS']) assert.ok(css.includes(section));
 for(const old of ['base','b','hybrid','production','refinement']) assert.equal(existsSync(new URL('../src/styles/'+old+'.css',import.meta.url)),false);
});
test('links label internal and new-tab navigation distinctly',()=>{
 const home=read('src/pages/index.astro');
 assert.match(home,/Explore research →/);
 assert.doesNotMatch(home,/Explore research ↗/);
 assert.match(home,/Academic CV ↗/);
});
test('research claims do not imply proven correlated phases',()=>{
 const s=read('src/pages/research.astro');
 assert.match(s,/starting point/);
 assert.match(s,/broader interests/);
 assert.doesNotMatch(s,/not yet a demonstration|rather than a claim/);
});
test('shared filter and mobile navigation preserved',()=>{
 const notes=read('src/pages/notes/index.astro');
 const pubs=read('src/pages/publications.astro');
 for(const s of [notes,pubs]) assert.match(s,/SearchFilter/);
 const h=read('src/components/Header.astro');
 assert.match(h,/aria-expanded="false"/);
 assert.match(h,/aria-label="Open navigation menu"/);
 assert.match(read('public/scripts/site.js'),/Escape/);
});
