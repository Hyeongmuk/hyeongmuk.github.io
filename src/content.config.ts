import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    title: z.string(), description: z.string(), date: z.coerce.date(),
    topic: z.string().default('Study notes'),
    category: z.enum(['qft','mathematics','condensed']),
    tags: z.array(z.string()).default([]),
    relations: z.array(z.object({
      note: z.string(),
      type: z.enum(['companion','supplement_to','related']),
      description: z.string().optional(),
    })).default([]),
    featured: z.boolean().default(false),
    complete: z.boolean().default(false), pages: z.number().int().positive().optional(),
    status: z.enum(['published','draft']).default('draft'),
    pdf: z.string().optional(),
    downloads: z.array(z.object({ label: z.string(), href: z.string() })).default([]),
  }),
});
export const collections = { notes };
