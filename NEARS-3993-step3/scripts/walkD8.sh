# WALK D8 (step 3): mixed basket (flag ON, free delivery 40) checkout entry + back; single-store checkout is walk C1. usage VAR=tip|base
source ./lib.sh
echo "# WALK D8 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
fresh mixed; settle 4 25
reveal "Garlic Bread" "Increase quantity"; rowtap "Garlic Bread" "Increase quantity"; settle 2 10; rowtap "Garlic Bread" "Increase quantity"; settle 3 15; snap D8-garlic3-min-met
scroll_bottom; snap D8-before-proceed; mark
tapn "Proceed to Checkout" 1; w 10; snap D8-checkout-top; settle 4 20; reqlog "D8 mixed checkout open"
for i in 1 2 3 4; do swipe_rel 0.4; w 1.5; snap "D8-checkout-mid$i"; done
ui_back >/dev/null 2>&1; w 4; snap D8-back-to-cart; mark
rowtap "Rice 5kg" "Increase quantity"; step "D8-rice-plus-after-checkout"; settle 2 12
errs > $EV/errs-D8.txt
echo "# D8 done $(date +%T)" >> $EV/steps.log
