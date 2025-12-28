#!/usr/bin/env bash
set -euo pipefail

# Environment variables from GitHub Actions
: "${CONTENT_DIRS:?}" "${FULL_REBUILD_TRIGGERS:?}"

full_rebuild_triggers="$FULL_REBUILD_TRIGGERS"

full_rebuild=false
changed_files=("$@")

# workflow_dispatch triggers full rebuild
if [[ "${EVENT_NAME:-}" == "workflow_dispatch" ]]; then
  full_rebuild=true
fi

# Check for full rebuild triggers
for file in "${changed_files[@]}"; do
  for trigger in $full_rebuild_triggers; do
    if [[ "$file" == "$trigger" ]] || [[ "$file" == "$trigger"* ]]; then
      full_rebuild=true
      break 2
    fi
  done
done

# Collect .qmd files per directory
declare -A dir_files
for dir in $CONTENT_DIRS; do
  dir_files[$dir]=""
done

for file in "${changed_files[@]}"; do
  if [[ "$file" == *.qmd ]]; then
    for dir in $CONTENT_DIRS; do
      if [[ "$dir" == "root" ]]; then
        # root: match .qmd files without subdirectory
        if [[ "$file" != */* ]]; then
          dir_files[$dir]+="$file "
          break
        fi
      elif [[ "$file" == "$dir/"* ]]; then
        dir_files[$dir]+="$file "
        break
      fi
    done
  fi
done

# Build matrix
matrix_items=()

if [[ "$full_rebuild" == "true" ]]; then
  for dir in $CONTENT_DIRS; do
    matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"full\",\"file\":\"\"}")
  done
else
  for dir in $CONTENT_DIRS; do
    files=$(echo "${dir_files[$dir]}" | xargs)
    if [[ -n "$files" ]]; then
      file_count=$(echo "$files" | wc -w)
      if [[ "$file_count" -eq 1 ]]; then
        matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"single\",\"file\":\"$files\"}")
      else
        matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"full\",\"file\":\"\"}")
      fi
    fi
  done
fi

# Output
if [[ ${#matrix_items[@]} -eq 0 ]]; then
  echo "matrix={\"include\":[]}" >>"$GITHUB_OUTPUT"
  echo "has_builds=false" >>"$GITHUB_OUTPUT"
else
  json="{\"include\":[$(
    IFS=,
    echo "${matrix_items[*]}"
  )]}"
  echo "matrix=$json" >>"$GITHUB_OUTPUT"
  echo "has_builds=true" >>"$GITHUB_OUTPUT"
fi

echo "full_rebuild=$full_rebuild" >>"$GITHUB_OUTPUT"

echo "=== Build: full_rebuild=$full_rebuild, dirs=${!dir_files[*]} ==="
