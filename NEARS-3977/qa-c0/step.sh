#!/bin/bash
# step.sh <label> <wait_s> -- <action cmd...> : marker, act, wait, observe (appends to qa-c0/observations.txt)
L=$1; W=$2; shift 3
B=/Users/Apple/.nears/qa/NEARS-3977/baseline; Q=/Users/Apple/.nears/qa/NEARS-3977/qa-c0
R=$(wc -l < $B/requests.jsonl | tr -d ' ')
T=$(date +%H:%M:%S)
echo "== $L (reqline marker $R, logcat since $T)" >> $Q/observations.txt
"$@" 2>&1 | tee -a $Q/observations.txt
sleep "$W"
bash $Q/observe.sh "$L" "$R" "$T"
