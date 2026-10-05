# WALK A: grocery, flag OFF, 3-store basket (stores 1 / 2 / 36 of zone 1). usage: VAR=tip|base bash walkA.sh
source ./lib.sh
: > $EV/steps.log; : > $EV/requests.txt
echo "# WALK A VAR=$VAR start $(date +%T)" >> $EV/steps.log
fresh 3store
mark; snap A0-cart-top-t4; w 3; snap A0-cart-top-t7; reqlog "A0 cold-start-to-cart (since mark)"
scroll_bottom; snap A0-cart-bottom; scroll_top
# A1-A3 + / - on first, middle, last row of section 1 (digits, N unit subtitle, header subtotal, caption, summary)
for item in "Rice 5kg" "Cola 1.5L" "Brown Eggs 12pk"; do
  rowtap "$item" "Increase quantity"; step "A-plus-$item"
  rowtap "$item" "Decrease quantity"; step "A-minus-$item"
done
# A4 5-tap burst: one PATCH
rowburst "Rice 5kg" "Increase quantity" 5; w 0.2; snap A4-burst5-imm; w 3; snap A4-burst5-set; reqlog "A4 burst +5 Rice"
rowburst "Rice 5kg" "Decrease quantity" 5; w 0.2; snap A4-burst-5-imm; w 3; snap A4-burst-5-set; reqlog "A4 burst -5 Rice"
# A5 section 2 rows (scrolled)
swipe_rel 0.3; w 1.2; snap A5-s2-view
for item in "Banana" "Orange Juice 1L" "Tomato"; do
  rowtap "$item" "Increase quantity"; step "A5-plus-$item"
  rowtap "$item" "Decrease quantity"; step "A5-minus-$item"
done
# A6 section 3 (single row, minimum 25): + crosses above minimum and flips Proceed; - back
scroll_bottom; snap A6-s3-view
rowtap "Ground Coffee 250g" "Increase quantity"; step "A6-plus-Coffee"
rowtap "Ground Coffee 250g" "Decrease quantity"; step "A6-minus-Coffee"
errs > $EV/errs-A1.txt; reqlog "A1-A6 tail"
echo "# A1-A6 done $(date +%T)" >> $EV/steps.log
