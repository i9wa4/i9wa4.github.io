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

    # Step 2: inkscape convert PDF to SVG with text-to-path
    if ! inkscape "$pdf_tmp" --export-text-to-path --export-plain-svg --export-filename="$svg" 2>/dev/null; then
        echo "✗ inkscape conversion failed for $pdf_tmp" >&2
        continue
    fi

    # Step 3: Remove font-family attributes from paths to ensure font-independent rendering
    if command -v sed >/dev/null 2>&1; then
        sed -i '' -e 's/font-family:[^;"]*//g' -e 's/;;/;/g' "$svg"
    fi

    generated_files+=("$svg")
    echo "✓ Generated $svg"
done

# Stage all generated files at once to avoid index.lock conflicts
if [ ${#generated_files[@]} -gt 0 ]; then
    git add "${generated_files[@]}"
    echo "Staged ${#generated_files[@]} file(s)"
fi
