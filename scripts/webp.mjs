// Writes a WebP copy next to every PNG/JPEG in public/images (`1.png` -> `1.png.webp`, gitignored),
// at most MAX_WIDTH wide. Posts and covers serve it through <picture> when it's meaningfully smaller
// (see webpFor in src/lib/markdown-plugins.mjs); the original stays at its URL for feeds, social
// previews and image search. Runs before `astro build`; up-to-date copies are skipped.
import { readdirSync, statSync } from 'node:fs';
import { availableParallelism } from 'node:os';
import { basename, join } from 'node:path';
import sharp from 'sharp';
import { COVER_WIDTH, MAX_WIDTH } from '../src/lib/webp.mjs';

const ROOT = new URL('../public/images/', import.meta.url).pathname;
const COVER_QUALITY = 75;
const QUALITY = { '.png': 90, '.jpg': 82, '.jpeg': 82 }; // PNGs are mostly text screenshots: keep them crisp

const sources = readdirSync(ROOT, { recursive: true })
  .map((f) => join(ROOT, f))
  .filter((f) => /\.(png|jpe?g)$/i.test(f));

const fresh = (src, out) => {
  try {
    return statSync(out).mtimeMs >= statSync(src).mtimeMs;
  } catch {
    return false;
  }
};

const todo = sources.filter((src) => !fresh(src, `${src}.webp`));
const started = Date.now();
let next = 0;
async function worker() {
  while (next < todo.length) {
    const src = todo[next++];
    const cover = basename(src).startsWith('cover.');
    const quality = cover ? COVER_QUALITY : QUALITY[src.slice(src.lastIndexOf('.')).toLowerCase()];
    await sharp(src)
      .resize({ width: cover ? COVER_WIDTH : MAX_WIDTH, withoutEnlargement: true })
      .webp({ quality, effort: 5 })
      .toFile(`${src}.webp`);
  }
}
await Promise.all(Array.from({ length: Math.min(4, availableParallelism()) }, worker));
console.log(`webp: ${todo.length} converted, ${sources.length - todo.length} up to date (${Date.now() - started} ms)`);
