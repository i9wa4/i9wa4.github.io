#!/usr/bin/env python3
"""Fix image paths and links in GFM (GitHub Flavored Markdown) files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

BASE_URL = "https://i9wa4.github.io"

REPLACEMENTS = [
    # Relative image paths: (../assets/ -> absolute
    (r"\(\.\./assets/", f"({BASE_URL}/assets/"),
    (r'src="\.\./assets/', f'src="{BASE_URL}/assets/'),
    # Absolute image paths: (/assets/ -> absolute URL
    (r"\]\(/assets/", f"]({BASE_URL}/assets/"),
    (r'src="/assets/', f'src="{BASE_URL}/assets/'),
    # .qmd links -> .md with absolute URL
    (r"\(([^)]*?)\.qmd\)", rf"({BASE_URL}/\1.md)"),
    # Relative paths: ../blog/, ../slides/, ../resume/
    (r"\(\.\./blog/", f"({BASE_URL}/blog/"),
    (r"\(\.\./slides/", f"({BASE_URL}/slides/"),
    (r"\(\.\./resume/", f"({BASE_URL}/resume/"),
    # Relative paths: ./blog/, ./slides/, ./resume/
    (r"\(\./blog/", f"({BASE_URL}/blog/"),
    (r"\(\./slides/", f"({BASE_URL}/slides/"),
    (r"\(\./resume/", f"({BASE_URL}/resume/"),
    # Absolute paths: /blog/, /slides/, /resume/
    (r"\]/blog/", f"]{BASE_URL}/blog/"),
    (r"\]/slides/", f"]{BASE_URL}/slides/"),
    (r"\]/resume/", f"]{BASE_URL}/resume/"),
]


def fix_content(content: str) -> str:
    """Apply all replacements to content."""
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    return content


def process_file(file_path: Path) -> bool:
    """Process a single markdown file. Returns True if modified."""
    original = file_path.read_text(encoding="utf-8")
    modified = fix_content(original)

    if original != modified:
        file_path.write_text(modified, encoding="utf-8")
        return True
    return False


def main() -> int:
    """Main function."""
    if len(sys.argv) < 2:
        site_dir = Path("_site")
    else:
        site_dir = Path(sys.argv[1])

    if not site_dir.exists():
        print(f"Error: Directory not found: {site_dir}")
        return 1

    md_files = list(site_dir.rglob("*.md"))
    modified_count = 0

    for md_file in md_files:
        if process_file(md_file):
            print(f"Fixed: {md_file}")
            modified_count += 1

    print(f"Processed {len(md_files)} files, modified {modified_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
