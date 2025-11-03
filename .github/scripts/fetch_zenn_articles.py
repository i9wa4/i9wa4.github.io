#!/usr/bin/env python3
"""Fetch Zenn articles from RSS feed and generate .qmd files."""

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen


def fetch_zenn_rss(username: str) -> list[dict]:
    """Fetch articles from Zenn RSS feed.

    Args:
        username: Zenn username

    Returns:
        List of article dictionaries
    """
    url = f"https://zenn.dev/{username}/feed"
    with urlopen(url) as response:
        xml_content = response.read()

    root = ET.fromstring(xml_content)
    articles = []

    # Find channel element first
    channel = root.find("channel")
    if channel is None:
        return articles

    for item in channel.findall("item"):
        title_elem = item.find("title")
        link_elem = item.find("link")
        pub_date_elem = item.find("pubDate")
        description_elem = item.find("description")

        if title_elem is None or link_elem is None or pub_date_elem is None:
            continue

        # Extract text from CDATA sections
        title = title_elem.text or ""
        link = link_elem.text or ""
        pub_date_str = pub_date_elem.text or ""
        description = description_elem.text if description_elem is not None else ""

        # Parse date (RFC 822 format)
        # Example: "Wed, 06 Aug 2025 11:02:00 GMT"
        try:
            # Parse as GMT and convert to JST (+0900)
            pub_date_utc = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
            # Add JST timezone info (UTC+9)
            pub_date = pub_date_utc.replace(tzinfo=timezone.utc).astimezone(
                timezone(timedelta(hours=9))
            )
        except ValueError:
            try:
                # Try with timezone offset format
                pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                continue

        articles.append(
            {
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "description": description,
            }
        )

    return articles


def generate_qmd_files(articles: list[dict], output_dir: Path) -> None:
    """Generate .qmd files for Zenn articles.

    Args:
        articles: List of article dictionaries
        output_dir: Output directory path
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for article in articles:
        # Extract slug from URL (last part)
        slug = article["link"].rstrip("/").split("/")[-1]
        filename = f"zenn-autogen-{slug}.qmd"
        filepath = output_dir / filename

        # Skip if file already exists
        if filepath.exists():
            continue

        # Skip if a manual file (not starting with zenn-autogen-) with the same slug already exists
        existing_files = [
            f for f in output_dir.glob(f"*{slug}.qmd")
            if not f.name.startswith("zenn-autogen-")
        ]
        if existing_files:
            print(f"Skipped: {filename} (conflicts with {existing_files[0].name})")
            continue

        # Format date for YAML frontmatter
        date_yaml = article["pub_date"].strftime("%Y-%m-%d %H:%M:%S %z")

        # Clean description (remove HTML tags if any, and fix multiline for YAML)
        description = article["description"].strip()
        # Indent each line of description for YAML block scalar
        description_lines = description.split("\n")
        description_yaml = "\n  ".join(description_lines)

        # Generate .qmd content
        content = f"""---
title: "{article['title']}"
author: uma-chan
date: {date_yaml}
date-modified: last-modified
image: "/assets/common/zenn-logo-only.svg"
description: |
  {description_yaml}
categories:
  - "blog"
  - "tech"
  - "zenn"
---

## Zenn リンク先

この記事は Zenn で公開されています。

[{article['title']}]({article['link']})
"""

        filepath.write_text(content, encoding="utf-8")
        print(f"Created: {filename}")


def main() -> None:
    """Main function."""
    username = "i9wa4"
    output_dir = Path("blog")

    print(f"Fetching articles from Zenn (@{username})...")
    articles = fetch_zenn_rss(username)
    print(f"Found {len(articles)} articles")

    print("Generating .qmd files...")
    generate_qmd_files(articles, output_dir)
    print("Done!")


if __name__ == "__main__":
    main()
