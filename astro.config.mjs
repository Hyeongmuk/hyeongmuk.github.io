import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// This repo targets the EXISTING hyeongmuk.github.io account by default.
// If you change the GitHub username or add a custom domain, update `site`.
export default defineConfig({
  site: 'https://mookphysics.org',
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
});
