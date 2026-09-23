#!/usr/bin/env python3
"""Export datawise.dev from Hashnode's public pages.

Hashnode's GraphQL API needs a Pro plan since 2026-05-13, so this reads each post's
server-rendered page instead and decodes the Next.js (RSC) payload embedded in it. That
payload carries the original Markdown plus the metadata the API used to return.

Writes:
  src/content/posts/<slug>.md   frontmatter + original Markdown, images pointed at local copies
  public/images/<slug>/...      every image a post references, plus its cover
  src/data/*.json               site info, series, tags, redirects, heading ids, comments

Everything fetched is cached in .export-cache/, so re-runs don't hit Hashnode again.
Usage: python3 scripts/export_hashnode.py [slug ...]   (no slugs = every post in the sitemap)
"""
import concurrent.futures as cf
import hashlib
import html as htmllib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SITE = "https://datawise.dev"
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".export-cache"
POSTS_DIR = ROOT / "src/content/posts"
DATA_DIR = ROOT / "src/data"
IMG_DIR = ROOT / "public/images"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0 Safari/537.36")
EXT_BY_TYPE = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
               "image/webp": ".webp", "image/svg+xml": ".svg", "image/avif": ".avif"}


def fetch(url: str) -> tuple[bytes, str]:
    """GET with an on-disk cache. Returns (body, content_type)."""
    key = hashlib.sha1(url.encode()).hexdigest()
    body_path, meta_path = CACHE / "http" / key, CACHE / "http" / f"{key}.json"
    if body_path.exists():
        return body_path.read_bytes(), json.loads(meta_path.read_text())["type"]
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body, ctype = r.read(), r.headers.get("Content-Type", "").split(";")[0].strip()
            break
        except urllib.error.HTTPError as e:
            if e.code in (404, 403, 410):
                raise
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 ** attempt)
    else:
        raise RuntimeError(f"giving up on {url}")
    body_path.parent.mkdir(parents=True, exist_ok=True)
    body_path.write_bytes(body)
    meta_path.write_text(json.dumps({"url": url, "type": ctype}))
    return body, ctype


def rsc_rows(page: str) -> dict[str, str]:
    """Decode the self.__next_f.push(...) chunks into React Flight rows keyed by id.

    Text rows ("<id>:T<hex byte length>,<text>") can span lines, so parse by byte length.
    """
    dec = json.JSONDecoder()
    parts = []
    for m in re.finditer(r"self\.__next_f\.push\(", page):
        arr, _ = dec.raw_decode(page, m.end())
        if len(arr) > 1 and arr[0] == 1:
            parts.append(arr[1])
    data = "".join(parts).encode()
    rows, pos, head = {}, 0, re.compile(rb"([0-9a-f]*):")
    while pos < len(data):
        m = head.match(data, pos)
        if not m:
            nl = data.find(b"\n", pos)
            pos = len(data) if nl < 0 else nl + 1
            continue
        key, pos = m.group(1).decode(), m.end()
        if data[pos:pos + 1] == b"T":
            comma = data.index(b",", pos)
            n = int(data[pos + 1:comma], 16)
            rows[key] = data[comma + 1:comma + 1 + n].decode()
            pos = comma + 1 + n
        else:
            nl = data.find(b"\n", pos)
            end = len(data) if nl < 0 else nl
            rows[key] = data[pos:end].decode()
            pos = end + 1
    return rows


def find_object(rows: dict[str, str], marker: str, where=lambda v: True):
    """Return the first JSON value following `marker` in any row that satisfies `where`."""
    dec = json.JSONDecoder()
    for text in rows.values():
        i = text.find(marker)
        while i >= 0:
            try:
                value = dec.raw_decode(text, i + len(marker))[0]
                if where(value):
                    return value
            except json.JSONDecodeError:
                pass
            i = text.find(marker, i + 1)
    return None


def deref(rows, value):
    """Resolve a "$<id>" reference to the row it points at."""
    if isinstance(value, str) and re.fullmatch(r"\$[0-9a-f]+", value):
        return rows.get(value[1:])
    return value


