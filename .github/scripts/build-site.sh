#!/usr/bin/env bash
set -euo pipefail

# Usage: build-site.sh [changed_files...]
# Environment variables:
#   PARALLEL_JOBS: Number of parallel jobs for Phase 1 (default: 1)
#
# If no arguments, build everything (full build)
# If arguments provided, build only those files + affected indexes

PARALLEL_JOBS="${PARALLEL_JOBS:-1}"
CHANGED_FILES=("$@")

echo "PARALLEL_JOBS=$PARALLEL_JOBS"
echo "CHANGED_FILES count: ${#CHANGED_FILES[@]}"

render() {
  echo "Rendering: $1"
  mise exec -- uv run quarto render "$1"
}

# Determine which directories have changes
has_blog_changes=false
has_slides_changes=false
has_resume_changes=false
has_zenn_changes=false
has_main_changes=false

if [ ${#CHANGED_FILES[@]} -eq 0 ]; then
  # Full build mode
  echo "=== Full build mode ==="
  has_blog_changes=true
  has_slides_changes=true
  has_resume_changes=true
  has_zenn_changes=true
  has_main_changes=true
else
  # Incremental build mode
  echo "=== Incremental build mode ==="
  for f in "${CHANGED_FILES[@]}"; do
    case "$f" in
    blog/*) has_blog_changes=true ;;
    slides/*) has_slides_changes=true ;;
    resume/*) has_resume_changes=true ;;
    zenn/*) has_zenn_changes=true ;;
    index.qmd | about.qmd | 404.qmd | _quarto.yaml | assets/*) has_main_changes=true ;;
    esac
  done
fi

# Phase 1: Build individual articles
echo "=== Phase 1: Building individual articles (parallel=$PARALLEL_JOBS) ==="
if [ ${#CHANGED_FILES[@]} -eq 0 ]; then
  # Full build: render all non-index files
  find blog slides resume zenn -name "*.qmd" ! -name "index.qmd" -print0 2>/dev/null |
    xargs -0 -P "$PARALLEL_JOBS" -I {} bash -c 'echo "Rendering: {}"; mise exec -- uv run quarto render "{}"'
else
  # Incremental: render only changed files (excluding index.qmd)
  for f in "${CHANGED_FILES[@]}"; do
    if [ -f "$f" ] && [[ "$f" == *.qmd ]] && [ "$(basename "$f")" != "index.qmd" ]; then
      render "$f"
    fi
  done
fi

# Phase 2: Build directory index files
echo "=== Phase 2: Building directory index files ==="
$has_blog_changes && [ -f "blog/index.qmd" ] && render "blog/index.qmd"
$has_slides_changes && [ -f "slides/index.qmd" ] && render "slides/index.qmd"
$has_resume_changes && [ -f "resume/index.qmd" ] && render "resume/index.qmd"
$has_zenn_changes && [ -f "zenn/index.qmd" ] && render "zenn/index.qmd"

# Phase 3: Build top-level pages (always rebuild if any content changed)
echo "=== Phase 3: Building top-level pages ==="
if $has_blog_changes || $has_zenn_changes || $has_main_changes; then
  [ -f "index.qmd" ] && render "index.qmd"
fi
if $has_main_changes; then
  [ -f "about.qmd" ] && render "about.qmd"
  [ -f "404.qmd" ] && render "404.qmd"
fi

# Phase 4: Generate PDFs
echo "=== Phase 4: Generating PDFs ==="

# Slides: deck2pdf
if $has_slides_changes; then
  for html in _site/slides/*.html; do
    if [ -f "$html" ] && [ "$(basename "$html")" != "index.html" ]; then
      pdf="${html%.html}.pdf"
      echo "Converting $html to $pdf"
      mise exec -- uvx deck2pdf@0.9.0 "$html" "$pdf" || echo "Warning: Failed to convert $html"
    fi
  done
fi

# Resume: playwright
if $has_resume_changes && [ -f "_site/resume/index.html" ]; then
  echo "Converting resume to PDF"
  mise exec -- uv run python .github/scripts/html-to-pdf.py \
    "_site/resume/index.html" \
    "_site/resume/index.pdf"
fi

echo "=== Build complete ==="
