# datawise.dev

The Datawise blog as a static [Astro](https://astro.build) site, served by Cloudflare
(Workers static assets). Migrated from Hashnode in September 2026.

## Writing a post

Add `src/content/posts/<slug>.md`. The file name is the URL: `/<slug>`.

```yaml
---
title: "Using WHERE inside aggregate functions"
seoTitle: "BigQuery: filter aggregates with WHERE"   # optional, <title> and og:title
seoDescription: "One or two sentences for search results."
datePublished: 2026-09-22T06:52:46Z
dateUpdated: 2026-10-01T09:00:00Z                  # optional
cover: "/images/<slug>/cover.jpg"                  # optional
series: "practical-sql"                            # optional, a key of src/data/series.json
tags: ["bigquery", "sql"]                          # optional, keys of src/data/tags.json
canonical: "https://www.notjustsql.com/p/..."      # only for posts syndicated from the newsletter
---
```

Put images in `public/images/<slug>/` and reference them as `/images/<slug>/1.png`. Give every
image alt text that says what it shows; for SQL, name the functions, tables and columns. Better
still, put the SQL in a fenced code block so it can be searched and copied.

The build fails if frontmatter is missing or wrong (schema in `src/content.config.ts`).

## Commands

| Command | What it does |
|---|---|
| `npm install` | Install dependencies |
| `npm run dev` | Local dev server with live reload (search doesn't work here) |
| `npm run build` | Build to `dist/` and index it for search (Pagefind) |
| `npm run preview` | Serve `dist/` with Cloudflare's runtime, so redirects and URLs behave as in production |
| `npm run check` | Compare `dist/` with the old Hashnode site, page by page |

## What's where

- `src/content/posts/` – the posts
- `public/images/` – post images and covers
- `src/data/` – series, tags, comments archived from Hashnode, Hashnode's heading ids
- `public/_redirects`, `public/_headers` – Cloudflare redirects and headers
- `wrangler.jsonc` – Cloudflare config
- `scripts/export_hashnode.py` – the one-off export from Hashnode (cached in `.export-cache/`)
- `scripts/apply_alt_text.py` + `scripts/image-alt.json` – image alt text
- `scripts/image-code.json` – code transcribed from SQL/code screenshots, not yet in the posts
- `scripts/check_parity.py` – old-vs-new comparison

## Kept from Hashnode

- Every post URL (`/<slug>`, no trailing slash), plus `/<slug>.md` Markdown copies
- Titles, meta descriptions and canonical URLs (10 posts canonicalise to notjustsql.com)
- Heading anchors (`#heading-…`) that Google shows as sitelinks
- `/rss.xml`, `/sitemap.xml`, `/archive`, `/series/<slug>`, `/tag/<slug>`
- Hashnode's 15 old-slug redirects, in `public/_redirects`

## Going live

1. Push this repo to GitHub.
2. Cloudflare dashboard → Workers & Pages → Create → Import a repository. Build command
   `npm run build`, deploy command `npx wrangler deploy`.
3. Check the `*.workers.dev` address it gives you; `npm run check` has already compared the
   content against Hashnode.
4. Before touching DNS:
   - Hashnode dashboard → export newsletter subscribers, if any (the newsletter feature is on).
   - Cloudflare → Email Routing: recreate the datawise.dev forwarding addresses (Namecheap's
     forwarding stops once DNS moves).
5. Cloudflare → Add a domain → `datawise.dev` (free plan). Check the imported DNS records include
   the `google-site-verification` TXT record (Search Console) before switching.
6. Screenshot the Namecheap DNS records, then Namecheap → datawise.dev → Nameservers →
   Custom DNS → the two Cloudflare nameservers.
7. Once the zone is active: Workers & Pages → datawise → Settings → Domains → add `datawise.dev`,
   and a redirect rule `www.datawise.dev/*` → `https://datawise.dev/${1}` (301).
8. Turn off the `workers.dev` address (Settings → Domains) so there's only one copy of the site.
9. Leave the custom domain set in Hashnode, so `cnstlungu.hashnode.dev` keeps redirecting here
   rather than serving a second copy. Keep the Hashnode blog for a few months as a fallback.
10. Search Console → Sitemaps → resubmit `https://datawise.dev/sitemap.xml`, then watch clicks.

Rollback: switch the nameservers back to Namecheap BasicDNS and check the records from the
screenshot are there.
