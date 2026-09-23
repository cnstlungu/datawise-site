#!/usr/bin/env python3
"""Compare the built site (dist/) with the live Hashnode site, page by page.

For every URL in the live sitemap, checks that the new page exists and keeps the same
<title>, meta description, canonical URL and heading anchors, and that the article text
and image count match. Run after `npm run build`. Live pages come from the export cache.
Exit code 1 if anything is off.
"""
import difflib
import html as htmllib
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from export_hashnode import (SITE, deref, fetch, find_object, html_meta,  # noqa: E402
                             rsc_rows, sitemap_paths)

DIST = Path(__file__).resolve().parent.parent / "dist"
EXPECTED_LOSS = r"https|github com cnstlungu [0-9a-f]+|title .* seotitle .* slug .*"


def words(fragment: str) -> list[str]:
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S)
    text = htmllib.unescape(re.sub(r"<[^>]+>", " ", fragment))
    # Compare words only: punctuation differs (smart quotes, escaped underscores).
    return re.findall(r"[\w]+", text.lower())


def local_file(path: str) -> Path:
    return DIST / (f"{path}.html" if path else "index.html")


def main() -> int:
    problems: list[str] = []
    paths = sitemap_paths()
    posts = 0
    for path in paths:
        f = local_file(path)
        # Exact-case match: macOS filesystems are case-insensitive, Cloudflare isn't.
        if not f.exists() or f.name not in os.listdir(f.parent):
            if path not in ("recommendations",):
                problems.append(f"/{path}: missing from dist")
            continue
        live_page = fetch(f"{SITE}/{path}")[0].decode()
        local_page = f.read_text()
        live, local = html_meta(live_page), html_meta(local_page)
        if path.startswith("series/") or path == "archive":
            continue  # listing pages: existence is what matters

        for key in ("title", "description"):
            if (live[key] or "").strip() != (local[key] or "").strip():
                problems.append(f"/{path}: {key} differs\n    live:  {live[key]}\n    local: {local[key]}")
        if (live["canonical"] or "").rstrip("/") != (local["canonical"] or "").rstrip("/"):
            problems.append(f"/{path}: canonical differs: live={live['canonical']} local={local['canonical']}")

        rows = rsc_rows(live_page)
        post = find_object(rows, '"post":', lambda v: isinstance(v, dict) and v.get("slug") == path
                           and isinstance(v.get("content"), dict))
        if not post:
            continue
        posts += 1
        live_html = deref(rows, post["content"]["html"]) or ""
        body = re.search(r'<div class="prose" data-pagefind-body>(.*?)</div>\s*(?:<ul class="tag-list"|<nav|<aside)',
                         local_page, re.S)
        local_html = body.group(1) if body else ""

        ids = re.findall(r'<h[1-6][^>]*\bid="([^"]+)"', live_html)
        missing = [i for i in ids if f'id="{i}"' not in local_html]
        if missing:
            problems.append(f"/{path}: heading anchors missing: {missing}")

        live_imgs = len(re.findall(r"<img\b", live_html))
        local_imgs = len(re.findall(r"<img\b", local_html))
        if live_imgs != local_imgs:
            problems.append(f"/{path}: images live={live_imgs} local={local_imgs}")

        lw, cw = words(live_html), words(local_html)
        # Share of the live text that survives in order. Two losses are intended: gist embed
        # URLs (replaced by the gist's code) and frontmatter Hashnode rendered as body text.
        matcher = difflib.SequenceMatcher(None, lw, cw, autojunk=False)
        lost = 0
        for tag, i1, i2, _, _ in matcher.get_opcodes():
            gone = " ".join(lw[i1:i2])
            if tag in ("delete", "replace") and not re.fullmatch(EXPECTED_LOSS, gone):
                lost += i2 - i1
        kept = 1 - lost / max(1, len(lw))
        if kept < 0.98:
            problems.append(f"/{path}: only {kept:.1%} of the live text found locally")

    print(f"checked {len(paths)} sitemap URLs ({posts} posts)")
    for p in problems:
        print(" -", p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
