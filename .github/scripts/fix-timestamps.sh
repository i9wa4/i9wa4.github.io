#!/usr/bin/env bash

# https://github.com/adityam/stochastic-control/blob/quarto/.github/scripts/fix-timestamps
git ls-tree -r --name-only HEAD | while read filename; do
  unixtime=$(git log -1 --format="%at" -- "${filename}")
  touchtime=$(date -d @$unixtime +'%Y%m%d%H%M.%S')
  touch -t ${touchtime} "${filename}"
done
