# WALK BURST3 (step 3): human-pace taps (250 ms apart) x5 on Rice, 15 rounds: quantity after +5 and -5. usage VAR=tip|base RUN=<n>
source ./lib.sh
OUT=$EV/burst3-run${RUN:-1}.txt; : > $OUT
qty() { nodes | python3 -c "
import sys,re
for l in sys.stdin:
    m=re.search(r'label=\"Rice 5kg\\\\n.*\\\\n(\d+)\"',l)
    if m: print(m.group(1)); break
else: print('NOROW')"; }
slow() { # slow <item> <button> <count>
  local xy; xy=$(rowbtn_xy "$1" "$2"); case "$xy" in NOROW|NOBTN|OFFSCREEN) echo "SLOW-MISS $xy" >> $EV/steps.log; return 1;; esac
  local cmd=""; for i in $(seq $3); do cmd="$cmd input tap $xy; sleep 0.25;"; done
  adb -s emulator-5556 shell "$cmd"
}
fresh 3store; settle 3 20; mark
for r in $(seq 1 15); do
  q0=$(qty); slow "Rice 5kg" "Increase quantity" 5; settle 2 12; qp=$(qty)
  slow "Rice 5kg" "Decrease quantity" 5; settle 2 12; qm=$(qty)
  echo "r$r start=$q0 after+5=$qp after-5=$qm" >> $OUT
  if [ "$qm" = NOROW ]; then fresh 3store; settle 3 20; fi
done
