# WALK K: cold-start + re-entry + reload request multisets, 3 reps (flag state as set by caller). usage VAR=tip|base
source ./lib.sh
echo "# WALK K VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
for r in 1 2 3; do
  fresh 3store            # mark is set inside fresh (before launch)
  settle 6 30
  reqlog "K$r cold-start-to-settled (incl. seed-excluded launch tail)"
  ui_tap "Home" --exact >/dev/null 2>&1; w 3; settle 4 20; mark
  ui_tap "Basket" --exact >/dev/null 2>&1; w 3; settle 5 20; reqlog "K$r reentry-basket"
  swipe_rel -0.5; w 2; settle 5 20; reqlog "K$r pull-reload"
done
echo "# K done $(date +%T)" >> $EV/steps.log
