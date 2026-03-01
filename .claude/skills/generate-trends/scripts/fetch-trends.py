"""Fetch trending tech articles from multiple sources via public APIs.

EN sources: Hacker News, dev.to, GitHub trending repos
JA sources: Zenn, Qiita, Hatena Bookmark
Data platform sources (EN+JA): Snowflake, BigQuery, Databricks, dbt

Outputs JSON to stdout with structured data for each source.
"""

from __future__ import annotations

import glob
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Any

DATA_PLATFORM_KEYWORDS = ["dbt", "snowflake", "bigquery", "databricks"]

# Canonical tag names per platform per service
_ZENN_TAGS = {
    "dbt": "dbt",
    "snowflake": "snowflake",
    "bigquery": "bigquery",
    "databricks": "databricks",
}
_QIITA_TAGS = {
    "dbt": "dbt",
    "snowflake": "Snowflake",
    "bigquery": "BigQuery",
    "databricks": "Databricks",
}


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


def fetch_devto(since_date: str, limit: int = 15) -> list[dict[str, Any]]:
    """Fetch top articles from dev.to since last generation."""
    since = datetime.strptime(since_date, "%Y-%m-%d").date()
    days = max(1, (datetime.now(tz=timezone.utc).date() - since).days + 1)
    data = fetch_json(f"https://dev.to/api/articles?top={days}&per_page={limit}")
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


