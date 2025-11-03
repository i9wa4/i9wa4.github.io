#!/bin/bash
set -e

# Convert .drawio files to .drawio.svg with text-to-path
generated_files=()

for drawio in "$@"; do
    svg="${drawio%.drawio}.drawio.svg"
    echo "Converting $drawio to $svg..."

    # Step 1: drawio CLI export
    if ! drawio -x -f svg -e -o "$svg" "$drawio" 2>/dev/null; then
        echo "✗ drawio export failed for $drawio" >&2
        continue
    fi

    # Step 2: inkscape text-to-path conversion
    tmp="${svg%.svg}_tmp.svg"
    if ! inkscape "$svg" --export-text-to-path --export-plain-svg --export-filename="$tmp" 2>/dev/null; then
        echo "✗ inkscape failed for $svg" >&2
        continue
    fi

    mv "$tmp" "$svg"
    generated_files+=("$svg")
    echo "✓ Generated $svg"
done

# Stage all generated files at once to avoid index.lock conflicts
if [ ${#generated_files[@]} -gt 0 ]; then
    git add "${generated_files[@]}"
    echo "Staged ${#generated_files[@]} file(s)"
fi
