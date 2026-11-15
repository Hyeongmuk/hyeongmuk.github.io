// Checks the built site in dist/ (runs after `npm run build`). Prefer checks here over regexes on
// source files: they test what visitors get, so refactors that keep the output unchanged still pass.
import {existsSync,readdirSync,readFileSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {parseBibtex,publicationFromBib} from '../src/lib/bibtex.mjs';
const root=resolve(import.meta.dirname,'..');
const dist=join(root,'dist');
const html=(p)=>readFileSync(join(dist,p),'utf8');
const fail=(msg)=>{throw Error(msg);};

const needed=['index.html','research/index.html','publications/index.html','notes/index.html','about/index.html','sitemap.xml'];
for(const p of needed)if(!existsSync(join(dist,p)))fail(`Build is incomplete. Missing ${p}`);

const notes=readdirSync(join(root,'src/content/notes')).filter(f=>f.endsWith('.md')).map(f=>{
  const src=readFileSync(join(root,'src/content/notes',f),'utf8');
  return {slug:f.slice(0,-3),published:/^status:\s*published\s*$/m.test(src),featured:Number(src.match(/^featured:\s*(\d+)\s*$/m)?.[1]||0)};
});
for(const n of notes)if(n.published&&!existsSync(join(dist,'notes',n.slug,'index.html')))fail(`Missing note page: ${n.slug}`);

// Both archives use the shared search/keyword filter, including the reset control.
for(const p of ['notes/index.html','publications/index.html']){
  const page=html(p);
  for(const marker of ['data-search-controls','data-keyword-filter','data-filter-reset-all','data-filter-item','data-keywords='])
    if(!page.includes(marker))fail(`${p}: shared filter marker missing: ${marker}`);
}

// Paper titles are plain headings (no duplicate link next to the DOI/arXiv links).
for(const p of ['index.html','research/index.html','publications/index.html']){
  for(const m of html(p).matchAll(/<h3 class="paper-title">([\s\S]*?)<\/h3>/g))
    if(/<a\b/.test(m[1]))fail(`${p}: paper title is a link: ${m[1].slice(0,60)}`);
}

// Paper cards link out via DOI/arXiv only, never to a duplicate PDF.
for(const p of ['index.html','research/index.html','publications/index.html']){
  for(const m of html(p).matchAll(/<article class="paper-row[\s\S]*?<\/article>/g))
    if(/href="[^"]*\.pdf/.test(m[0]))fail(`${p}: paper card links to a PDF`);
}

// H design structure: sidebar navigation everywhere, note cards and paper rows on the archives.
for(const p of needed.filter(p=>p.endsWith('.html')))if(!html(p).includes('desktop-nav'))fail(`${p}: sidebar navigation missing`);
if(!html('notes/index.html').includes('class="note-row"'))fail('notes: note cards missing');
if(!html('publications/index.html').includes('class="paper-row'))fail('publications: paper rows missing');

// Research "Related publications" in each established section match the papers' areas.
const meta=JSON.parse(readFileSync(join(root,'src/data/publication-meta.json'),'utf8'));
const papers=parseBibtex(readFileSync(join(root,'src/data/publications.bib'),'utf8')).map(e=>publicationFromBib(e,meta[e.id]));
const research=html('research/index.html');
const sectionHtml=(id)=>{const start=research.indexOf(`id="${id}"`);const next=research.indexOf('<article class="research-chapter"',start+1);return research.slice(start,next<0?undefined:next);};
for(const [id,area] of [['geometry','Quantum Geometry'],['topology','Band Topology']]){
  const block=sectionHtml(id);
  for(const p of papers){
    const listed=block.includes(`<h3 class="paper-title">${p.title}</h3>`);
    if(p.areas.includes(area)!==listed)fail(`research #${id}: paper "${p.title}" ${listed?'should not be':'should be'} listed`);
  }
}

// Home shows the featured notes in their frontmatter order.
const expected=notes.filter(n=>n.published&&n.featured).sort((a,b)=>a.featured-b.featured).map(n=>n.slug);
const shown=[...html('index.html').matchAll(/<div class="small-note">[\s\S]*?<h3><a href="\/notes\/([^/]+)\//g)].map(m=>m[1]);
if(JSON.stringify(shown)!==JSON.stringify(expected))fail(`Home featured notes ${JSON.stringify(shown)} != ${JSON.stringify(expected)}`);

// Style decisions the owner made, checked on the built CSS whatever selector carries them.
const css=readdirSync(join(dist,'_astro')).filter(f=>f.endsWith('.css')).map(f=>readFileSync(join(dist,'_astro',f),'utf8')).join('\n');
if(!/\.hero-copy[^{}]*\{[^}]*font-size:17px/.test(css))fail('Home hero copy is no longer 17px');
const hover=[...css.matchAll(/\.paper-title:hover[^{}]*\{([^}]*)\}/g)].map(m=>m[1]).filter(d=>/color:/.test(d)).pop();
if(!hover||!/color:var\(--ink\)/.test(hover))fail('Paper title hover colour is no longer var(--ink)');

console.log('Verified main pages, note routes, shared filters, paper titles, Research papers, Home notes and key styles in dist/.');
