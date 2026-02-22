#!/usr/bin/env python3
"""Fetch trending tech articles from multiple sources via public APIs.

EN sources: Hacker News, dev.to, GitHub trending repos
JA sources: Zenn, Qiita, Hatena Bookmark

Outputs JSON to stdout with structured data for each source.
"""

from __future__ import annotations

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Any


def fetch_json(url: str, headers: dict[str, str] | None = None) -> Any:
    """Fetch JSON from URL."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "fetch-trends/1.0")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    """Fetch text content from URL."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "fetch-trends/1.0")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


# --- EN Sources ---


def fetch_hackernews(limit: int = 15) -> list[dict[str, Any]]:
    """Fetch top stories from Hacker News."""
    ids = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")
    top_ids = ids[:limit]

    items = []

    def _fetch_item(item_id: int) -> dict[str, Any] | None:
        try:
            data = fetch_json(
                f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            )
            if data and data.get("type") == "story" and data.get("url"):
                return {
                    "title": data.get("title", ""),
                    "url": data["url"],
                    "score": data.get("score", 0),
                    "comments": data.get("descendants", 0),
                    "source": "hackernews",
                }
        except Exception:
            pass
        return None

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(_fetch_item, i): i for i in top_ids}
        for future in as_completed(futures):
            result = future.result()
            if result:
                items.append(result)

    items.sort(key=lambda x: x["score"], reverse=True)
    return items


def fetch_devto(limit: int = 15) -> list[dict[str, Any]]:
    """Fetch top articles from dev.to (last 1 day)."""
    data = fetch_json(f"https://dev.to/api/articles?top=1&per_page={limit}")
    items = []
    for article in data:
        items.append(
            {
                "title": article["title"],
                "url": article["url"],
                "reactions": article.get("positive_reactions_count", 0),
                "tags": article.get("tag_list", []),
                "source": "devto",
            }
        )
    return items


def fetch_github_trending(limit: int = 10) -> list[dict[str, Any]]:
    """Fetch trending repos from GitHub Search API (created in last 7 days)."""
    week_ago = (datetime.now(tz=timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    url = (
        f"https://api.github.com/search/repositories"
        f"?q=created:>{week_ago}+stars:>50&sort=stars&order=desc&per_page={limit}"
    )
    data = fetch_json(url, headers={"Accept": "application/vnd.github+json"})
    items = []
    for repo in data.get("items", []):
        items.append(
            {
                "title": repo["full_name"],
                "url": repo["html_url"],
                "description": repo.get("description", ""),
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language", ""),
                "source": "github",
            }
        )
    return items


# --- JA Sources ---


def fetch_zenn(limit: int = 20) -> list[dict[str, Any]]:
    """Fetch trending articles from Zenn."""
    data = fetch_json(
        f"https://zenn.dev/api/articles?order=trending&count={limit}&article_type=tech"
    )
    items = []
    for article in data.get("articles", []):
        items.append(
            {
                "title": article["title"],
                "url": f"https://zenn.dev{article['path']}",
                "likes": article.get("liked_count", 0),
                "source": "zenn",
            }
        )
    return items


def fetch_qiita(limit: int = 20) -> list[dict[str, Any]]:
    """Fetch popular articles from Qiita (last 3 days, stocks > 5)."""
    days_ago = (datetime.now(tz=timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
    query = f"stocks:>5 created:>{days_ago}"
    url = f"https://qiita.com/api/v2/items?query={urllib.parse.quote(query)}&per_page={limit}"
    data = fetch_json(url)
    items = []
    for article in data:
        items.append(
            {
                "title": article["title"],
                "url": article["url"],
                "likes": article.get("likes_count", 0),
                "stocks": article.get("stocks_count", 0),
                "tags": [t["name"] for t in article.get("tags", [])],
                "source": "qiita",
            }
        )
    return items


def fetch_hatena(limit: int = 15) -> list[dict[str, Any]]:
    """Fetch tech hotentry from Hatena Bookmark via RSS."""
    rss_text = fetch_text("https://b.hatena.ne.jp/hotentry/it.rss")
    root = ET.fromstring(rss_text)

    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rss": "http://purl.org/rss/1.0/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "hatena": "http://www.hatena.ne.jp/info/xmlns#",
    }

    items = []
    for item in root.findall("rss:item", ns)[:limit]:
        title = item.find("rss:title", ns)
        link = item.find("rss:link", ns)
        bookmarks = item.find("hatena:bookmarkcount", ns)
        items.append(
            {
                "title": title.text if title is not None else "",
                "url": link.text if link is not None else "",
                "bookmarks": int(bookmarks.text) if bookmarks is not None else 0,
                "source": "hatena",
            }
        )
    return items


# --- Main ---


def fetch_source(name: str, func: Any) -> tuple[str, list[dict[str, Any]]]:
    """Fetch a single source with error handling."""
    try:
        return name, func()
    except Exception as e:
        print(f"Warning: {name} fetch failed: {e}", file=sys.stderr)
        return name, []


def main() -> int:
    """Fetch all sources and output JSON."""

    sources = {
        "en": [
            ("hackernews", fetch_hackernews),
            ("devto", fetch_devto),
            ("github", fetch_github_trending),
        ],
        "ja": [
            ("zenn", fetch_zenn),
            ("qiita", fetch_qiita),
            ("hatena", fetch_hatena),
        ],
    }

    result: dict[str, dict[str, list[dict[str, Any]]]] = {"en": {}, "ja": {}}

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {}
        for lang, source_list in sources.items():
            for name, func in source_list:
                future = pool.submit(fetch_source, name, func)
                futures[future] = (lang, name)

        for future in as_completed(futures):
            lang, name = futures[future]
            source_name, items = future.result()
            result[lang][source_name] = items

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
