# Q3 mixed-module basket, flag ON, free delivery over 40: food row LAST (mixed) and FIRST (foodfirst); NEARS-4057 facets + NEARS-4039/4059 min-gate step (Garlic Bread, Pizza Heaven min 10)
START_N=400 source $S/lib.sh
echo "# Q3 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh on >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
logcat_reset
fresh mixed; settle 5 30; snap Q3m-top-a; w 3; snap Q3m-top-b; reqlog "Q3 mixed cold start"
for i in 1 2 3; do swipe_rel 0.4; w 1.5; snap "Q3m-mid$i"; done; scroll_bottom; snap Q3m-bottom
reveal "Rice 5kg" "Increase quantity"; rowtap "Rice 5kg" "Increase quantity"; step "Q3m-plus-Rice(first row, legacy)"; settle 3 15
rowtap "Rice 5kg" "Decrease quantity"; step "Q3m-minus-Rice"; settle 3 15
# NEARS-4039 / 4059 c23778 min-gate step: Garlic Bread qty 1 -> 2 -> 3 -> 2 -> 3, long settles
mark
reveal "Garlic Bread" "Increase quantity"; snap H0-garlic1
rowtap "Garlic Bread" "Increase quantity"; settle 4 20; snap H1-garlic2-settled
rowtap "Garlic Bread" "Increase quantity"; w 0.5; snap H2-garlic3-a; settle 5 25; snap H2-garlic3-settled; w 8; snap H2-garlic3-late
reqlog "H plus plus"
rowtap "Garlic Bread" "Decrease quantity"; settle 5 25; snap H3-garlic2-settled; w 6; snap H3-garlic2-late
rowtap "Garlic Bread" "Increase quantity"; settle 5 25; snap H4-garlic3-again-settled; w 6; snap H4-garlic3-again-late
# Q7 mixed checkout entry (Garlic at 3 = min met)
scroll_bottom; mark
tapn "Proceed to Checkout" 1; w 10; snap Q7m-checkout-top; settle 4 20; reqlog "Q7 mixed checkout open"
for i in 1 2; do swipe_rel 0.4; w 1.5; snap "Q7m-checkout-mid$i"; done
ui_back >/dev/null 2>&1; w 4; snap Q7m-back-to-cart
# food row FIRST
fresh foodfirst; settle 5 30; snap Q3f-top-a; w 3; snap Q3f-top-b; reqlog "Q3 foodfirst cold start"
for i in 1 2 3; do swipe_rel 0.4; w 1.5; snap "Q3f-mid$i"; done; scroll_bottom; snap Q3f-bottom
logcat_grab Q3
errs > $EV/errs-Q3.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
echo "# Q3 done $(date +%T)" >> $EV/steps.log
