import raw from '../data/publications.bib?raw';
import metadata from '../data/publication-meta.json';
import { parseBibtex, publicationFromBib } from './bibtex.mjs';
export const publications = parseBibtex(raw)
  .map((entry) => publicationFromBib(entry, metadata[entry.id] || {}))
  .sort((a, b) => b.year - a.year || b.month - a.month || a.title.localeCompare(b.title));
export const featuredPublications = publications.filter((p) => p.featured);
// Research uses the SAME publication records and the same newest-first order as Home and Publications.
export function researchPublications(area) {
  return publications.filter(p => p.areas.includes(area));
}
