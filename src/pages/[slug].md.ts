import type { APIRoute, GetStaticPaths } from 'astro';
import { SITE } from '../consts';
import { allPosts, type Post } from '../lib/posts';

// Plain-Markdown copy of every post at /<slug>.md (Hashnode served the same URLs).
export const getStaticPaths = (async () =>
  (await allPosts()).map((post) => ({ params: { slug: post.id }, props: { post } }))) satisfies GetStaticPaths;

export const GET: APIRoute = ({ props }) => {
  const { post } = props as { post: Post };
  // Root-relative links and images only work on the site itself; make them absolute.
  const body = (post.body ?? '').replace(/\]\(\//g, `](${SITE.url}/`);
  return new Response(`# ${post.data.title}\n\n${body.trim()}\n`, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
};
