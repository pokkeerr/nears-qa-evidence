#!/bin/bash
# usage: run_nets.sh <UserApp dir> <listfile> <outtsv> <labelprefix> [extra flutter test args]
APP="$1"; LIST="$2"; OUT="$3"; LP="$4"; shift 4
cd "$APP" || exit 9
while read -r f; do
  [ -z "$f" ] && continue
  slug=$(echo "$f" | tr '/.' '__')
  log="$(dirname "$OUT")/nets/${LP}_${slug}.log"
  python3 ~/.nears/bin/mem-guard.py --label "${LP}-${slug}" --max-gb 6 --wait-s 3600 -- /Users/Apple/Tools/flutter/bin/flutter test --reporter compact "$@" "$f" > "$log" 2>&1
  rc=$?
  last=$(tr '\r' '\n' < "$log" | /usr/bin/grep -E '^[0-9]+:[0-9]+ \+[0-9]+' | tail -1)
  plus=$(echo "$last" | /usr/bin/grep -oE '\+[0-9]+' | head -1)
  minus=$(echo "$last" | /usr/bin/grep -oE ' -[0-9]+' | head -1 | tr -d ' ')
  skip=$(echo "$last" | /usr/bin/grep -oE '~[0-9]+' | head -1)
  printf '%s\t%s\t%s\t%s\t%s\n' "$f" "$rc" "${plus:-?}" "${minus:-}" "${skip:-}" >> "$OUT"
done < "$LIST"
echo DONE >> "$OUT"
