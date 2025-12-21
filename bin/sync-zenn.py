#!/usr/bin/env python3
"""Sync Zenn articles from local repository to generate .qmd files."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import yaml


def parse_front_matter(content: str) -> tuple[dict, str]:
    """Parse YAML front matter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        front_matter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return front_matter or {}, body
    except yaml.YAMLError:
        return {}, content


def extract_description(body: str, max_length: int = 200) -> str:
    """Extract description from body content."""
    lines = []
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("```"):
            break
        lines.append(line)
        if len(" ".join(lines)) > max_length:
            break

    description = " ".join(lines)
    if len(description) > max_length:
        description = description[:max_length] + "..."
    return description


def build_zenn_url(slug: str, publication_name: str | None, username: str) -> str:
    """Build Zenn article URL."""
    if publication_name:
        return f"https://zenn.dev/{publication_name}/articles/{slug}"
    return f"https://zenn.dev/{username}/articles/{slug}"


def fetch_published_at_from_web(url: str) -> str | None:
    """Fetch publishedAt from Zenn article page.

    Args:
        url: Zenn article URL

    Returns:
        Published date string or None if failed
    """
    try:
        with urlopen(url, timeout=10) as response:
            html = response.read().decode("utf-8")

        # Extract publishedAt from JSON in HTML
        # Pattern: "publishedAt":"2025-03-28T16:27:58.214+09:00"
        match = re.search(r'"publishedAt"\s*:\s*"([^"]+)"', html)
        if match:
            return match.group(1)
    except (URLError, TimeoutError) as e:
        print(f"  Warning: Failed to fetch {url}: {e}")
    return None


def convert_date(published_at: str) -> str:
    """Convert Zenn date format to Quarto format.

    Handles formats:
    - "2024-11-20 18:00" (from local file)
    - "2025-03-28T16:27:58.214+09:00" (from web)
    """
    if not published_at:
        return ""

    date_str = str(published_at).strip()

    # Handle ISO 8601 format from web (e.g., "2025-03-28T16:27:58.214+09:00")
    if "T" in date_str:
        match = re.match(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", date_str)
        if match:
            date_part = match.group(1)
            time_part = match.group(2)
            return f"{date_part} {time_part} +0900"

    # Handle local format (e.g., "2024-11-20 18:00")
    if len(date_str) == 16:
        date_str += ":00"
    if "+" not in date_str and "-" not in date_str[-5:]:
        date_str += " +0900"
    return date_str


def generate_qmd_content(
    title: str,
    date: str,
    description: str,
    zenn_url: str,
) -> str:
    """Generate .qmd file content."""
    description_lines = description.split("\n")
    description_yaml = "\n  ".join(description_lines)

    return f'''---
title: "{title}"
author: uma-chan
date: {date}
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

[{title}]({zenn_url})
'''


def sync_articles(
    zenn_repo_path: Path,
    output_dir: Path,
    username: str,
) -> bool:
    """Sync Zenn articles to output directory."""
    articles_dir = zenn_repo_path / "articles"
    if not articles_dir.exists():
        print(f"Zenn articles directory not found: {articles_dir}")
        print("Skipping sync (this is expected in CI environment)")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)

    zenn_slugs: set[str] = set()
    changes_made = False

    md_files = sorted(articles_dir.glob("*.md"))
    total = len([f for f in md_files if f.name != ".keep"])
    current = 0

    for md_file in md_files:
        if md_file.name == ".keep":
            continue

        current += 1
        slug = md_file.stem
        zenn_slugs.add(slug)

        content = md_file.read_text(encoding="utf-8")
        front_matter, body = parse_front_matter(content)

        if not front_matter.get("published", False):
            print(f"[{current}/{total}] Skipping unpublished: {slug}")
            continue

        title = front_matter.get("title", slug)
        published_at = front_matter.get("published_at", "")
        publication_name = front_matter.get("publication_name")
        zenn_url = build_zenn_url(slug, publication_name, username)

        # Fetch published_at from web if not in local file
        if not published_at:
            print(f"[{current}/{total}] Fetching date from web: {slug}")
            web_published_at = fetch_published_at_from_web(zenn_url)
            if web_published_at:
                published_at = web_published_at

        date = convert_date(published_at)
        description = extract_description(body)

        qmd_content = generate_qmd_content(title, date, description, zenn_url)
        qmd_file = output_dir / f"{slug}.qmd"

        if qmd_file.exists():
            existing_content = qmd_file.read_text(encoding="utf-8")
            if existing_content == qmd_content:
                print(f"[{current}/{total}] No change: {slug}")
                continue

        qmd_file.write_text(qmd_content, encoding="utf-8")
        print(f"[{current}/{total}] Updated: {qmd_file.name}")
        changes_made = True

    # Delete qmd files that don't exist in Zenn repo
    for qmd_file in output_dir.glob("*.qmd"):
        slug = qmd_file.stem
        if slug not in zenn_slugs:
            qmd_file.unlink()
            print(f"Deleted: {qmd_file.name}")
            changes_made = True

    return changes_made


def main() -> int:
    """Main function."""
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    zenn_repo_path = project_root.parent / "zenn"
    output_dir = project_root / "zenn"
    username = "i9wa4"

    print(f"Syncing Zenn articles from: {zenn_repo_path}")
    print(f"Output directory: {output_dir}")
    print()

    changes_made = sync_articles(zenn_repo_path, output_dir, username)

    print()
    if changes_made:
        print("Changes detected, files updated")
        return 0
    print("No changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