def html_meta(page: str) -> dict:
    def meta(attr, name):
        m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', page)
        return htmllib.unescape(m.group(1)) if m else None
    title = re.search(r"<title>(.*?)</title>", page, re.S)
    canon = re.search(r'<link rel="canonical" href="([^"]*)"', page)
    return {
        "title": htmllib.unescape(title.group(1)) if title else None,
        "description": meta("name", "description"),
        "canonical": canon.group(1) if canon else None,
        "robots": meta("name", "robots"),
    }


def heading_ids(content_html: str) -> list[dict]:
    out = []
    for m in re.finditer(r'<h([1-6])\b[^>]*?\bid="([^"]+)"[^>]*>(.*?)</h\1>', content_html or "", re.S):
        text = htmllib.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()
        out.append({"depth": int(m.group(1)), "id": m.group(2), "text": text})
    return out


IMG_MD = re.compile(r'!\[(?P<alt>[^\]]*)\]\((?P<url>[^)\s]+)(?P<rest>[^)]*)\)')
IMG_HTML = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")')


def localise_images(slug: str, markdown: str, manifest: list, failures: list) -> str:
    """Download every image in the post and point the Markdown at /images/<slug>/<n>.<ext>."""
    local_by_url: dict[str, str] = {}

    def local_for(url: str) -> str | None:
        if url in local_by_url:
            return local_by_url[url]
        if not url.startswith("http"):
            return None
        try:
            body, ctype = fetch(url)
        except Exception as e:  # noqa: BLE001 - record and keep going
            failures.append({"slug": slug, "url": url, "error": str(e)})
            return None
        ext = EXT_BY_TYPE.get(ctype) or Path(url.split("?")[0]).suffix.lower() or ".bin"
        name = f"{len(local_by_url) + 1}{'.jpg' if ext == '.jpeg' else ext}"
        dest = IMG_DIR / slug / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        local_by_url[url] = f"/images/{slug}/{name}"
        return local_by_url[url]

    def md_sub(m):
        local = local_for(m.group("url"))
        if not local:
            # Unfetchable (e.g. expired LinkedIn CDN links, already broken on Hashnode).
            # Leave a marker so the original image can be put back by hand.
            return f"<!-- missing image, source no longer available: {m.group('url')} -->"
        start, end = m.start(), m.end()
        manifest.append({
            "slug": slug, "file": local, "source": m.group("url"), "alt": m.group("alt"),
            "before": markdown[max(0, start - 600):start], "after": markdown[end:end + 400],
        })
        # Hashnode appends ` align="center"` inside the parentheses; that isn't CommonMark.
        title = re.search(r'\s("[^"]*")\s*$', m.group("rest"))
        return f"![{m.group('alt')}]({local}{' ' + title.group(1) if title and 'align=' not in title.group(0) else ''})"

    def html_sub(m):
        local = local_for(m.group(2))
        if local:
            manifest.append({"slug": slug, "file": local, "source": m.group(2), "alt": "",
                             "before": "", "after": "", "html": True})
        return f"{m.group(1)}{local or m.group(2)}{m.group(3)}"

    markdown = IMG_MD.sub(md_sub, markdown)
    return IMG_HTML.sub(html_sub, markdown)


GIST_LANG = {"shell": "bash", "text": "", "jupyter notebook": None}


def inline_gists(markdown: str) -> str:
    """Replace Hashnode's %[gist-url] embeds with the gist's files as fenced code.

    A script-tag gist embed is invisible to crawlers; inline code is searchable.
    """
    def sub(m):
        url, gist_id = m.group(1), m.group(2)
        gist = json.loads(fetch(f"https://api.github.com/gists/{gist_id}")[0])
        blocks = []
        for name, f in gist["files"].items():
            lang = (f.get("language") or "").lower()
            lang = GIST_LANG.get(lang, lang)
            if lang is None or f.get("truncated"):
                return f"[View the code on GitHub Gist]({url})"
            blocks.append(f"```{lang}\n{f['content'].rstrip()}\n```")
        return "\n\n".join(blocks) + f"\n\n*[View on GitHub Gist]({url})*"
    return re.sub(r"%\[(https://gist\.github\.com/[\w-]+/([0-9a-f]+))\]", sub, markdown)


