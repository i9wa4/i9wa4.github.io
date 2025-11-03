#!/bin/bash
set -e

# Convert .drawio files to .drawio.svg with text-to-path
generated_files=()

for drawio in "$@"; do
    svg="${drawio%.drawio}.drawio.svg"
    echo "Converting $drawio to $svg..."

    # Step 1: drawio CLI export to PDF (to avoid foreignObject)
    svg_basename=$(basename "$svg")
    pdf_tmp="/tmp/${svg_basename%.svg}_tmp_$$.pdf"
    if ! drawio -x -f pdf -o "$pdf_tmp" "$drawio" 2>/dev/null; then
        echo "✗ drawio PDF export failed for $drawio" >&2
        continue
    fi

    # Step 2: pdftocairo convert PDF to SVG (automatically converts text to paths)
    if ! pdftocairo -svg "$pdf_tmp" "$svg" 2>/dev/null; then
        echo "✗ pdftocairo conversion failed for $pdf_tmp" >&2
        continue
    fi

    generated_files+=("$svg")
    echo "✓ Generated $svg"
done

# Stage all generated files at once to avoid index.lock conflicts
if [ ${#generated_files[@]} -gt 0 ]; then
    git add "${generated_files[@]}"
    echo "Staged ${#generated_files[@]} file(s)"
fi
