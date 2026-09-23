// Sätteri hast plugins used by astro.config.mjs.
import { existsSync, readFileSync } from 'node:fs';
import { basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { imageSize } from 'image-size';
import { MAX_WIDTH, webpFor } from './webp.mjs';

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

// Images live in public/images/<slug>/. Give them intrinsic sizes (no layout shift), load
// them lazily, serve the WebP copy when there is one, and have Pagefind index their alt text.
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

const escapeAttr = (v) =>
  String(v).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export const imageAttributes = {
  name: 'image-attributes',
  element: {
    filter: ['img'],
    visit(node, ctx) {
      const { src, alt, title } = node.properties ?? {};
      if (typeof src !== 'string' || !src.startsWith('/images/')) return;
      const size = sizeOf(decodeURI(src));
      const attrs = {
        src,
        alt: alt ?? '',
        title,
        loading: 'lazy',
        decoding: 'async',
        width: size?.width,
        height: size?.height,
        // Site search indexes the alt text, which describes the SQL in the image.
        // Sätteri drops data-* set via setProperty, hence the raw node.
        'data-pagefind-index-attrs': 'alt',
      };
      const html = Object.entries(attrs)
        .filter(([, v]) => v != null)
        .map(([k, v]) => `${k}="${escapeAttr(v)}"`)
        .join(' ');
      const webp = webpFor(src);
      const img = `<img ${html}>`;
      let value = webp ? `<picture><source srcset="${escapeAttr(webp)}" type="image/webp">${img}</picture>` : img;
      // The WebP copy of a very wide screenshot is scaled down; link to the original for reading the detail.
      if (webp && size && size.width > MAX_WIDTH) value = `<a href="${escapeAttr(src)}" title="Open full-size image">${value}</a>`;
      ctx.replaceNode(node, { type: 'raw', value });
    },
  },
};
