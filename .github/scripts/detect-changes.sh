#!/usr/bin/env bash
set -euo pipefail

# Environment variables from GitHub Actions
: "${CONTENT_DIRS:?}" "${FEED_DIRS:=}" "${FULL_REBUILD_TRIGGERS:?}"

# Parse ADDED_FILES into array
added_files_arr=()
if [[ -n ${ADDED_FILES:-} ]]; then
  read -ra added_files_arr <<<"$ADDED_FILES"
fi

# Check if directory has added files (for feed regeneration)
has_added_file_in_dir() {
  local dir="$1"
  for file in "${added_files_arr[@]}"; do
    if [[ $file == "$dir/"* ]]; then
      return 0
    fi
  done
  return 1
}

full_rebuild_triggers="$FULL_REBUILD_TRIGGERS"

# Always do full rebuild for deployment stability
# (incremental deploy has file sync issues)
full_rebuild=true
changed_files=("$@")

# Check for full rebuild triggers
for file in "${changed_files[@]}"; do
  for trigger in $full_rebuild_triggers; do
    if [[ $file == "$trigger" ]] || [[ $file == "$trigger"* ]]; then
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
  for dir in $CONTENT_DIRS; do
    if [[ $dir == "root" ]]; then
      # root: match .qmd files without subdirectory, or assets/
      if [[ $file != */* ]] && [[ $file == *.qmd ]]; then
        dir_files[$dir]+="$file "
        break
      elif [[ $file == assets/* ]]; then
        dir_files[$dir]+="__assets__ "
        break
      fi
    elif [[ $file == "$dir/"* ]]; then
      # .qmd for single mode, other files trigger full rebuild
      if [[ $file == *.qmd ]]; then
        dir_files[$dir]+="$file "
      else
        dir_files[$dir]+="__non_qmd__ "
      fi
      break
    fi
  done
done

# Build matrix
matrix_items=()

if [[ $full_rebuild == "true" ]]; then
  for dir in $CONTENT_DIRS; do
    matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"full\",\"file\":\"\"}")
  done
else
  for dir in $CONTENT_DIRS; do
    files="${dir_files[$dir]}"
    if [[ -n $files ]]; then
      # Non-.qmd files or assets trigger full rebuild
      if [[ $files == *"__non_qmd__"* ]] || [[ $files == *"__assets__"* ]]; then
        matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"full\",\"file\":\"\"}")
      else
        qmd_files=$(echo "$files" | xargs)
        file_count=$(echo "$qmd_files" | wc -w)
        # Force full mode for feed dirs with added files
        is_feed_dir=false
        for feed_dir in $FEED_DIRS; do
          if [[ $dir == "$feed_dir" ]] && has_added_file_in_dir "$dir"; then
            is_feed_dir=true
            break
          fi
        done
        if [[ $is_feed_dir == "true" ]]; then
          matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"full\",\"file\":\"\"}")
        elif [[ $file_count -eq 1 ]]; then
          matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"single\",\"file\":\"$qmd_files\"}")
        else
          matrix_items+=("{\"dir\":\"$dir\",\"mode\":\"full\",\"file\":\"\"}")
        fi
      fi
    fi
  done
fi

# Output
if [[ ${#matrix_items[@]} -eq 0 ]]; then
  echo 'matrix={"include":[]}' >>"$GITHUB_OUTPUT"
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
