import type { APIRoute } from 'astro';
import { AUTHOR, SITE } from '../consts';
import series from '../data/series.json';
import { listedPosts, type Post, postPath } from '../lib/posts';

// https://llmstxt.org — an index of the site for language models, linking the Markdown copies.
export const GET: APIRoute = async () => {
  const posts = (await listedPosts()).filter((p) => !p.data.canonical);
  const line = (p: Post) => `- [${p.data.title}](${SITE.url}${postPath(p)}.md): ${p.data.seoDescription}`;

  const sections = Object.entries(series)
    .map(([slug, s]) => ({ name: s.name, posts: posts.filter((p) => p.data.series === slug) }))
    .filter((s) => s.posts.length > 0)
    .map((s) => `## ${s.name}\n\n${s.posts.map(line).join('\n')}`);
  const loose = posts.filter((p) => !p.data.series);
  if (loose.length) sections.push(`## Other posts\n\n${loose.map(line).join('\n')}`);

  const text = [
    `# ${SITE.title}`,
    `> ${SITE.description}`,
    `Written by ${AUTHOR.name} (${AUTHOR.url}). Every post is also available as Markdown by adding .md to its URL.`,
    ...sections,
  ].join('\n\n');

  return new Response(`${text}\n`, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
