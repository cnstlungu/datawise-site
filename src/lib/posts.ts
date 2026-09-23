import { type CollectionEntry, getCollection } from 'astro:content';
import seriesData from '../data/series.json';
import tagData from '../data/tags.json';

export type Post = CollectionEntry<'posts'>;
export type SeriesSlug = keyof typeof seriesData;

const newestFirst = (a: Post, b: Post) => b.data.datePublished.valueOf() - a.data.datePublished.valueOf();

/** Every post, including delisted ones (they keep their URL). Newest first. */
export async function allPosts(): Promise<Post[]> {
  return (await getCollection('posts')).sort(newestFirst);
}

/** Posts that appear in listings, feeds and the sitemap. Newest first. */
export async function listedPosts(): Promise<Post[]> {
  return (await allPosts()).filter((p) => !p.data.delisted);
}

export const postPath = (post: Post) => `/${post.id}`;

export const seriesInfo = (slug: string) => (seriesData as Record<string, { name: string; description?: string }>)[slug];

export const tagName = (slug: string) => (tagData as Record<string, string>)[slug] ?? slug;

export function readingMinutes(post: Post): number {
  const words = (post.body ?? '').replace(/```[\s\S]*?```/g, ' ').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}

export const formatDate = (d: Date) =>
  d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
