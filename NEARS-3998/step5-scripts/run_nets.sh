#!/bin/bash
# usage: run_nets.sh <wt:tip|base> <out.tsv> files...   each file alone via mem-guard, 25s gaps
WT=$1; OUT=$2; shift 2
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa
cd $S/wt/$WT/UserApp || exit 9
: > $OUT
for f in "$@"; do
  [ -f "$f" ] || { printf '%s\tMISSING\t-\t-\n' "$f" >> $OUT; continue; }
  LOG=$S/out/nets_$(basename $f .dart)_$WT.log
  python3 ~/.nears/bin/mem-guard.py --label NEARS-3998-s5-qa-nets --max-gb 6 --wait-s 3600 -- /Users/Apple/Tools/flutter/bin/flutter test --reporter compact --timeout 90s "$f" > $LOG 2>&1
  rc=$?
  plus=$(grep -oE '\+[0-9]+' $LOG | tail -1); minus=$(grep -oE '\-[0-9]+' $LOG | tail -1); last=$(tail -1 $LOG | cut -c1-80)
  printf '%s\trc=%s\t%s\t%s\t%s\n' "$f" "$rc" "${plus:-+?}" "${minus:--0}" "$last" >> $OUT
  sleep 25
done
echo NETS_DONE >> $OUT
