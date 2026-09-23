import rss from '@astrojs/rss';
import type { APIRoute } from 'astro';
import { SITE } from '../consts';
import { listedPosts, postPath, tagName } from '../lib/posts';

export const GET: APIRoute = async () =>
  rss({
    title: SITE.title,
    description: SITE.description,
    site: SITE.url,
    items: (await listedPosts()).map((post) => ({
      title: post.data.title,
      link: postPath(post),
      pubDate: post.data.datePublished,
      description: post.data.seoDescription,
      categories: post.data.tags.map(tagName),
    })),
  });
