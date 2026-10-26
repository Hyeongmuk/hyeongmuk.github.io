import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
const read = p => readFileSync(new URL(`../${p}`,import.meta.url),'utf8');

test('homepage uses the two user-selected featured papers',()=>{
  const meta=JSON.parse(read('src/data/publication-meta.json'));
  assert.deepEqual(Object.keys(meta).filter(k=>meta[k].featured).sort(),[
    'lim2023hopf','lim2026quaternion']);
});
test('research distinguishes demonstrated results from future interests',()=>{
  const s=read('src/pages/research.astro');
  assert.match(s,/ESTABLISHED RESEARCH/);
  assert.match(s,/BROADER RESEARCH INTERESTS/);
  assert.match(s,/not yet a demonstration/);
  assert.match(s,/generalized symmetries/);
});
test('academic profiles and photo are available',()=>{
  assert.ok(existsSync(new URL('../public/profile-hyeongmuk-lim.webp',import.meta.url)));
  assert.ok(existsSync(new URL('../public/downloads/Hyeongmuk_Lim_CV.pdf',import.meta.url)));
  assert.match(read('src/pages/about.astro'),/August 2027/);
  assert.match(read('src/pages/about.astro'),/Bohm-Jung Yang/);
  assert.match(read('src/pages/about.astro'),/0009-0001-0036-5355/);
});
test('all five archived notes are public and marked complete',()=>{
  const names=['bv-formalism','noncommutative-geometry','haldane-gap-lsm','cotangent-complex','planar-diagram-algebra-3d-tqft'];
  names.forEach(n=>{
    const text=read(`src/content/notes/${n}.md`);
    assert.match(text,/complete: true/);
    assert.match(text,/status: published/);
    const pdf=text.match(/^pdf: '\/downloads\/([^']+)'/m);
    assert.ok(pdf,`missing pdf field: ${n}`);
    assert.ok(existsSync(new URL(`../public/downloads/${pdf[1]}`,import.meta.url)));
  });
});
test('shared filtering and static SEO endpoints are retained',()=>{
  assert.match(read('src/pages/notes/index.astro'),/SearchFilter/);
  assert.match(read('src/pages/publications.astro'),/SearchFilter/);
  assert.match(read('src/layouts/SiteLayout.astro'),/schema.org/);
  assert.match(read('public/robots.txt'),/sitemap.xml/);
  assert.match(read('src/pages/sitemap.xml.ts'),/getCollection/);
});
