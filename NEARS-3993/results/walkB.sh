# WALK B: removals / undo / swipe / slidable / detail sheet / reload / checkout entry / module switch (flag OFF, 3-store)
source ./lib.sh
echo "# WALK B VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
# B1 step to zero + minimum boundary
fresh 3store; mark
rowtap "Cola 1.5L" "Decrease quantity"; step "B1-zero-nonlast-Cola(S1 below min)"
rowtap "Brown Eggs 12pk" "Decrease quantity"; step "B1-zero-Eggs(S1 17.16->15.03)"
swipe_rel 0.3; w 1.2; snap B1-s2-view
rowtap "Banana" "Decrease quantity"; step "B1-Banana-2to1"
rowtap "Banana" "Decrease quantity"; step "B1-Banana-zero"
rowtap "Tomato" "Decrease quantity"; step "B1-Tomato-zero(S2 at min 5.00)"
rowtap "Orange Juice 1L" "Decrease quantity"; step "B1-OJ-zero-last-row-of-section"
scroll_bottom; snap B1-bottom
rowtap "Ground Coffee 250g" "Decrease quantity"; step "B1-Coffee-zero-last-row-last-section"
# B2 close button + undo
fresh 3store; mark
rowtap "Brown Eggs 12pk" "Remove Brown Eggs 12pk"; tapn "Undo" 1; step "B2-close-then-undo"
rowtap "Brown Eggs 12pk" "Remove Brown Eggs 12pk"; w 6; step "B2-close-no-undo"
# B3 swipe delete + undo
fresh 3store; mark
rowswipe "Cola 1.5L" left; w 1; snap B3-open; rowdelete "Cola 1.5L"; tapn "Undo" 1; step "B3-swipe-delete-undo"
rowswipe "Cola 1.5L" left; w 1; rowdelete "Cola 1.5L"; w 6; step "B3-swipe-delete-final"
# B4 Slidable declared difference
fresh 3store; mark
rowswipe "Brown Eggs 12pk" left; w 1.2; snap B4-open-Eggs
rowtap "Rice 5kg" "Increase quantity"; step "B4-SL1-pane-Eggs,plus-Rice(same section)"
swipe_rel 0.3; w 1.2; snap B4-scrolled
rowswipe "Banana" left; w 1.2; snap B4-open-Banana
rowtap "Orange Juice 1L" "Increase quantity"; step "B4-SL2-pane-Banana,plus-OJ(same section)"
rowswipe "Banana" left; w 1.2; snap B4-open-Banana2
rowtap "Brown Eggs 12pk" "Increase quantity"; step "B4-SL3-pane-Banana,plus-Eggs(other section)"
# B5 detail sheet after an earlier row was removed (cartIndex)
fresh 3store; mark
rowtap "Rice 5kg" "Remove Rice 5kg"; w 6; snap B5-after-remove
tapn 'Cola 1.5L\n*' 1; w 3; snap B5-detail-Cola; reqlog "B5 detail open"
ui_back >/dev/null 2>&1; w 2; snap B5-back
tapn 'Brown Eggs 12pk\n*' 1; w 3; snap B5-detail-Eggs
ui_back >/dev/null 2>&1; w 2
# B6 re-entry + reload
mark; ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "B6-reentry"
swipe_rel -0.5; w 4; step "B6-pull-reload"
errs > $EV/errs-B1.txt
echo "# B done $(date +%T)" >> $EV/steps.log
