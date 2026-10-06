# WALK BURST2 (step 3): statistics of the 5-tap burst: quantity after +5 and after -5 on Rice (expected 6 and 1), 20 rounds. usage VAR=tip|base RUN=<n>
source ./lib.sh
OUT=$EV/burst2-run${RUN:-1}.txt; : > $OUT
qty() { nodes | python3 -c "
import sys,re
for l in sys.stdin:
    m=re.search(r'label=\"Rice 5kg\\\\n.*\\\\n(\d+)\"',l)
    if m: print(m.group(1)); break
else: print('NOROW')"; }
fresh 3store; settle 3 20; mark
for r in $(seq 1 20); do
  m0=$(wc -l < $S/access.log)
  q0=$(qty)
  rowburst "Rice 5kg" "Increase quantity" 5; settle 2 12; qp=$(qty)
  up1=$(tail -n +$((m0+1)) $S/access.log | grep -ac "cart/update")
  m1=$(wc -l < $S/access.log)
  rowburst "Rice 5kg" "Decrease quantity" 5; settle 2 12; qm=$(qty)
  up2=$(tail -n +$((m1+1)) $S/access.log | grep -ac "cart/update"); rm2=$(tail -n +$((m1+1)) $S/access.log | grep -ac "remove-item")
  echo "r$r start=$q0 after+5=$qp updates=$up1 after-5=$qm updates=$up2 removes=$rm2" >> $OUT
  if [ "$qm" = NOROW ]; then fresh 3store; settle 3 20; fi
done
echo "# BURST2 done $(date +%T)" >> $EV/steps.log
