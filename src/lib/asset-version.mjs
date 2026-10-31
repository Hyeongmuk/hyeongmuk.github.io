// Adds a content hash to a public/ asset URL (e.g. /scripts/site.js?v=1a2b3c4d) at build time.
// GitHub Pages caches these files for 10 minutes; a new hash makes browsers fetch the new file
// as soon as the HTML that references it is updated.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

export function versioned(path) {
  const hash = createHash('sha256').update(readFileSync(join(process.cwd(), 'public', path))).digest('hex').slice(0, 10);
  return `${path}?v=${hash}`;
}
