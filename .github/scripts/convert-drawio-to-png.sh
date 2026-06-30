#!/bin/bash
set -e

# Convert .drawio files to .drawio.png
generated_files=()

should_convert() {
  local drawio="$1"
  local png="${drawio%.drawio}.drawio.png"

  if [ ! -f "$drawio" ]; then
    return 1
  fi

  if [ ! -f "$png" ]; then
    echo "PNG missing for $drawio; converting"
    return 0
  fi

  if ! git ls-files --error-unmatch -- "$drawio" >/dev/null 2>&1; then
    echo "Untracked $drawio; converting"
    return 0
  fi

  if ! git diff --quiet -- "$drawio"; then
    echo "Modified $drawio; converting"
    return 0
  fi

  if ! git diff --cached --quiet -- "$drawio"; then
    echo "Staged $drawio; converting"
    return 0
  fi

  return 1
}

for drawio in "$@"; do
  png="${drawio%.drawio}.drawio.png"

  if ! should_convert "$drawio"; then
    echo "Skipping unchanged $drawio"
    continue
  fi

  echo "Converting $drawio to $png..."

  # drawio CLI export to PNG with 2x scale for high quality
  if ! drawio -x -f png -s 2 -t -o "$png" "$drawio" 2>/dev/null; then
    echo "✗ drawio PNG export failed for $drawio" >&2
    continue
  fi

  generated_files+=("$png")
  echo "✓ Generated $png"
done

# Stage all generated files at once to avoid index.lock conflicts
if [ ${#generated_files[@]} -gt 0 ]; then
  git add "${generated_files[@]}"
  echo "Staged ${#generated_files[@]} file(s)"
fi
