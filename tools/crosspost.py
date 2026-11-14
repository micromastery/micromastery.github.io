"""Cross-post blog posts to dev.to, with the blog as the canonical (original) source.

Converts Jekyll/Chirpy-specific markdown into plain markdown dev.to understands,
then creates one article per post. Posts already on dev.to (matched by canonical
URL) are skipped, or updated with --update. Nothing is sent with --dry-run.

Front matter controls (all optional):
  crosspost: false        never cross-post this post
  devto_tags: [a, b]      tags to use instead of the first 4 post tags
  ai_disclosure: no_ai    no_ai | some_ai | fully_autonomous (default: --ai-default)

Usage:
  python tools/crosspost.py --since 2026-01-01 --dry-run --out .crosspost-preview
  DEVTO_API_KEY=... python tools/crosspost.py --since 2026-01-01 --publish
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"
SITE_URL = "https://blog.mavsankar.com"
SITE_NAME = "Sankar's Blog"
SERIES_CATEGORY = "Homelab Series"
API = "https://dev.to/api"
AI_LEVELS = {"no_ai", "some_ai", "fully_autonomous"}
HEADERS = {
    "Accept": "application/vnd.forem.api-v1+json",
    "Content-Type": "application/json",
    # dev.to's CDN rejects requests without a User-Agent.
    "User-Agent": "blog.mavsankar.com-crosspost/1.0",
}
POST_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.(md|markdown)$")


def parse_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        raise ValueError(f"{path.name}: no front matter")
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def absolute(url: str) -> str:
    return SITE_URL + url if url.startswith("/") and not url.startswith("//") else url


def html_img_to_markdown(match: re.Match) -> str:
    tag = match.group(0)
    src = re.search(r'\ssrc="([^"]+)"', tag)
    alt = re.search(r'\salt="([^"]*)"', tag)
    if not src:
        return ""
    return f"![{alt.group(1) if alt else ''}]({absolute(src.group(1))})"


def wrap_liquid_code_blocks(body: str) -> str:
    """dev.to runs Liquid over the body; `{{ }}`/`{% %}` inside code must sit in {% raw %}."""
    out: list[str] = []
    block: list[str] = []
    fence = ""
    for line in body.split("\n"):
        stripped = line.strip()
        if not fence:
            opening = re.match(r"(`{3,}|~{3,})", stripped)
            if opening:
                fence, block = opening.group(1), [line]
            else:
                out.append(line)
            continue
        block.append(line)
        if stripped.startswith(fence) and stripped.strip(fence[0]) == "":
            chunk = "\n".join(block)
            if "{{" in chunk or "{%" in chunk:
                chunk = "{% raw %}\n" + chunk + "\n{% endraw %}"
            out.append(chunk)
            fence, block = "", []
    out.extend(block)
    return "\n".join(out)


def convert_body(body: str, canonical: str, in_series: bool) -> str:
    body = re.sub(r"<script\b.*?</script>\s*", "", body, flags=re.S | re.I)
    # Kramdown attribute lists such as `{: .prompt-tip }` (Jekyll-only styling).
    body = re.sub(r"^\{:[^}\n]*\}[ \t]*\n?", "", body, flags=re.M)
    body = re.sub(r"[ \t]*\{:[^}\n]*\}[ \t]*$", "", body, flags=re.M)
    body = re.sub(r"<img\b[^>]*>", html_img_to_markdown, body, flags=re.I)
    # Layout-only HTML wrappers and inline status text (e.g. "Loading live screenshot...").
    body = re.sub(r"^[ \t]*<p\b[^>]*style=[^>]*>.*?</p>[ \t]*\n?", "", body, flags=re.M | re.I)
    body = re.sub(r"^[ \t]*</?(p|div|center)\b[^>]*>[ \t]*\n?", "", body, flags=re.M | re.I)
    # Image captions left behind by the removed wrappers: plain markdown instead of <br>/<em>.
    body = re.sub(r"^[ \t]*<br\s*/?>[ \t]*\n?", "", body, flags=re.M | re.I)
    body = re.sub(r"<em>(.*?)</em>", r"*\1*", body, flags=re.S | re.I)
    body = re.sub(r"^[ \t]+(!\[)", r"\1", body, flags=re.M)
    body = re.sub(r"^[ \t]+(\*[^*\n]+\*)[ \t]*$", r"\1", body, flags=re.M)
    body = re.sub(r"\]\((/[^)\s]*)", lambda m: "](" + absolute(m.group(1)), body)
    body = re.sub(r'\b(src|href)="(/[^"]*)"', lambda m: f'{m.group(1)}="{absolute(m.group(2))}"', body)
    body = wrap_liquid_code_blocks(body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    if body.startswith("---"):
        body = "\u200b\n\n" + body  # a leading --- would be read as dev.to front matter

    footer = f"*Originally published on [{SITE_NAME}]({canonical})"
    if in_series:
        footer += f" as part of the [{SERIES_CATEGORY}]({SITE_URL}/categories/{SERIES_CATEGORY.lower().replace(' ', '-')}/)"
    return body + "\n\n---\n\n" + footer + ".*\n"


def devto_tags(meta: dict) -> list[str]:
    raw = meta.get("devto_tags") or meta.get("tags") or []
    tags: list[str] = []
    for tag in raw:
        clean = re.sub(r"[^a-z0-9]", "", str(tag).lower())
        if clean and clean not in tags:
            tags.append(clean)
    return tags[:4]


def cover_image(meta: dict) -> str | None:
    image = meta.get("image")
    path = image.get("path") if isinstance(image, dict) else image
    if not path:
        return None
    banners_file = ROOT / "_data" / "banner_images.json"
    if banners_file.exists():
        optimized = json.loads(banners_file.read_text(encoding="utf-8")).get(Path(path).stem)
        if optimized:
            path = optimized["path"]
    return absolute(path)


def build_article(path: Path, published: bool, ai_default: str) -> dict | None:
    match = POST_FILE.match(path.name)
    meta, body = parse_post(path)
    if meta.get("crosspost") is False or meta.get("hidden") or meta.get("published") is False:
        return None
    canonical = f"{SITE_URL}/posts/{match.group(2)}/"
    in_series = SERIES_CATEGORY in (meta.get("categories") or [])
    ai_level = meta.get("ai_disclosure", ai_default)
    if ai_level not in AI_LEVELS:
        raise ValueError(f"{path.name}: ai_disclosure must be one of {sorted(AI_LEVELS)}")
    article = {
        "title": str(meta["title"])[:128],
        "body_markdown": convert_body(body, canonical, in_series),
        "published": published,
        "canonical_url": canonical,
        "description": meta.get("description", ""),
        "tags": devto_tags(meta),
        "ai_disclosure_level": ai_level,
    }
    if cover := cover_image(meta):
        article["main_image"] = cover
    if in_series:
        article["series"] = SERIES_CATEGORY
    return article


def request(method: str, url: str, api_key: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={**HEADERS, "api-key": api_key})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read() or b"null")
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < 3:
                time.sleep(int(error.headers.get("Retry-After", "30")))
                continue
            raise RuntimeError(f"{method} {url} -> {error.code}: {error.read().decode(errors='replace')[:500]}") from None
    raise RuntimeError(f"{method} {url} failed after retries")


def existing_articles(api_key: str) -> dict[str, dict]:
    found, page = {}, 1
    while True:
        batch = request("GET", f"{API}/articles/me/all?per_page=1000&page={page}", api_key)
        for article in batch:
            if article.get("canonical_url"):
                found[article["canonical_url"].rstrip("/") + "/"] = article
        if len(batch) < 1000:
            return found
        page += 1


def select_posts(since: str | None, names: list[str]) -> list[Path]:
    posts = sorted(p for p in POSTS_DIR.iterdir() if POST_FILE.match(p.name))
    if names:
        wanted = {Path(n).name for n in names}
        missing = wanted - {p.name for p in posts}
        if missing:
            sys.exit(f"Unknown post file(s): {', '.join(sorted(missing))}")
        return [p for p in posts if p.name in wanted]
    if since:
        return [p for p in posts if POST_FILE.match(p.name).group(1) >= since]
    sys.exit("Pass --since YYYY-MM-DD or --posts FILE ...")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", help="cross-post posts dated on or after YYYY-MM-DD")
    parser.add_argument("--posts", nargs="*", default=[], help="specific _posts file names")
    parser.add_argument("--publish", action="store_true", help="publish immediately (default: create drafts)")
    parser.add_argument("--update", action="store_true", help="update posts that are already on dev.to")
    parser.add_argument("--ai-default", default="some_ai", choices=sorted(AI_LEVELS))
    parser.add_argument("--dry-run", action="store_true", help="convert only; send nothing")
    parser.add_argument("--out", help="with --dry-run, write converted markdown here")
    args = parser.parse_args()

    if args.since:
        date.fromisoformat(args.since)
    articles = []
    for path in select_posts(args.since, args.posts):
        article = build_article(path, args.publish, args.ai_default)
        if article is None:
            print(f"skip   {path.name} (crosspost: false / hidden)")
            continue
        articles.append((path, article))

    if args.dry_run:
        out = Path(args.out) if args.out else None
        if out:
            out.mkdir(parents=True, exist_ok=True)
        for path, article in articles:
            print(f"would  {path.name}\n       tags={article['tags']} series={article.get('series')} "
                  f"ai={article['ai_disclosure_level']}\n       canonical={article['canonical_url']}")
            if out:
                body = article.pop("body_markdown")
                (out / path.name).write_text(body, encoding="utf-8")
                (out / f"{path.stem}.json").write_text(json.dumps(article, indent=2), encoding="utf-8")
        return 0

    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        sys.exit("DEVTO_API_KEY is not set")

    try:
        existing = existing_articles(api_key)
    except RuntimeError as error:
        sys.exit(f"Could not list your dev.to articles (check DEVTO_API_KEY): {error}")
    failures = 0
    for index, (path, article) in enumerate(articles):
        current = existing.get(article["canonical_url"])
        try:
            if current and not args.update:
                print(f"exists {path.name} -> {current.get('url')}")
                continue
            if index:
                time.sleep(4)  # dev.to allows about 10 article writes per 30 seconds
            if current:
                if current.get("published") and not args.publish:
                    article["published"] = True  # never unpublish an article by updating it
                result = request("PUT", f"{API}/articles/{current['id']}", api_key, {"article": article})
                print(f"update {path.name} -> {result.get('url')}")
            else:
                result = request("POST", f"{API}/articles", api_key, {"article": article})
                state = "published" if article["published"] else "draft"
                print(f"create {path.name} ({state}) -> {result.get('url')}")
        except RuntimeError as error:
            failures += 1
            print(f"FAILED {path.name}: {error}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
