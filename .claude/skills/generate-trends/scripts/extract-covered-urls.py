"""Extract URLs already covered in recent trend articles.

Scans auto/*.qmd files from the last N days and collects all URLs
found in markdown list items. Outputs a JSON skip-list to stdout.

Usage:
    uv run python .claude/skills/generate-trends/scripts/extract-covered-urls.py > /tmp/covered-urls.json

Output format:
    {
      "urls": ["https://...", ...],
      "days": 7,
      "articles_scanned": 14,
      "generated_at": "YYYY-MM-DD"
    }
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

# Match markdown URLs inside list items: **[Title](https://...)** or [Title](https://...)
URL_PATTERN = re.compile(r"\]\((https?://[^)]+)\)")

# How many days back to scan (exclusive of today)
LOOKBACK_DAYS = 7


def article_date(path: Path) -> date | None:
    """Parse YYYY-MM-DD from filename like 2026-02-28-en-tech-trends.qmd."""
    parts = path.stem.split("-")
    if len(parts) < 3:
        return None
    try:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return None


def extract_urls(auto_dir: Path, since: date) -> tuple[list[str], int]:
    """Collect URLs from articles dated on or after `since`."""
    seen: set[str] = set()
    articles_scanned = 0

    for qmd_file in sorted(auto_dir.glob("*.qmd")):
        if qmd_file.name == "index.qmd":
            continue
        art_date = article_date(qmd_file)
        if art_date is None or art_date < since:
            continue

        articles_scanned += 1
        for line in qmd_file.read_text(encoding="utf-8").splitlines():
            if not line.startswith("- "):
                continue
            for url in URL_PATTERN.findall(line):
                seen.add(url)

    return sorted(seen), articles_scanned


def main() -> int:
    project_root = Path.cwd()
    auto_dir = project_root / "auto"

    if not auto_dir.exists():
        print(f"Error: {auto_dir} not found", file=sys.stderr)
        return 1

    today = date.today()
    since = today - timedelta(days=LOOKBACK_DAYS)

    urls, articles_scanned = extract_urls(auto_dir, since)

    result = {
        "urls": urls,
        "days": LOOKBACK_DAYS,
        "articles_scanned": articles_scanned,
        "generated_at": today.isoformat(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
