import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '..');
const read = p => readFileSync(resolve(root,p),'utf8');
test('Students pages are present and use the existing SiteLayout',()=>{
  const list=read('src/pages/students/index.astro');
  const story=read('src/pages/students/band-theory.astro');
  assert.match(list,/SiteLayout active="students"/);
  assert.match(story,/students-essay\.html\?raw/);
  assert.match(read('src/components/Header.astro'),/id:'students'/);
  assert.match(read('src/pages/sitemap.xml.ts'),/\/students\/band-theory\//);
});
test('story keeps six milestone boxes and clean clickable sources',()=>{
  const story=read('src/data/students-essay.html');
  assert.equal((story.match(/class="milestone (?:blue|amber|stone|green)?"/g)||[]).length,6);
  assert.doesNotMatch(story,/>Original paper/);
  assert.match(story,/references-list/);
  assert.match(story,/target="_blank"/);
});
test('Students and Research share the exact QK SVG path',()=>{
  const story=read('src/data/students-essay.html');
  const research=read('src/pages/research.astro');
  const p='public/research/quaternion-kahler-geometry.svg';
  assert.ok(existsSync(resolve(root,p)));
  assert.match(story,/\/research\/quaternion-kahler-geometry\.svg/);
  assert.match(research,/\/research\/quaternion-kahler-geometry\.svg/);
});

test('clean presentation removes decorative signoff and TOC footer and prevents heading collision',()=>{
  assert.doesNotMatch(read('src/data/students-landing.html'),/electron-signoff|A recurring guide/);
  assert.doesNotMatch(read('src/data/students-essay.html'),/toc-note|6 featured milestone boxes/);
  assert.match(read('src/styles/students.css'),/\.ps-students \.story-section > \.section-heading\{display:block/);
});

test('Students heading matches primary page title hierarchy',()=>{
 const list=read('src/data/students-landing.html');
 assert.match(list,/<header class="page-heading">/);
 assert.match(list,/<h1>For Students<span class="title-dot">\.<\/span><\/h1>/);
 assert.match(list,/<h2>Physics Stories<\/h2>/);
 assert.doesNotMatch(list,/<h1>Physics Stories/);
});
