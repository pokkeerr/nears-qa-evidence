# WALK S: Slidable declared difference, 4 trials; B3 swipe-delete with settle. usage VAR=tip|base START_N=400
source ./lib.sh
echo "# WALK S VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
fresh 3store; settle 3 20
for t in 1 2 3 4; do
  # trial: open pane on Eggs (S1 row 3), tap + on Rice (S1 row 1): pane state right after (a) and later (b)
  settle 2 10
  rowswipe "Brown Eggs 12pk" left; w 1.0; snap "S$t-pane-open"
  rowtap "Rice 5kg" "Increase quantity"; w 0.3; snap "S$t-after-plus-Rice-a"; w 3; snap "S$t-after-plus-Rice-b"
  rowtap "Rice 5kg" "Decrease quantity"; settle 2 10   # restore qty
done
reqlog "S1-4 slidable trials"
# trial against another SECTION: pane on Banana (S2), + on Eggs (S1)
swipe_rel 0.3; w 1.2; settle 2 10
rowswipe "Banana" left; w 1.0; snap "S5-pane-open-Banana"
rowtap "Brown Eggs 12pk" "Increase quantity"; w 0.3; snap "S5-after-plus-Eggs-a"; w 3; snap "S5-after-plus-Eggs-b"
reqlog "S5 other section"
# B3 swipe-delete with settle
fresh 3store; settle 3 20; mark
rowswipe "Cola 1.5L" left; w 1.0; snap B3s-open; rowdelete "Cola 1.5L"; w 1; snap B3s-after-delete-a; settle 2 10; snap B3s-after-delete-b; reqlog "B3s swipe delete"
echo "# S done $(date +%T)" >> $EV/steps.log
