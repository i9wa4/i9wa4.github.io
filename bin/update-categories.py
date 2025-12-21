#!/usr/bin/env python3
"""Extract categories from blog/zenn posts and update index.qmd."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import yaml


def parse_front_matter(content: str) -> dict:
    """Parse YAML front matter from markdown content."""
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def extract_categories(directories: list[Path]) -> Counter[str]:
    """Extract all categories from qmd files in directories."""
    categories: Counter[str] = Counter()

    for directory in directories:
        if not directory.exists():
            continue

        for qmd_file in directory.glob("*.qmd"):
            if qmd_file.name == "index.qmd":
                continue

            content = qmd_file.read_text(encoding="utf-8")
            front_matter = parse_front_matter(content)

            for category in front_matter.get("categories", []):
                categories[category] += 1

    return categories


def generate_category_buttons(categories: Counter[str]) -> str:
    """Generate category button markdown."""
    lines = ["::: {.category-buttons}"]
    lines.append("[All](.){.btn .btn-outline-secondary .btn-sm}")

    # Sort alphabetically
    sorted_categories = sorted(categories.items(), key=lambda x: x[0])

    for category, _count in sorted_categories:
        lines.append(
            f"[{category}](#category={category}){{.btn .btn-outline-primary .btn-sm}}"
        )

    lines.append(":::")
    return "\n".join(lines)


def update_index_qmd(index_path: Path, new_buttons: str) -> bool:
    """Update index.qmd with new category buttons. Returns True if modified."""
    content = index_path.read_text(encoding="utf-8")

    # Pattern to match the category-buttons div
    pattern = r"::: \{\.category-buttons\}.*?:::"
    replacement = new_buttons

    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # Insert before the listing div if category-buttons doesn't exist
        listing_pattern = r"(::: \{#list-all\})"
        new_content = re.sub(
            listing_pattern,
            f"{new_buttons}\n\n\\1",
            content,
        )

    if content != new_content:
        index_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main() -> int:
    """Main function."""
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent

    blog_dir = project_root / "blog"
    zenn_dir = project_root / "zenn"
    index_path = project_root / "index.qmd"

    if not index_path.exists():
        print(f"Error: {index_path} not found")
        return 1

    categories = extract_categories([blog_dir, zenn_dir])

    if not categories:
        print("No categories found")
        return 0

    new_buttons = generate_category_buttons(categories)
    modified = update_index_qmd(index_path, new_buttons)

    if modified:
        print(f"Updated {index_path}")
        print(f"Categories: {dict(categories)}")
    else:
        print("No changes needed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
