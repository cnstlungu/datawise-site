// @ts-check
import { satteri } from '@astrojs/markdown-satteri';
import { defineConfig } from 'astro/config';
import { hashnodeHeadingIds, imageAttributes } from './src/lib/markdown-plugins.mjs';

export default defineConfig({
  site: 'https://datawise.dev',
  // Hashnode served every post at /<slug> with no trailing slash. `file` builds /<slug>.html,
  // which Cloudflare serves at /<slug>, so every URL Google knows stays exactly the same.
  build: { format: 'file' },
  trailingSlash: 'never',
  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      wrap: true,
    },
    processor: satteri({
      hastPlugins: [hashnodeHeadingIds, imageAttributes],
    }),
  },
});
