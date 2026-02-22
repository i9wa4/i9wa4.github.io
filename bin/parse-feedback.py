#!/usr/bin/env python3
"""Parse [x] feedback from auto-generated trend articles and update preferences.

Scans all auto/*.qmd files for checked checkbox items (- [x]) and extracts
topic tags from square brackets at the end of each line. Recomputes topic
counts from scratch on every run (idempotent).

Format expected in articles:
    - [x] **Title** - Description [tag1, tag2]
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Match checked items with tags at end: - [x] ... [tag1, tag2]
CHECKED_PATTERN = re.compile(r"^- \[x\] .+\[([^\]]+)\]\s*$")


def extract_checked_topics(auto_dir: Path) -> Counter[str]:
    """Extract topic tags from all checked items in auto/*.qmd files."""
    topics: Counter[str] = Counter()

    for qmd_file in sorted(auto_dir.glob("*.qmd")):
        if qmd_file.name == "index.qmd":
            continue

        for line in qmd_file.read_text(encoding="utf-8").splitlines():
            match = CHECKED_PATTERN.match(line)
            if match:
                raw_tags = match.group(1)
                for tag in raw_tags.split(","):
                    tag = tag.strip().lower()
                    if tag:
                        topics[tag] += 1

    return topics


def write_preferences(prefs_path: Path, topics: Counter[str]) -> None:
    """Write preferences YAML file."""
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    data = {
        "topics": dict(sorted(topics.items())),
        "last_updated": now,
    }

    lines = [
        "# Auto-generated tech trend preferences",
        "# Updated by bin/parse-feedback.py from [x] checkboxes in articles",
    ]
    lines.append(yaml.dump(data, default_flow_style=False, allow_unicode=True).rstrip())
    prefs_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Main function."""
    project_root = Path(__file__).parent.resolve().parent
    auto_dir = project_root / "auto"
    prefs_path = auto_dir / ".preferences.yaml"

    if not auto_dir.exists():
        print(f"Error: {auto_dir} not found")
        return 1

    topics = extract_checked_topics(auto_dir)

    if not topics:
        print("No checked items found")
        return 0

    write_preferences(prefs_path, topics)
    print(f"Updated {prefs_path}")
    print(f"  Topics: {dict(topics.most_common(10))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
