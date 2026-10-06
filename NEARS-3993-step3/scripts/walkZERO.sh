# WALK ZERO (step 3): repeat the two steps where one label-level difference showed (D5 Ibuprofen to zero in the mixed basket, B1 OJ to zero in section 2): count the +/- /Remove buttons of the neighbouring row at +0.4 s / +2.8 s / +9 s. usage VAR=tip|base RUN=<n>
source ./lib.sh
OUT=$EV/zero-run${RUN:-1}.txt; : > $OUT
cnt() { nodes | python3 -c "
import sys,re
t=sys.stdin.read()
print('inc=%d dec=%d rm=%d'%(len(re.findall(r'label=\"Increase quantity\"',t)),len(re.findall(r'label=\"Decrease quantity\"',t)),len(re.findall(r'label=\"Remove [^\"]*\"',t))))"; }
bash $S/flag.sh on >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
for r in 1 2 3 4 5 6; do
  fresh mixed; settle 4 25; scroll_bottom
  rowtap "Ibuprofen 400mg" "Decrease quantity"; sleep 0.4; a=$(cnt); sleep 2.4; b=$(cnt); sleep 6; c=$(cnt)
  echo "D5 r$r +0.4s[$a] +2.8s[$b] +9s[$c]" >> $OUT
done
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
for r in 1 2 3 4 5 6; do
  fresh 3store; settle 4 25
  rowtap "Cola 1.5L" "Decrease quantity"; settle 2 10
  rowtap "Brown Eggs 12pk" "Decrease quantity"; settle 2 10
  swipe_rel 0.3; w 1.2
  rowtap "Banana" "Decrease quantity"; settle 2 10; rowtap "Banana" "Decrease quantity"; settle 2 10
  rowtap "Tomato" "Decrease quantity"; settle 2 10
  rowtap "Orange Juice 1L" "Decrease quantity"; sleep 0.4; a=$(cnt); sleep 2.4; b=$(cnt); sleep 6; c=$(cnt)
  echo "B1 r$r +0.4s[$a] +2.8s[$b] +9s[$c]" >> $OUT
done
