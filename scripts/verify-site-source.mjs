import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { parseBibtex } from '../src/lib/bibtex.mjs';
const root=resolve(import.meta.dirname,'..');
const read=(p)=>readFileSync(join(root,p),'utf8');
const required=['src/pages/index.astro','src/pages/research.astro','src/pages/publications.astro','src/pages/notes/index.astro','src/pages/notes/[slug].astro','src/pages/about.astro','src/layouts/SiteLayout.astro','src/components/PaperCard.astro','src/components/SearchFilter.astro','src/content.config.ts'];
for (const path of required) if(!existsSync(join(root,path))) throw Error(`Missing critical source file: ${path}`);
const bib=parseBibtex(read('src/data/publications.bib'));
const meta=JSON.parse(read('src/data/publication-meta.json'));
const allowed=new Set(['Quantum Geometry','Band Topology','Many-Body Physics']);
const ids=new Set();
for(const p of bib){
 if(ids.has(p.id))throw Error(`Duplicate BibTeX key: ${p.id}`); ids.add(p.id);
 if(!p.title || !p.author || !p.year)throw Error(`Missing required publication metadata: ${p.id}`);
 const m=meta[p.id];if(!m)throw Error(`Missing publication-meta.json entry: ${p.id}`);
 if(!Array.isArray(m.areas) || !m.areas.length || new Set(m.areas).size!==m.areas.length || m.areas.some(a=>!allowed.has(a)))throw Error(`Invalid areas for ${p.id}`);
 if(!Array.isArray(m.tags))throw Error(`Invalid tags for ${p.id}`);
}
for(const id of Object.keys(meta))if(!ids.has(id))throw Error(`Orphan publication metadata: ${id}`);
const files=readdirSync(join(root,'src/content/notes')).filter(f=>f.endsWith('.md'));
const notes=new Map();
for(const f of files){
 const contents=read(`src/content/notes/${f}`);let header=contents.match(/^---\s*\n([\s\S]*?)\n---/);
 if(!header)throw Error(`Missing frontmatter: ${f}`);
 let body=header[1];
 const get=(key)=>body.match(new RegExp(`^${key}:\\s*(.*)$`,'m'))?.[1]?.trim();
 const slug=f.slice(0,-3);notes.set(slug,{f,body,slug,status:get('status'),pdf:get('pdf')?.replace(/^['"]|['"]$/g,'')});
 if(!get('title') || !get('category') || !get('status'))throw Error(`Missing metadata in ${f}`);
 if(!/^tags:\s*(?:\[|\n\s+- )/m.test(body))throw Error(`Missing note tags: ${f}`);
 const pdf=get('pdf')?.replace(/^['"]|['"]$/g,'');
 if(get('status')==='published' && pdf && !existsSync(join(root,'public',pdf.replace(/^\//,''))))throw Error(`Missing public PDF: ${pdf}`);
}
for(const note of notes.values()){
 const rels=[...note.body.matchAll(/^\s+- note:\s*([a-zA-Z0-9-]+)\s*$/gm)].map(m=>m[1]);
 for(const rel of rels)if(!notes.has(rel))throw Error(`Missing relation target in ${note.f}: ${rel}`);
}
console.log(`Verified critical pages, ${bib.length} papers, ${notes.size} notes, links and relationships.`);
