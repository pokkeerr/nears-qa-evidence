#!/bin/bash
# burst.sh <rowprefix> <row#> <label> <n> <gap_s> : label-resolve once, then n taps in ONE adb shell
Q=/Users/Apple/.nears/qa/NEARS-3977/qa-c0
L=$(python3 $Q/rowtap.py --rowprefix "$1" "$2" "$3" --print); echo "$L"
C=$(echo "$L" | sed -E 's/.*@ \(([0-9]+), ([0-9]+)\).*/\1 \2/')
CMD=""; for i in $(seq 1 $4); do CMD="$CMD input tap $C; sleep $5;"; done
adb -s emulator-5600 shell "date +%s.%N; $CMD date +%s.%N"
