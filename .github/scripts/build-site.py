#!/usr/bin/env python3
"""Build site with parallel execution.

Usage:
    python build-site.py [changed_files...]

Environment variables:
    PARALLEL_JOBS: Number of parallel workers (default: 4)
"""

from __future__ import annotations

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def run(cmd: list[str], desc: str = "") -> bool:
    """Run a command and return success status."""
    if desc:
        print(f"[START] {desc}")
    try:
        subprocess.run(cmd, check=True)
        if desc:
            print(f"[DONE] {desc}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {desc}: {e}")
        return False


def render(path: str) -> bool:
    """Render a single file or directory."""
    return run(
        ["mise", "exec", "--", "uv", "run", "quarto", "render", path],
        f"Render {path}",
    )


def generate_slides_pdf(html_path: Path) -> bool:
    """Generate PDF from slides HTML using deck2pdf."""
    pdf_path = html_path.with_suffix(".pdf")
    return run(
        ["mise", "exec", "--", "uvx", "deck2pdf@0.9.0", str(html_path), str(pdf_path)],
        f"PDF {html_path.name}",
    )


def generate_resume_pdf() -> bool:
    """Generate PDF from resume HTML using playwright."""
    html_path = Path("_site/resume/index.html")
    pdf_path = Path("_site/resume/index.pdf")
    if not html_path.exists():
        print("[SKIP] Resume HTML not found")
        return True
    return run(
        [
            "mise",
            "exec",
            "--",
            "uv",
            "run",
            "python",
            ".github/scripts/html-to-pdf.py",
            str(html_path),
            str(pdf_path),
        ],
        "PDF resume",
    )


def detect_changes(changed_files: list[str]) -> dict[str, bool]:
    """Detect which directories have changes."""
    changes = {
        "blog": False,
        "slides": False,
        "resume": False,
        "zenn": False,
        "main": False,
    }

    if not changed_files:
        # Full build
        for key in changes:
            changes[key] = True
        return changes

    for f in changed_files:
        if f.startswith("blog/"):
            changes["blog"] = True
        elif f.startswith("slides/"):
            changes["slides"] = True
        elif f.startswith("resume/"):
            changes["resume"] = True
        elif f.startswith("zenn/"):
            changes["zenn"] = True
        elif f in ("index.qmd", "about.qmd", "404.qmd", "_quarto.yaml") or f.startswith(
            "assets/"
        ):
            changes["main"] = True

    return changes


def build_full(executor: ThreadPoolExecutor) -> None:
    """Full build with parallel directory rendering and PDF generation."""
    futures = {}

    # Phase 1: Submit directory renders
    print("=== Phase 1: Building directories ===")
    for dir_name in ["blog", "slides", "resume", "zenn"]:
        future = executor.submit(render, f"{dir_name}/")
        futures[future] = ("render", dir_name)

    # Phase 1.5: Submit PDF generation (can run in parallel)
    # PDFs depend on HTML files which may already exist from gh-pages checkout
    print("=== Submitting PDF generation (parallel) ===")

    # Slides PDFs
    slides_dir = Path("_site/slides")
    if slides_dir.exists():
        for html in slides_dir.glob("*.html"):
            if html.name != "index.html":
                future = executor.submit(generate_slides_pdf, html)
                futures[future] = ("pdf", f"slides/{html.name}")

    # Resume PDF
    future = executor.submit(generate_resume_pdf)
    futures[future] = ("pdf", "resume")

    # Wait for all Phase 1 tasks
    for future in as_completed(futures):
        task_type, name = futures[future]
        try:
            future.result()
        except Exception as e:
            print(f"[ERROR] {task_type} {name}: {e}")

    # Phase 2: Top-level pages (after all content is ready)
    print("=== Phase 2: Building top-level pages ===")
    render("index.qmd")
    render("about.qmd")
    render("404.qmd")


def build_incremental(
    changed_files: list[str], changes: dict[str, bool], executor: ThreadPoolExecutor
) -> None:
    """Incremental build for changed files only."""
    futures = {}

    # Phase 1: Render changed files
    print("=== Phase 1: Building changed files ===")
    for f in changed_files:
        if f.endswith(".qmd") and not f.endswith("index.qmd") and Path(f).exists():
            future = executor.submit(render, f)
            futures[future] = ("render", f)

    # Wait for individual files
    for future in as_completed(futures):
        task_type, name = futures[future]
        try:
            future.result()
        except Exception as e:
            print(f"[ERROR] {task_type} {name}: {e}")

    futures.clear()

    # Phase 1.5: Render affected directory indexes + PDF generation
    print("=== Phase 1.5: Building indexes and PDFs ===")

    if changes["blog"]:
        future = executor.submit(render, "blog/index.qmd")
        futures[future] = ("render", "blog/index.qmd")

    if changes["slides"]:
        future = executor.submit(render, "slides/index.qmd")
        futures[future] = ("render", "slides/index.qmd")
        # Slides PDFs
        slides_dir = Path("_site/slides")
        if slides_dir.exists():
            for html in slides_dir.glob("*.html"):
                if html.name != "index.html":
                    future = executor.submit(generate_slides_pdf, html)
                    futures[future] = ("pdf", f"slides/{html.name}")

    if changes["resume"]:
        future = executor.submit(render, "resume/index.qmd")
        futures[future] = ("render", "resume/index.qmd")
        future = executor.submit(generate_resume_pdf)
        futures[future] = ("pdf", "resume")

    if changes["zenn"]:
        future = executor.submit(render, "zenn/index.qmd")
        futures[future] = ("render", "zenn/index.qmd")

    # Wait for all
    for future in as_completed(futures):
        task_type, name = futures[future]
        try:
            future.result()
        except Exception as e:
            print(f"[ERROR] {task_type} {name}: {e}")

    # Phase 2: Top-level pages
    print("=== Phase 2: Building top-level pages ===")
    if changes["blog"] or changes["zenn"] or changes["main"]:
        render("index.qmd")
    if changes["main"]:
        render("about.qmd")
        render("404.qmd")


def main() -> None:
    parallel_jobs = int(os.environ.get("PARALLEL_JOBS", "4"))
    changed_files = sys.argv[1:]

    print(f"PARALLEL_JOBS={parallel_jobs}")
    print(f"CHANGED_FILES count: {len(changed_files)}")

    changes = detect_changes(changed_files)
    print(f"Changes detected: {changes}")

    with ThreadPoolExecutor(max_workers=parallel_jobs) as executor:
        if not changed_files:
            build_full(executor)
        else:
            build_incremental(changed_files, changes, executor)

    print("=== Build complete ===")


if __name__ == "__main__":
    main()
