# WALK A2: grocery, flag OFF, 3-store basket (stores 1 / 2 / 36 of zone 1). usage: VAR=tip|base bash walkA.sh
source ./lib.sh
echo "# WALK A2 VAR=$VAR start $(date +%T)" >> $EV/steps.log
fresh 3store
mark; snap A2-0-cart-top-t4; w 3; snap A2-0-cart-top-t7; reqlog "A0 cold-start-to-cart (since mark)"
scroll_bottom; snap A2-0-cart-bottom; scroll_top
# A1-A3 + / - on first, middle, last row of section 1 (digits, N unit subtitle, header subtotal, caption, summary)
for item in "Rice 5kg" "Cola 1.5L" "Brown Eggs 12pk"; do
  rowtap "$item" "Increase quantity"; step "A2-plus-$item"
  rowtap "$item" "Decrease quantity"; step "A2-minus-$item"
done
# A4 5-tap burst: one PATCH
# A5 section 2 rows (scrolled)
swipe_rel 0.3; w 1.2; snap A2-5-s2-view
for item in "Banana" "Orange Juice 1L" "Tomato"; do
  rowtap "$item" "Increase quantity"; step "A2-5-plus-$item"
  rowtap "$item" "Decrease quantity"; step "A2-5-minus-$item"
done
# A6 section 3 (single row, minimum 25): + crosses above minimum and flips Proceed; - back
scroll_bottom; snap A2-6-s3-view
rowtap "Ground Coffee 250g" "Increase quantity"; step "A2-6-plus-Coffee"
rowtap "Ground Coffee 250g" "Decrease quantity"; step "A2-6-minus-Coffee"
errs > $EV/errs-A1.txt; reqlog "A2 tail"
echo "# A2 done $(date +%T)" >> $EV/steps.log
