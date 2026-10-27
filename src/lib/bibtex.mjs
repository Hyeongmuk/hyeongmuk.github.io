/* Lightweight BibTeX parser for the repository's controlled .bib file.
   Supports braced and quoted field values, nested braces, @comment, and @string.
   For complex BibLaTeX crossref/macro expansion, use a dedicated parser. */
function balanced(text, start, open, close) {
  let depth = 0;
  for (let i = start; i < text.length; i++) {
    const c = text[i];
    if (c === '\\') { i++; continue; }
    if (c === open) depth++;
    if (c === close && --depth === 0) return i;
  }
  throw Error('Unbalanced BibTeX entry');
}
function normalizeLatex(text) {
  return text
    .replace(/\\["{]\s*\{?a\}?/g, 'ä')
    .replace(/\\["{]\s*\{?A\}?/g, 'Ä')
    .replace(/\\["{]\s*\{?o\}?/g, 'ö')
    .replace(/\\["{]\s*\{?u\}?/g, 'ü')
    .replace(/\\&/g, '&')
    .replace(/\\textendash/g, '–')
    .replace(/\\_/g, '_')
    .replace(/[{}]/g, '')
    .replace(/\s+/g, ' ').trim();
}
function parseFields(body) {
  const fields = {};
  let i = 0;
  while (i < body.length) {
    while (i < body.length && /[\s,]/.test(body[i])) i++;
    const from = i;
    while (i < body.length && /[\w-]/.test(body[i])) i++;
    const name = body.slice(from, i).toLowerCase();
    if (!name) break;
    while (/\s/.test(body[i] || '') && i < body.length) i++;
    if (body[i++] !== '=') throw Error(`Expected = after ${name}`);
    while (/\s/.test(body[i] || '') && i < body.length) i++;
    let raw = '';
    if (body[i] === '{') {
      const end = balanced(body, i, '{', '}');
      raw = body.slice(i + 1, end); i = end + 1;
    } else if (body[i] === '"') {
      const start = ++i;
      while (i < body.length && !(body[i] === '"' && body[i-1] !== '\\')) i++;
      raw = body.slice(start, i); i++;
    } else {
      const start = i;
      while (i < body.length && body[i] !== ',') i++;
      raw = body.slice(start, i).trim();
    }
    fields[name] = normalizeLatex(raw);
  }
  return fields;
}
export function parseBibtex(input) {
  const entries = [];
  const source = input.replace(/^\s*%.*$/gm, '');
  const entryPattern = /@([a-zA-Z]+)\s*([({])/g;
  let match;
  while ((match = entryPattern.exec(source))) {
    const type = match[1].toLowerCase();
    const close = match[2] === '{' ? '}' : ')';
    const start = match.index + match[0].length - 1;
    // Find top-level end; entry content may contain quoted/braced values.
    let i = start + 1, depth = 1, quoted = false;
    for (; i < source.length; i++) {
      if (source[i] === '\\') { i++; continue; }
      if (source[i] === '"') quoted = !quoted;
      if (quoted) continue;
      if (source[i] === match[2]) depth++;
      if (source[i] === close && --depth === 0) break;
    }
    if (depth !== 0) throw Error(`Unbalanced entry at ${match.index}`);
    entryPattern.lastIndex = i + 1;
    if (['comment', 'preamble', 'string'].includes(type)) continue;
    const content = source.slice(start + 1, i);
    const comma = content.indexOf(',');
    if (comma === -1) throw Error(`BibTeX entry has no fields: ${content}`);
    const id = content.slice(0, comma).trim();
    entries.push({ id, type, ...parseFields(content.slice(comma + 1)) });
  }
  return entries;
}
export function publicationFromBib(entry, meta = {}) {
  return {
    ...entry, ...meta,
    areas: Array.isArray(meta.areas) ? meta.areas : (meta.area ? [meta.area] : []),
    year: Number(entry.year) || 0,
    authors: (entry.author || '').split(/\s+and\s+/i).map(s => s.trim()),
    topics: (entry.keywords || '').split(',').map(s => s.trim()).filter(Boolean),
    doiUrl: entry.doi ? `https://doi.org/${entry.doi}` : null,
    arxivUrl: entry.eprint ? `https://arxiv.org/abs/${entry.eprint.replace(/^arXiv:/i, '')}` : null,
    pdfUrl: entry.eprint ? `https://arxiv.org/pdf/${entry.eprint.replace(/^arXiv:/i, '')}` : null,
  };
}
