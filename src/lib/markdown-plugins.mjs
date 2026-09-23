// Sätteri hast plugins used by astro.config.mjs.
import { existsSync, readFileSync } from 'node:fs';
import { basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { imageSize } from 'image-size';

const root = new URL('../../', import.meta.url);
const headingIds = JSON.parse(readFileSync(new URL('src/data/heading-ids.json', root), 'utf8'));

// Hashnode's heading ids ("heading-what-is-a-cte" on older posts, no prefix on newer ones)
// don't match Astro's slugger, and Google links to them as sitelinks. Reuse the exported ids.
const comparable = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '');

export function hashnodeHeadingIds(ctx) {
  if (!ctx.fileURL) return null;
  const known = headingIds[basename(fileURLToPath(ctx.fileURL), '.md')];
  if (!known) return null;
  let next = 0;
  return {
    name: 'hashnode-heading-ids',
    element: {
      filter: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
      visit(node, vctx) {
        const text = comparable(vctx.textContent(node));
        // Both lists are in document order; skip past headings Hashnode didn't render.
        for (let i = next; i < known.length; i++) {
          if (comparable(known[i].text) === text) {
            vctx.setProperty(node, 'id', known[i].id);
            next = i + 1;
            return;
          }
        }
      },
    },
  };
}

// Images live in public/images/<slug>/. Give them intrinsic sizes (no layout shift) and
// load them lazily.
const sizeCache = new Map();
function sizeOf(src) {
  if (!sizeCache.has(src)) {
    const file = new URL(`public${src}`, root);
    let size = null;
    if (existsSync(file)) {
      try {
        const { width, height } = imageSize(readFileSync(file));
        size = { width, height };
      } catch {
        // Unreadable header: leave the image unsized rather than fail the build.
      }
    }
    sizeCache.set(src, size);
  }
  return sizeCache.get(src);
}

export const imageAttributes = {
  name: 'image-attributes',
  element: {
    filter: ['img'],
    visit(node, ctx) {
      const src = node.properties?.src;
      if (typeof src !== 'string' || !src.startsWith('/images/')) return;
      ctx.setProperty(node, 'loading', 'lazy');
      ctx.setProperty(node, 'decoding', 'async');
      const size = sizeOf(decodeURI(src));
      if (size && node.properties.width == null) {
        ctx.setProperty(node, 'width', size.width);
        ctx.setProperty(node, 'height', size.height);
      }
    },
  },
};
