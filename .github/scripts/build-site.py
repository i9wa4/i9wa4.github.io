#!/usr/bin/env python3
"""Build site with parallel execution.

Usage:
    python build-site.py [changed_files...]

Environment variables:
    PARALLEL_JOBS: Number of parallel workers (default: 4)
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)


@dataclass
class TaskResult:
    """Result of a task execution."""

    name: str
    success: bool
    duration: float


# Global list to collect task results
task_results: list[TaskResult] = []


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)


def run(cmd: list[str], desc: str = "", prefix: str = "") -> bool:
    """Run a command and return success status."""
    log = get_logger(prefix or "build")
    if desc:
        log.info(f"START {desc}")
    start_time = time.time()
    success = False
    output_lines: list[str] = []
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if process.stdout:
            for line in process.stdout:
                line = line.rstrip()
                if line:
                    log.debug(line)
                    output_lines.append(line)
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)
        if desc:
            log.info(f"DONE {desc}")
        success = True
    except subprocess.CalledProcessError as e:
        log.error(f"FAILED {desc}: {e}")
        # Show last 50 lines of output on error
        if output_lines:
            log.error("--- Last 50 lines of output ---")
            for line in output_lines[-50:]:
                log.error(f"  {line}")
            log.error("--- End of output ---")
        success = False
    finally:
        duration = time.time() - start_time
        if desc:
            task_results.append(
                TaskResult(name=desc, success=success, duration=duration)
            )
    return success


def render(path: str, prefix: str = "") -> bool:
    """Render a single file or directory."""
    # Derive prefix from path if not provided
    if not prefix:
        if path.startswith("blog"):
            prefix = "blog"
        elif path.startswith("slides"):
            prefix = "slides"
        elif path.startswith("resume"):
            prefix = "resume"
        elif path.startswith("zenn"):
            prefix = "zenn"
        else:
            prefix = "main"
    return run(
        ["mise", "exec", "--", "uv", "run", "quarto", "render", path],
        f"Render {path}",
        prefix,
    )


def generate_slides_pdf(html_path: Path) -> bool:
    """Generate PDF from slides HTML using deck2pdf."""
    pdf_path = html_path.with_suffix(".pdf")
    return run(
        ["mise", "exec", "--", "uvx", "deck2pdf@0.9.0", str(html_path), str(pdf_path)],
        f"PDF {html_path.name}",
        "pdf-slides",
    )


def generate_resume_pdf() -> bool:
    """Generate PDF from resume HTML using playwright."""
    html_path = Path("_site/resume/index.html")
    pdf_path = Path("_site/resume/index.pdf")
    log = get_logger("pdf-resume")
    if not html_path.exists():
        log.info("SKIP Resume HTML not found")
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
        "pdf-resume",
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
        elif (
            f in ("index.qmd", "about.qmd", "404.qmd", "_quarto.yaml")
            or f.startswith("assets/")
            or f.startswith("themes/")
            or f.startswith("_extensions/")
            or f.startswith("_includes/")
        ):
            changes["main"] = True

    return changes


def build_slides_with_pdf() -> bool:
    """Build slides and generate PDFs."""
    if not render("slides/"):
        return False
    # Generate PDFs for all slides
    slides_dir = Path("_site/slides")
    if slides_dir.exists():
        for html in slides_dir.glob("*.html"):
            if html.name != "index.html":
                generate_slides_pdf(html)
    return True


def build_resume_with_pdf() -> bool:
    """Build resume and generate PDF."""
    if not render("resume/"):
        return False
    generate_resume_pdf()
    return True


def build_full(executor: ThreadPoolExecutor) -> None:
    """Full build with parallel directory rendering and PDF generation."""
    log = get_logger("build")
    futures = {}

    # Clean _site directory for full build
    site_dir = Path("_site")
    if site_dir.exists():
        log.info("Cleaning _site directory")
        shutil.rmtree(site_dir)
    site_dir.mkdir(exist_ok=True)

    # Phase 1: Build all directories (4 parallel tasks)
    log.info("Phase 1: Building directories")
    future = executor.submit(build_slides_with_pdf)
    futures[future] = ("build", "slides+pdf")
    future = executor.submit(build_resume_with_pdf)
    futures[future] = ("build", "resume+pdf")
    future = executor.submit(render, "blog/")
    futures[future] = ("render", "blog")
    future = executor.submit(render, "zenn/")
    futures[future] = ("render", "zenn")

    # Wait for Phase 1
    for future in as_completed(futures):
        task_type, name = futures[future]
        try:
            future.result()
        except Exception as e:
            log.error(f"{task_type} {name}: {e}")

    # Phase 2: Top-level pages (after all content is ready)
    log.info("Phase 2: Building top-level pages")
    render("index.qmd")
    render("about.qmd")
    render("404.qmd")


def build_incremental(
    changed_files: list[str], changes: dict[str, bool], executor: ThreadPoolExecutor
) -> None:
    """Incremental build for changed directories only."""
    log = get_logger("build")
    futures = {}

    # Phase 1: Build changed directories (directory-level parallel, no file-level)
    log.info("Phase 1: Building changed directories")
    for dir_name in ["blog", "slides", "resume", "zenn"]:
        if changes[dir_name]:
            future = executor.submit(render, f"{dir_name}/")
            futures[future] = ("render", dir_name)

    # Phase 1.5: PDF generation for changed slides/resume
    log.info("Submitting PDF generation (parallel)")
    if changes["slides"]:
        for f in changed_files:
            if (
                f.startswith("slides/")
                and f.endswith(".qmd")
                and not f.endswith("index.qmd")
            ):
                html_name = Path(f).stem + ".html"
                html_path = Path("_site/slides") / html_name
                if html_path.exists():
                    future = executor.submit(generate_slides_pdf, html_path)
                    futures[future] = ("pdf", f"slides/{html_name}")

    if changes["resume"]:
        future = executor.submit(generate_resume_pdf)
        futures[future] = ("pdf", "resume")

    # Wait for all Phase 1 tasks
    for future in as_completed(futures):
        task_type, name = futures[future]
        try:
            future.result()
        except Exception as e:
            log.error(f"{task_type} {name}: {e}")

    # Phase 2: Top-level pages
    log.info("Phase 2: Building top-level pages")
    if changes["blog"] or changes["zenn"]:
        render("index.qmd")


def main() -> None:
    log = get_logger("build")
    parallel_jobs = int(os.environ.get("PARALLEL_JOBS") or "4")
    changed_files = sys.argv[1:]

    log.info(f"PARALLEL_JOBS={parallel_jobs}")
    log.info(f"CHANGED_FILES count: {len(changed_files)}")

    changes = detect_changes(changed_files)
    log.info(f"Changes detected: {changes}")

    with ThreadPoolExecutor(max_workers=parallel_jobs) as executor:
        if not changed_files or changes["main"]:
            # Full build when no files specified or global config changed
            log.info("Running full build")
            build_full(executor)
        else:
            # Incremental build for directory-only changes
            log.info("Running incremental build")
            build_incremental(changed_files, changes, executor)

    log.info("Build complete")

    # Print summary
    log.info("")
    log.info("=== Build Summary ===")
    total_duration = sum(r.duration for r in task_results)
    succeeded = [r for r in task_results if r.success]
    failed = [r for r in task_results if not r.success]

    # Sort by duration (longest first)
    for result in sorted(task_results, key=lambda r: r.duration, reverse=True):
        status = "OK" if result.success else "FAILED"
        log.info(f"  {result.duration:6.2f}s [{status:6}] {result.name}")

    log.info("")
    log.info(
        f"Total: {len(task_results)} tasks, {len(succeeded)} succeeded, {len(failed)} failed"
    )
    log.info(f"Total time: {total_duration:.2f}s")


if __name__ == "__main__":
    main()
