#!/bin/bash
# usage: runtests.sh <UserApp root> <listfile> <outdir> <tag> [extra flutter test args...]
ROOT=$1; LIST=$2; OUT=$3; TAG=$4; shift 4
mkdir -p $OUT; cd $ROOT
while read -r f; do
  [ -z "$f" ] && continue
  n=$(echo "$f" | tr '/' '_')
  python3 ~/.nears/bin/mem-guard.py --label NEARS-3993-s3-qa-$TAG --max-gb 6 --wait-s 3600 -- /Users/Apple/Tools/flutter/bin/flutter test "$f" "$@" > "$OUT/$n.txt" 2>&1
  rc=$?
  last=$(grep -aE '^[0-9:]+ \+[0-9]+' "$OUT/$n.txt" | tail -1 | sed -E 's/^[0-9:]+ //' | cut -c1-80)
  echo "$f rc=$rc $last" >> $OUT/_table.txt
done < $LIST
echo ALLDONE >> $OUT/_table.txt
