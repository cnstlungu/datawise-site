// Shared by the markdown plugins (loaded by astro.config) and page templates (bundled by Vite,
// where import.meta.url points into dist/), so resolve files from the project root instead.
import { statSync } from 'node:fs';
import { join } from 'node:path';

const PUBLIC = join(process.cwd(), 'public');

// The content column is 704px. Screenshots and diagrams get room for 2x screens and zooming; cover
// photos (already well-compressed Unsplash JPEGs) only shrink meaningfully when resized.
export const MAX_WIDTH = 2000;
export const COVER_WIDTH = 1280;

/** URL of the WebP copy scripts/webp.mjs made for a /images/ file, if it's worth serving. */
export function webpFor(src) {
  if (!/\.(png|jpe?g)$/i.test(src)) return null;
  const original = join(PUBLIC, decodeURI(src));
  try {
    return statSync(`${original}.webp`).size < 0.9 * statSync(original).size ? `${src}.webp` : null;
  } catch {
    return null; // not generated (e.g. `astro dev` without the build script)
  }
}
