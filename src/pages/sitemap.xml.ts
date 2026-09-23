import type { APIRoute } from 'astro';
import { SITE } from '../consts';
import series from '../data/series.json';
import { listedPosts, postPath } from '../lib/posts';

// Kept at /sitemap.xml, the path already submitted in Search Console.
export const GET: APIRoute = async () => {
  const posts = await listedPosts();
  // A post whose canonical points to the newsletter isn't ours to list.
  const ownPosts = posts.filter((p) => !p.data.canonical);
  const newest = posts[0].data.dateUpdated ?? posts[0].data.datePublished;

  const urls: { loc: string; lastmod?: Date }[] = [
    { loc: '/', lastmod: newest },
    { loc: '/archive', lastmod: newest },
    ...Object.keys(series)
      .filter((slug) => posts.some((p) => p.data.series === slug))
      .map((slug) => ({ loc: `/series/${slug}` })),
    ...ownPosts.map((p) => ({ loc: postPath(p), lastmod: p.data.dateUpdated ?? p.data.datePublished })),
  ];

  const body = urls
    .map(({ loc, lastmod }) => {
      const url = new URL(loc, SITE.url).href.replace(/\/$/, loc === '/' ? '/' : '');
      return `  <url><loc>${url}</loc>${lastmod ? `<lastmod>${lastmod.toISOString()}</lastmod>` : ''}</url>`;
    })
    .join('\n');

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
  );
};
