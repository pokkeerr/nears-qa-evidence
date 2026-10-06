#!/bin/bash
# one flutter test per invocation through mem-guard; 25 s fairness gap; results in auto/
Q=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s4/qa
F=/Users/Apple/Tools/flutter/bin/flutter
cd $Q/tip/UserApp
LIST=${1:-$Q/listA.txt}
OUT=${2:-$Q/auto}
mkdir -p $OUT
while read -r f; do
  [ -z "$f" ] && continue
  n=$(echo $f | tr '/' '_')
  python3 ~/.nears/bin/mem-guard.py --label NEARS-3993-s4-qa-A --max-gb 6 --wait-s 3600 -- $F test --no-pub --reporter expanded $f > $OUT/$n.log 2>&1
  rc=$?
  last=$(grep -a -E '^[0-9:]+ \+[0-9]+' $OUT/$n.log | tail -1 | sed -E 's/^[0-9:]+ //')
  echo "$(date +%T) rc=$rc $f :: $last" >> $OUT/summary.txt
  sleep 25
done < $LIST
echo ALLDONE >> $OUT/summary.txt
