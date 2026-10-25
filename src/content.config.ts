import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    topic: z.string().default('Study notes'),
    status: z.enum(['published', 'draft']).default('published'),
    pdf: z.string().optional(),
    downloads: z.array(z.object({ label: z.string(), href: z.string() })).default([]),
  }),
});
export const collections = { notes };