def fetch_github_trending(since_date: str, limit: int = 10) -> list[dict[str, Any]]:
    """Fetch trending repos from GitHub Search API since last generation."""
    url = (
        f"https://api.github.com/search/repositories"
        f"?q=created:>{since_date}+stars:>50&sort=stars&order=desc&per_page={limit}"
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


def fetch_qiita(since_date: str, limit: int = 20) -> list[dict[str, Any]]:
    """Fetch popular articles from Qiita since last generation."""
    query = f"stocks:>5 created:>{since_date}"
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


# --- Data Platform Sources ---


def get_since_date(fallback_days: int = 7) -> str:
    """Return the date of the last generated trend article as YYYY-MM-DD.

    Scans auto/ directory for the most recent *-en-tech-trends.qmd file.
    Falls back to fallback_days ago if no files are found.
    """
    files = glob.glob("auto/*-en-tech-trends.qmd")
    dates = [m.group(1) for f in files if (m := re.search(r"(\d{4}-\d{2}-\d{2})", f))]
    if dates:
        return max(dates)
    return (datetime.now(tz=timezone.utc) - timedelta(days=fallback_days)).strftime(
        "%Y-%m-%d"
    )


def _pop(item: dict[str, Any]) -> int:
    """Extract a comparable popularity score from any item regardless of source."""
    return item.get(
        "score", item.get("reactions", item.get("stars", item.get("likes", 0)))
    )


def fetch_hn_dataplatform(
    since_date: str, per_keyword: int = 50
) -> list[dict[str, Any]]:
    """Fetch HN stories about data platform tools via Algolia search API."""
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    since_ts = int(
        datetime.strptime(since_date, "%Y-%m-%d")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    for keyword in DATA_PLATFORM_KEYWORDS:
        url = (
            f"https://hn.algolia.com/api/v1/search"
            f"?query={urllib.parse.quote(keyword)}&tags=story"
            f"&hitsPerPage={per_keyword}"
            f"&numericFilters=created_at_i%3E{since_ts}"
        )
        try:
            data = fetch_json(url)
            for hit in data.get("hits", []):
                article_url = hit.get("url") or ""
                if not article_url or article_url in seen:
                    continue
                seen.add(article_url)
                items.append(
                    {
                        "title": hit.get("title", ""),
                        "url": article_url,
                        "score": hit.get("points", 0),
                        "platform": keyword,
                        "source": "hackernews",
                    }
                )
        except Exception:
            pass

    items.sort(key=_pop, reverse=True)
    return items


def fetch_devto_dataplatform(
    since_date: str, per_keyword: int = 50
) -> list[dict[str, Any]]:
    """Fetch dev.to articles tagged with data platform tools since last generation."""
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    since = datetime.strptime(since_date, "%Y-%m-%d").date()
    days = max(1, (datetime.now(tz=timezone.utc).date() - since).days + 1)

    for keyword in DATA_PLATFORM_KEYWORDS:
        try:
            data = fetch_json(
                f"https://dev.to/api/articles?tag={keyword}&per_page={per_keyword}&top={days}"
            )
            for article in data:
                url = article["url"]
                if url in seen:
                    continue
                seen.add(url)
                items.append(
                    {
                        "title": article["title"],
                        "url": url,
                        "reactions": article.get("positive_reactions_count", 0),
                        "tags": article.get("tag_list", []),
                        "platform": keyword,
                        "source": "devto",
                    }
                )
        except Exception:
            pass

    items.sort(key=_pop, reverse=True)
    return items


def fetch_github_dataplatform(
    since_date: str, per_keyword: int = 50
) -> list[dict[str, Any]]:
    """Fetch GitHub repos related to data platform tools pushed since last generation."""
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    month_ago = since_date

    for keyword in DATA_PLATFORM_KEYWORDS:
        url = (
            f"https://api.github.com/search/repositories"
            f"?q=topic:{keyword}+pushed:>{month_ago}+stars:>50"
            f"&sort=stars&order=desc&per_page={per_keyword}"
        )
        try:
            data = fetch_json(url, headers={"Accept": "application/vnd.github+json"})
            for repo in data.get("items", []):
                repo_url = repo["html_url"]
                if repo_url in seen:
                    continue
                seen.add(repo_url)
                items.append(
                    {
                        "title": repo["full_name"],
                        "url": repo_url,
                        "description": repo.get("description", ""),
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language", ""),
                        "platform": keyword,
                        "source": "github",
                    }
                )
        except Exception:
            pass

    items.sort(key=_pop, reverse=True)
    return items


def fetch_medium_dataplatform(
    since_date: str, per_keyword: int = 50
) -> list[dict[str, Any]]:
    """Fetch Medium articles tagged with data platform tools via RSS, since last generation."""
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    since_dt = datetime.strptime(since_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    for keyword in DATA_PLATFORM_KEYWORDS:
        try:
            rss_text = fetch_text(f"https://medium.com/feed/tag/{keyword}")
            root = ET.fromstring(rss_text)
            channel = root.find("channel")
            if channel is None:
                continue
            count = 0
            for item in channel.findall("item"):
                link_el = item.find("link")
                title_el = item.find("title")
                pub_el = item.find("pubDate")
                if link_el is None or title_el is None:
                    continue
                article_url = (link_el.text or "").strip()
                if not article_url or article_url in seen:
                    continue
                if pub_el is not None and pub_el.text:
                    try:
                        from email.utils import parsedate_to_datetime

                        pub_dt = parsedate_to_datetime(pub_el.text)
                        if pub_dt.tzinfo is None:
                            pub_dt = pub_dt.replace(tzinfo=timezone.utc)
                        if pub_dt < since_dt:
                            continue
                    except Exception:
                        pass
                seen.add(article_url)
                items.append(
                    {
                        "title": (title_el.text or "").strip(),
                        "url": article_url,
                        "platform": keyword,
                        "source": "medium",
                    }
                )
                count += 1
                if count >= per_keyword:
                    break
        except Exception:
            pass

    items.sort(key=_pop, reverse=True)
    return items


def fetch_zenn_dataplatform(per_keyword: int = 50) -> list[dict[str, Any]]:
    """Fetch Zenn trending articles tagged with data platform tools."""
    seen: set[str] = set()
    items: list[dict[str, Any]] = []

    for keyword, tag in _ZENN_TAGS.items():
        try:
            data = fetch_json(
                f"https://zenn.dev/api/articles"
                f"?order=trending&count={per_keyword}&article_type=tech&tag_name={tag}"
            )
            for article in data.get("articles", []):
                url = f"https://zenn.dev{article['path']}"
                if url in seen:
                    continue
                seen.add(url)
                items.append(
                    {
                        "title": article["title"],
                        "url": url,
                        "likes": article.get("liked_count", 0),
                        "platform": keyword,
                        "source": "zenn",
                    }
                )
        except Exception:
            pass

    items.sort(key=_pop, reverse=True)
    return items


def fetch_qiita_dataplatform(
    since_date: str, per_keyword: int = 100
) -> list[dict[str, Any]]:
    """Fetch Qiita articles tagged with data platform tools since last generation."""
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    month_ago = since_date

    for keyword, tag in _QIITA_TAGS.items():
        query = f"tag:{tag} created:>{month_ago}"
        url = f"https://qiita.com/api/v2/items?query={urllib.parse.quote(query)}&per_page={per_keyword}"
        try:
            data = fetch_json(url)
            for article in data:
                article_url = article["url"]
                if article_url in seen:
                    continue
                seen.add(article_url)
                items.append(
                    {
                        "title": article["title"],
                        "url": article_url,
                        "likes": article.get("likes_count", 0),
                        "stocks": article.get("stocks_count", 0),
                        "tags": [t["name"] for t in article.get("tags", [])],
                        "platform": keyword,
                        "source": "qiita",
                    }
                )
        except Exception:
            pass

    items.sort(key=_pop, reverse=True)
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
    since_date = get_since_date()

    def _fetch_en_dataplatform() -> list[dict[str, Any]]:
        seen: set[str] = set()
        items: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=4) as p:
            futs = [
                p.submit(fetch_hn_dataplatform, since_date),
                p.submit(fetch_devto_dataplatform, since_date),
                p.submit(fetch_github_dataplatform, since_date),
                p.submit(fetch_medium_dataplatform, since_date),
            ]
            for f in as_completed(futs):
                try:
                    for item in f.result():
                        if item["url"] not in seen:
                            seen.add(item["url"])
                            items.append(item)
                except Exception:
                    pass
        items.sort(key=_pop, reverse=True)
        return items

    def _fetch_ja_dataplatform() -> list[dict[str, Any]]:
        seen: set[str] = set()
        items: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=2) as p:
            futs = [
                p.submit(fetch_zenn_dataplatform),
                p.submit(fetch_qiita_dataplatform, since_date),
            ]
            for f in as_completed(futs):
                try:
                    for item in f.result():
                        if item["url"] not in seen:
                            seen.add(item["url"])
                            items.append(item)
                except Exception:
                    pass
        items.sort(key=_pop, reverse=True)
        return items

    sources = {
        "en": [
            ("hackernews", fetch_hackernews),
            ("devto", lambda: fetch_devto(since_date)),
            ("github", lambda: fetch_github_trending(since_date)),
            ("dataplatform", _fetch_en_dataplatform),
        ],
        "ja": [
            ("zenn", fetch_zenn),
            ("qiita", lambda: fetch_qiita(since_date)),
            ("hatena", fetch_hatena),
            ("dataplatform", _fetch_ja_dataplatform),
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
