#!/usr/bin/env python3
"""Write image alt text into the posts.

Reads scripts/image-alt.json ({"/images/<slug>/<n>.<ext>": {"kind", "alt"}}) and sets the alt
of every matching Markdown image in src/content/posts/. Existing alt text is replaced only
when it's empty or Hashnode/LinkedIn boilerplate, unless --force.

  python3 scripts/apply_alt_text.py            # apply
  python3 scripts/apply_alt_text.py --check    # after `npm run build`: rendered alt == intended
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALT_FILE = ROOT / "scripts/image-alt.json"
POSTS = ROOT / "src/content/posts"
IMG = re.compile(r"!\[(?P<alt>(?:\\.|[^\]\\])*)\]\((?P<src>/images/[^)\s]+)(?P<rest>[^)]*)\)")
BOILERPLATE = {"", "no alt text provided for this image", "image"}


def md_escape(text: str) -> str:
    # Image descriptions are parsed as inline Markdown; escape anything that could turn
    # into emphasis, strikethrough, code, links or HTML so the alt keeps the literal text.
    return re.sub(r"([\\`*_~\[\]<>&])", r"\\\1", " ".join(text.split()))


def apply(force: bool) -> None:
    alts = json.loads(ALT_FILE.read_text())
    used, changed_posts = set(), 0
    for post in sorted(POSTS.glob("*.md")):
        text = post.read_text()

        def sub(m):
            entry = alts.get(m.group("src"))
            if not entry:
                return m.group(0)
            used.add(m.group("src"))
            current = m.group("alt").strip()
            if current.lower() not in BOILERPLATE and not force and current != md_escape(entry["alt"]):
                print(f"  keeping existing alt in {post.name}: {current[:80]}")
                return m.group(0)
            return f"![{md_escape(entry['alt'])}]({m.group('src')}{m.group('rest')})"

        new = IMG.sub(sub, text)
        if new != text:
            post.write_text(new)
            changed_posts += 1
    unused = sorted(set(alts) - used)
    print(f"alt text for {len(used)} images in {changed_posts} posts; {len(unused)} entries unused")
    for u in unused:
        print("  unused:", u)


class ImgCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs: list[dict] = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.imgs.append(dict(attrs))


def check() -> int:
    alts = json.loads(ALT_FILE.read_text())
    problems, seen = 0, set()
    for page in sorted((ROOT / "dist").glob("*.html")):
        parser = ImgCollector()
        parser.feed(page.read_text())
        for img in parser.imgs:
            src = img.get("src")
            if src not in alts:
                continue
            seen.add(src)
            wanted = " ".join(alts[src]["alt"].split())
            if (img.get("alt") or "") != wanted:
                problems += 1
                print(f"{page.name} {src}\n  wanted:   {wanted}\n  rendered: {img.get('alt')}")
    missing = set(alts) - seen
    print(f"{len(seen)} images checked, {problems} mismatch(es), {len(missing)} not found in dist")
    return 1 if problems or missing else 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    apply(force="--force" in sys.argv)
