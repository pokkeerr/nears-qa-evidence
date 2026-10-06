# WALK RAIL (step 3): the suggestion-rail card after "Add To Cart": does the added card stay (with its qty stepper) or leave the rail, at +0.4 s / +2.8 s / +9 s? usage VAR=tip|base RUN=<n>
source ./lib.sh
OUT=$EV/rail-run${RUN:-1}.txt; : > $OUT
state() { nodes | python3 -c "
import sys,re
t=sys.stdin.read()
m=re.search(r'label=\"[0-9]+% OFF\\\\nNEARS MART\\\\n(\w+)\\\\n[^\"]*?(\\\\n1)?\"',t)
mango=bool(re.search(r'label=\"[^\"]*Mango[^\"]*\\\\n1\"',t))
inrail=bool(re.search(r'label=\"[^\"]*Mango[^\"]*\"',t))
print('mango_in_rail=%s mango_qty_badge=%s'%(inrail,mango))"; }
for r in 1 2 3 4 5 6; do
  fresh 3store; settle 4 20; scroll_bottom
  tapn "Add To Cart" 1; sleep 0.4; a=$(state); sleep 2.4; b=$(state); sleep 6; c=$(state)
  echo "r$r +0.4s[$a] +2.8s[$b] +9s[$c]" >> $OUT
done
