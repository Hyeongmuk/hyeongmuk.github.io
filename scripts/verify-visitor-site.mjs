/**
 * Deployment safety check for the pages visitors actually see.
 * Run after Astro builds dist/ (no network, browsers, or extra dependencies).
 */
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, resolve, relative, sep } from 'node:path';

const dist = resolve(import.meta.dirname, '../dist');
const problems = [];
const pages = [];
function scan(dir) {
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    const file = join(dir, ent.name);
    if (ent.isDirectory()) scan(file);
    else if (ent.isFile() && ent.name.endsWith('.html')) pages.push(file);
  }
}
if (!existsSync(dist) || !statSync(dist).isDirectory()) {
  throw Error('dist/ is absent: run npm run build before verifying visitor pages.');
}
scan(dist);
if (!pages.length) throw Error('Build produced no HTML pages.');
const badCopy = [
  'Publication metadata is maintained in BibTeX',
  'New papers are added by editing',
  'src/data/publications.bib',
  'Browse study notes ↗',
];
const knownPages = ['index.html','research/index.html','publications/index.html',
  'notes/index.html','about/index.html','students/index.html'];
for (const path of knownPages) if (!existsSync(join(dist,path))) problems.push(`Missing primary route: ${path}`);

let checkedInternalLinks = 0;
for (const file of pages) {
  const html = readFileSync(file, 'utf8');
  const page = relative(dist,file).split(sep).join('/');
  for (const phrase of badCopy) if (html.includes(phrase)) problems.push(`${page}: developer-only copy appears publicly (${phrase})`);
  const htmlAnchorPattern = /<a\b[^>]*?\bhref\s*=\s*(["'])(.*?)\1[^>]*>/gi;
  for (const match of html.matchAll(htmlAnchorPattern)) {
    const link = match[2].replaceAll('&amp;', '&').trim();
    if (!link || link === '#') {
      problems.push(`${page}: a link has no destination (${link || '(empty)'})`);
      continue;
    }
    if (/^(?:https?:|mailto:|tel:|javascript:|data:|blob:|\/\/)/i.test(link) || link.startsWith('#')) continue;
    try {
      // Astro emits root-relative URLs. Handle relative links if authors add them.
      const origin = `https://mookphysics.org/${page === 'index.html' ? '' : page.replace(/index\.html$/, '')}`;
      const url = new URL(link, origin);
      if (url.origin !== 'https://mookphysics.org') continue;
      const pathname = decodeURIComponent(url.pathname);
      if (!pathname.startsWith('/') || pathname.includes('\0')) throw Error('invalid URL path');
      const rel = pathname.slice(1);
      const resolved = resolve(dist, rel);
      if (resolved !== dist && !resolved.startsWith(dist + sep)) throw Error('link escapes dist/');
      const target = pathname.endsWith('/') ? join(resolved, 'index.html') : resolved;
      if (!existsSync(target) || !statSync(target).isFile()) {
        // Extensionless relative routes are also accepted by Astro.
        if (!existsSync(join(resolved, 'index.html'))) problems.push(`${page}: broken internal link ${link}`);
      }
      checkedInternalLinks++;
    } catch (e) {
      problems.push(`${page}: invalid internal link ${link}: ${e.message}`);
    }
  }
}
if (problems.length) {
  console.error(problems.slice(0, 60).map(p => '  - ' + p).join('\n'));
  throw Error(`Public-site verification found ${problems.length} problem(s).`);
}
console.log(`PASS: ${pages.length} generated HTML pages and ${checkedInternalLinks} internal links checked; no maintenance copy.`);