def strip_frontmatter(markdown: str) -> str:
    # Posts once published from GitHub kept their frontmatter inside the Markdown.
    return re.sub(r"\A\s*---\n.*?\n---\n", "", markdown, count=1, flags=re.S)


def fix_links(markdown: str, slug_by_cuid: dict, slug_by_id: dict, medium_ids: dict) -> str:
    # Old Hashnode permalinks -> local slugs.
    def hn(m):
        target = slug_by_cuid.get(m.group(1)) or slug_by_id.get(m.group(1))
        return f"/{target}" if target else m.group(0)
    markdown = re.sub(r"https?://hashnode\.com/post/([a-z0-9]+)", hn, markdown)
    # medium.com/p/<id> links to posts that moved here from Medium.
    markdown = re.sub(r"https?://medium\.com/p/([0-9a-f]{12})\b",
                      lambda m: medium_ids.get(m.group(1), m.group(0)), markdown)
    # Absolute links to our own posts -> root-relative, so previews work.
    markdown = re.sub(r"\]\(https?://(?:www\.)?datawise\.dev(/[^)\s]*)", r"](\1", markdown)
    # The apex notjustsql.com doesn't answer over HTTPS; always link to www.
    markdown = re.sub(r"https?://notjustsql\.com", "https://www.notjustsql.com", markdown)
    return markdown


def yaml_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in v) + "]"
    return json.dumps(v, ensure_ascii=False)


