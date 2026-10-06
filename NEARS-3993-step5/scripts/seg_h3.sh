# H3 repeat of the NEARS-4039/4059 min-gate step (Garlic Bread at Pizza Heaven, min 10): 2 -> 3 six times; per iteration an early (0.5 s) + a settled snapshot and the request order of group/validate vs cart/update; flag ON mixed
START_N=1300 source $S/lib.sh
probe() { echo "$1 $(date +%T) :: $(nodes | grep -a -o 'label="[^"]*' | grep -a -E "Pizza Heaven, Minimum order amount not reached|Minimum order met \(.{1,12}AED.{1,4} / .{1,12}10\.00|Minimum order amount not reached" | tr '\n' ' ')" >> $EV/probe-h3.txt; }
echo "# H3 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh on >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
fresh mixed; settle 5 30
reveal "Garlic Bread" "Increase quantity"
rowtap "Garlic Bread" "Increase quantity"; settle 4 20; rowtap "Garlic Bread" "Increase quantity"; settle 4 20
for i in 1 2 3 4 5 6 7 8; do
  rowtap "Garlic Bread" "Decrease quantity"; settle 4 20; mark
  rowtap "Garlic Bread" "Increase quantity"; w 0.5; probe "HS$i-a"; settle 4 20; probe "HS$i-s"; reqlog "HS$i plus (2->3)"
done
errs > $EV/errs-H3.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
echo "# H3 done $(date +%T)" >> $EV/steps.log
