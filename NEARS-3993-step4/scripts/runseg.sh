#!/bin/bash
# runseg.sh <seg> <DEV> [variants...]  (default: base tip)
export S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s4/qa
seg=$1; export DEV=$2; shift 2; V=${@:-base tip}
for v in $V; do
  export VAR=$v
  ( source $S/seg_$seg.sh ) > $S/evidence-run-$seg-$v.out 2>&1
  echo "$(date +%T) seg $seg $v done rc=$?" >> $S/walk.progress
done
