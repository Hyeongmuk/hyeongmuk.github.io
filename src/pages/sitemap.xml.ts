import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async () => {
  const base = 'https://mookphysics.org';
  const pages = ['/', '/research/', '/publications/', '/notes/', '/students/', '/students/band-theory/', '/about/'];
  const notes = await getCollection('notes', ({ data }) => data.status === 'published');
  for (const note of notes) pages.push(`/notes/${note.id}/`);
  const urls = pages.map(path => `  <url><loc>${base}${path}</loc></url>`).join('\n');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`, {
    headers: {'Content-Type': 'application/xml; charset=utf-8'}
  });
};