def frontmatter(fields: dict) -> str:
    lines = ["---"]
    for k, v in fields.items():
        if v is None or v == [] or v is False:
            continue
        if isinstance(v, dict):
            lines.append(f"{k}:")
            lines += [f"  {kk}: {yaml_value(vv)}" for kk, vv in v.items() if vv]
        elif k.startswith("date"):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_value(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def sitemap_paths() -> list[str]:
    index = fetch(f"{SITE}/sitemap.xml")[0].decode()
    urls = []
    for sub in re.findall(r"<loc>(.*?)</loc>", index):
        urls += re.findall(r"<loc>(.*?)</loc>", fetch(htmllib.unescape(sub))[0].decode())
    return [u.removeprefix(SITE).strip("/") for u in urls if u.rstrip("/") != SITE]


def main(argv):
    CACHE.mkdir(exist_ok=True)
    paths = sitemap_paths()
    slugs = argv or [p for p in paths if "/" not in p]
    sitemap_series = [p.removeprefix("series/") for p in paths if p.startswith("series/")]
    print(f"exporting {len(slugs)} posts")

    def load(slug):
        page = fetch(f"{SITE}/{slug}")[0].decode()
        rows = rsc_rows(page)
        post = find_object(rows, '"post":', lambda v: isinstance(v, dict) and v.get("slug") == slug
                           and isinstance(v.get("content"), dict))
        return slug, page, rows, post

    with cf.ThreadPoolExecutor(4) as pool:
        results = list(pool.map(load, slugs))
    loaded = [r for r in results if r[3]]
    not_posts = [r[0] for r in results if not r[3]]
    if not_posts:
        print(f"not posts (skipped): {not_posts}")

    slug_by_cuid = {p["cuid"]: p["slug"] for _, _, _, p in loaded}
    slug_by_id = {p["id"]: p["slug"] for _, _, _, p in loaded}
    publication = find_object(loaded[0][2], '"publication":', lambda v: isinstance(v, dict)
                              and "RedirectionRule" in json.dumps(v))
    rules = next((v for v in (publication or {}).values() if isinstance(v, list) and v
                  and isinstance(v[0], dict) and v[0].get("__typename") == "RedirectionRule"), [])
    # Medium-era slugs end in the 12-hex Medium post id.
    medium_ids = {m.group(1): r["destination"] for r in rules
                  if (m := re.search(r"-([0-9a-f]{12})$", r["source"]))}

    manifest, failures, headings, comments = [], [], {}, {}
    series, tags, report = {}, {}, []
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for slug, page, rows, post in loaded:
        meta = html_meta(page)
        content = post.get("content") or {}
        markdown = deref(rows, content.get("markdown")) or ""
        body = inline_gists(strip_frontmatter(markdown))
        body = localise_images(slug, fix_links(body, slug_by_cuid, slug_by_id, medium_ids),
                               manifest, failures)

        cover = (post.get("coverImage") or {})
        cover_local = None
        if cover.get("url"):
            try:
                cbody, ctype = fetch(cover["url"])
                ext = EXT_BY_TYPE.get(ctype, ".jpg")
                (IMG_DIR / slug).mkdir(parents=True, exist_ok=True)
                (IMG_DIR / slug / f"cover{ext}").write_bytes(cbody)
                cover_local = f"/images/{slug}/cover{ext}"
            except Exception as e:  # noqa: BLE001
                failures.append({"slug": slug, "url": cover["url"], "error": str(e), "cover": True})

        if post.get("series"):
            series.setdefault(post["series"]["slug"], {"name": post["series"]["name"]})
        for t in post.get("tags") or []:
            tags[t["slug"]] = t["name"]

        canonical = post.get("canonicalUrl") or None
        if canonical and canonical.rstrip("/") == f"{SITE}/{slug}":
            canonical = None
        prefs = post.get("preferences") or {}
        fm = {
            "title": post["title"],
            "subtitle": post.get("subtitle"),
            "seoTitle": meta["title"] if meta["title"] != post["title"] else None,
            "seoDescription": meta["description"],
            "datePublished": post["publishedAt"],
            "dateUpdated": post.get("updatedAt") if post.get("updatedAt") != post["publishedAt"] else None,
            "cover": cover_local,
            # Hashnode stored some profile links with a locale (unsplash.com/ja/@name).
            "coverCredit": {"name": cover.get("photographer"),
                            "url": re.sub(r"(unsplash\.com)/[a-z]{2}(?:-[A-Za-z]{2,4})?/@", r"\1/@",
                                          cover.get("attribution") or "")}
            if cover.get("photographer") and not cover.get("isAttributionHidden") else None,
            "series": (post.get("series") or {}).get("slug"),
            "tags": [t["slug"] for t in post.get("tags") or []],
            "canonical": canonical,
            "delisted": bool(prefs.get("isDelisted")),
            "hashnodeCuid": post.get("cuid"),
        }
        (POSTS_DIR / f"{slug}.md").write_text(frontmatter(fm) + body.strip() + "\n")

        hs = heading_ids(deref(rows, content.get("html")))
        if hs:
            headings[slug] = hs
        edges = find_object(rows, '"initialEdges":') or []
        if edges:
            comments[slug] = [e["node"] for e in edges]
        report.append({"slug": slug, "responses": post.get("responseCount", 0),
                       "comments_exported": len(edges), "live_canonical": meta["canonical"],
                       "robots": meta["robots"], "md_chars": len(markdown)})

    # Series descriptions live on the series pages.
    for s_slug in sitemap_series:
        series.setdefault(s_slug, {"name": None})
    for s_slug, s in series.items():
        s_rows = rsc_rows(fetch(f"{SITE}/series/{s_slug}")[0].decode())
        obj = find_object(s_rows, '"series":', lambda v: isinstance(v, dict)
                          and v.get("slug") == s_slug and "description" in v) or {}
        s["name"] = s["name"] or obj.get("name")
        s["description"] = (obj.get("description") or {}).get("markdown")

    redirects = [{"from": r["source"], "to": r["destination"], "status": r["type"]} for r in rules]

    def dump(name, obj):
        (DATA_DIR / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

    dump("series.json", series)
    dump("tags.json", dict(sorted(tags.items())))
    dump("redirects.json", redirects)
    dump("heading-ids.json", headings)
    dump("comments.json", comments)
    (CACHE / "publication.json").write_text(json.dumps(publication, indent=2, ensure_ascii=False))
    (CACHE / "images-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    (CACHE / "export-report.json").write_text(json.dumps(
        {"posts": report, "image_failures": failures, "not_posts": not_posts},
        indent=2, ensure_ascii=False))
    print(f"posts={len(loaded)} images={len(manifest)} image_failures={len(failures)} "
          f"series={len(series)} tags={len(tags)} redirects={len(redirects)} "
          f"posts_with_comments={len(comments)}")


if __name__ == "__main__":
    main(sys.argv[1:])
