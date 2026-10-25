import raw from '../data/publications.bib?raw';
import metadata from '../data/publication-meta.json';
import { parseBibtex, publicationFromBib } from './bibtex.mjs';
export const publications = parseBibtex(raw)
  .map((entry) => publicationFromBib(entry, metadata[entry.id] || {}))
  .sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));
export const featuredPublications = publications.filter((p) => p.featured);
