# WALK R: add from the suggestion rail (new line, same store) and a NEW store via an item detail sheet (flag OFF)
source ./lib.sh
echo "# WALK R VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
fresh 3store; settle 4 20; mark
scroll_bottom; snap R0-bottom
tapn "Add To Cart" 1; step "R1-rail-add-new-line"
scroll_bottom; snap R1-after-bottom
ui_tap "Home" --exact >/dev/null 2>&1; w 4; mark
for i in 1 2 3 4 5 6; do swipe_rel 0.3; sleep 1.2; nodes | grep -aq 'Daily Fresh Market.nAlmond Milk 1L' && break; done
tapn 'Daily Fresh Market\nAlmond Milk 1L*' 1; w 4; snap R2-item-detail
tapn "Add To Cart" 1; w 3; settle 3 15; reqlog "R2 add item of a NEW store (detail sheet)"
tapn "Dismiss" 1; w 2
waitfor "Basket" 15; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "R2-basket-with-new-store"
scroll_bottom; snap R2-basket-bottom
echo "# R done $(date +%T)" >> $EV/steps.log
