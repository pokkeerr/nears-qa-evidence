# H2 repeat of the NEARS-4039/4059 min-gate step (Garlic Bread at Pizza Heaven, min 10): 2 -> 3 six times; per iteration an early (0.5 s) + a settled snapshot and the request order of group/validate vs cart/update; flag ON mixed
START_N=1100 source $S/lib.sh
echo "# H2 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh on >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
fresh mixed; settle 5 30
reveal "Garlic Bread" "Increase quantity"; snap HR-start
rowtap "Garlic Bread" "Increase quantity"; settle 4 20; rowtap "Garlic Bread" "Increase quantity"; settle 4 20; snap HR-at3
for i in 1 2 3 4 5 6; do
  rowtap "Garlic Bread" "Decrease quantity"; settle 4 20; mark
  rowtap "Garlic Bread" "Increase quantity"; w 0.5; snap "HR$i-a"; settle 4 20; snap "HR$i-s"; reqlog "HR$i plus (2->3)"
done
errs > $EV/errs-H2.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
echo "# H2 done $(date +%T)" >> $EV/steps.log
