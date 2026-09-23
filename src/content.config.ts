import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import series from './data/series.json';
import tags from './data/tags.json';

const seriesSlugs = Object.keys(series) as [string, ...string[]];
const tagSlugs = Object.keys(tags) as [string, ...string[]];

// The file name is the URL: src/content/posts/<slug>.md is served at /<slug>.
const posts = defineCollection({
  loader: glob({
    base: './src/content/posts',
    pattern: '*.md',
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    title: z.string(),
    subtitle: z.string().optional(),
    // <title> and og:title; falls back to `title`.
    seoTitle: z.string().optional(),
    seoDescription: z.string().min(1),
    datePublished: z.coerce.date(),
    dateUpdated: z.coerce.date().optional(),
    cover: z.string().startsWith('/images/').optional(),
    coverCredit: z.object({ name: z.string(), url: z.string().url() }).optional(),
    series: z.enum(seriesSlugs).optional(),
    tags: z.array(z.enum(tagSlugs)).default([]),
    // Set on posts syndicated from the newsletter, which point search engines there.
    canonical: z.string().url().optional(),
    // Reachable by URL but left out of listings, feeds and the sitemap.
    delisted: z.boolean().default(false),
    hashnodeCuid: z.string().optional(),
  }),
});

export const collections = { posts };
