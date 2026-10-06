#!/bin/bash
# usage: VAR=tip|base bash walkfull2.sh <tokens...>   tokens: ON OFF (flag + free-delivery fixtures) or a segment name (walk<name>.sh)
cd /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s3/qa
S=$(pwd); EV=$S/evidence/walk-$VAR; mkdir -p $EV; [ -f $EV/steps.log ] || : > $EV/steps.log; [ -f $EV/requests.txt ] || : > $EV/requests.txt
declare -A N=([G]=1100 [H]=1200 [D8]=1300 [M]=1400 [L]=1500 [B3r]=1600 [D]=1000 [A]=0 [BURST]=1700 [M4]=1800 [A2]=2000 [L2]=2100 [B]=100 [C]=200 [E]=300 [R]=400 [K]=500 [P]=600)
for s in "$@"; do
  case $s in
    ON) bash flag.sh on >> $EV/steps.log 2>&1; bash fd.sh on >> $EV/steps.log 2>&1;;
    OFF) bash flag.sh off >> $EV/steps.log 2>&1; bash fd.sh off >> $EV/steps.log 2>&1;;
    *) echo "### SEG $s start $(date +%T)" >> $EV/steps.log
       START_N=${N[$s]} bash walk$s.sh </dev/null >> $EV/seg-$s.out 2>&1
       echo "### SEG $s end $(date +%T) rc=$?" >> $EV/steps.log;;
  esac
done
echo "WALKFULL2-DONE $(date +%T)" >> $EV/steps.log
