import {existsSync,readdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
const dist=resolve(import.meta.dirname,'../dist');
const needed=['index.html','research/index.html','publications/index.html','notes/index.html','about/index.html','sitemap.xml'];
for(const p of needed)if(!existsSync(join(dist,p)))throw Error(`Build is incomplete. Missing ${p}`);
const noteFiles=readdirSync(resolve(import.meta.dirname,'../src/content/notes')).filter(f=>f.endsWith('.md'));
for(const f of noteFiles){
 const src=join(import.meta.dirname,'../src/content/notes',f);
 const {readFileSync}=await import('node:fs');
 if(/^status:\s*published\s*$/m.test(readFileSync(src,'utf8'))&&!existsSync(join(dist,'notes',f.slice(0,-3),'index.html'))) throw Error(`Missing note page: ${f}`);
}
console.log('Verified main pages and published note routes in dist/.');
