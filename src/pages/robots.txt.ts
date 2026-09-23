import type { APIRoute } from 'astro';
import { SITE } from '../consts';

// Everyone, AI crawlers included, may read everything.
export const GET: APIRoute = () =>
  new Response(`User-agent: *\nAllow: /\n\nSitemap: ${SITE.url}/sitemap.xml\n`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
