# WALK D: mixed basket (flag ON, admin free delivery by order amount 40): grocery store 1 / restaurant 4 / restaurant 5 / pharmacy 7
source ./lib.sh
echo "# WALK D VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
fresh mixed; settle 3 20; mark
snap D0-top; for i in 1 2 3; do swipe_rel 0.4; w 1.5; snap "D0-mid$i"; done; scroll_bottom; snap D0-bottom; scroll_top
reqlog "D0 mixed cold start"
for item in "Rice 5kg" "Thin Crust Margherita" "Paracetamol 500mg" "Ibuprofen 400mg"; do
  reveal "$item" "Increase quantity"; rowtap "$item" "Increase quantity"; step "D1-plus-$item"; settle 2 10
  rowtap "$item" "Decrease quantity"; step "D1-minus-$item"; settle 2 10
done
scroll_top; rowburst "Rice 5kg" "Increase quantity" 5; w 0.2; snap D2-burst5-imm; settle 2 12; snap D2-burst5-set; reqlog "D2 burst +5 Rice"
rowburst "Rice 5kg" "Decrease quantity" 5; w 0.2; snap D2-burst-5-imm; settle 2 12; snap D2-burst-5-set; reqlog "D2 burst -5 Rice"
# D3 switches
revealL 'Add Cutlery, Burger Palace'; tapn 'Add Cutlery, Burger Palace' 1; step "D3-cutlery-on"; tapn 'Add Cutlery, Burger Palace' 1; step "D3-cutlery-off"
revealL 'Need Extra Packaging, Burger Palace'; tapn 'Need Extra Packaging, Burger Palace' 1; step "D3-packaging-on"; tapn 'Need Extra Packaging, Burger Palace' 1; step "D3-packaging-off"
# D4 min boundary in Pizza Heaven (min 10): 4.99 -> 9.98 (below) -> 14.97 (above)
reveal "Garlic Bread" "Increase quantity"; rowtap "Garlic Bread" "Increase quantity"; step "D4-garlic-plus1"; settle 2 10
rowtap "Garlic Bread" "Increase quantity"; step "D4-garlic-plus2"; settle 2 10
rowtap "Garlic Bread" "Decrease quantity"; step "D4-garlic-minus1"; settle 2 10
rowtap "Garlic Bread" "Decrease quantity"; step "D4-garlic-minus2"; settle 2 10
# D5 remove last row of a section
rowtap "Garlic Bread" "Decrease quantity"; step "D5-garlic-zero-last-row-section-gone"
scroll_bottom; rowtap "Ibuprofen 400mg" "Decrease quantity"; step "D5-ibuprofen-zero-last-row-last-section"
# D6 module switch (mixed basket unaffected by module)
mark; ui_tap "Home" --exact >/dev/null 2>&1; w 4; ui_tap "Restaurant" --exact >/dev/null 2>&1; w 6; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "D6-basket-in-restaurant-module"
# D7 add more items
tapn 'Add More Items, Nears Mart' 1; w 5; snap D7-add-more-items; reqlog "D7 add more items"
ui_back >/dev/null 2>&1; w 3; snap D7-back-to-cart
errs > $EV/errs-D.txt
echo "# D done $(date +%T)" >> $EV/steps.log
