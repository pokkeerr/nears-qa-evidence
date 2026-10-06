#!/bin/bash
# usage: VAR=tip|base bash walkfull.sh [segments...]  default: all in order (flag OFF group, then flag ON group)
cd /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s3/qa
S=$(pwd); EV=$S/evidence/walk-$VAR; mkdir -p $EV; [ -f $EV/steps.log ] || : > $EV/steps.log; [ -f $EV/requests.txt ] || : > $EV/requests.txt
seg() { # seg <name> <start_n>
  echo "### SEG $1 start $(date +%T)" >> $EV/steps.log
  START_N=$2 bash walk$1.sh </dev/null >> $EV/seg-$1.out 2>&1
  echo "### SEG $1 end $(date +%T) rc=$?" >> $EV/steps.log
}
SEGS="${@:-A B E R K P C D G H D8 L}"
for s in $SEGS; do
  case $s in
    A) bash flag.sh off >> $EV/steps.log 2>&1; bash fd.sh off >> $EV/steps.log 2>&1; seg A 0;;
    B) seg B 100;; C) seg C 200;; E) seg E 300;; R) seg R 400;; K) seg K 500;; P) seg P 600;;
    D) bash flag.sh on >> $EV/steps.log 2>&1; bash fd.sh on >> $EV/steps.log 2>&1; seg D 1000;;
    G) seg G 1100;; H) seg H 1200;; D8) seg D8 1300;;
    M) seg M 1400;;
    L) bash flag.sh off >> $EV/steps.log 2>&1; bash fd.sh off >> $EV/steps.log 2>&1; seg L 1500;;
  esac
done
echo "WALKFULL-DONE $(date +%T)" >> $EV/steps.log
