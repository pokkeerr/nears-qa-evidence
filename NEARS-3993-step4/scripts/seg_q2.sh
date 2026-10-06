# Q2 3-store grocery basket (stores 1 / 2 / 36 of zone 1, flag OFF, admin free delivery over 40) + Q7 single-flag checkout entry
START_N=200 source $S/lib.sh
echo "# Q2 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
fresh 3store; settle 6 30; snap Q2-top-a; w 3; snap Q2-top-b; reqlog "Q2 cold start to cart"
scroll_bottom; snap Q2-bottom; scroll_top
for item in "Rice 5kg" "Brown Eggs 12pk"; do
  rowtap "$item" "Increase quantity"; step "Q2-plus-$item"; settle 2 10
  rowtap "$item" "Decrease quantity"; step "Q2-minus-$item"; settle 2 10
done
swipe_rel 0.3; w 1.2; snap Q2-s2-view
for item in "Banana" "Orange Juice 1L"; do
  rowtap "$item" "Increase quantity"; step "Q2-plus-$item"; settle 2 10
  rowtap "$item" "Decrease quantity"; step "Q2-minus-$item"; settle 2 10
done
scroll_bottom; snap Q2-s3-view
rowtap "Ground Coffee 250g" "Increase quantity"; step "Q2-plus-Coffee(S3 crosses min 25, Proceed flips)"; settle 2 10
rowtap "Ground Coffee 250g" "Decrease quantity"; step "Q2-minus-Coffee"; settle 2 10
# Q7 checkout entry
rowtap "Ground Coffee 250g" "Increase quantity"; settle 3 15; mark
tapn "Proceed to Checkout" 1; w 9; snap Q7-checkout-top; settle 4 20; reqlog "Q7 checkout open (3 stores)"
swipe_rel 0.4; w 1.5; snap Q7-checkout-mid1
ui_back >/dev/null 2>&1; w 3; snap Q7-back-to-cart
errs > $EV/errs-Q2.txt
bash $S/fd.sh off >> $EV/steps.log 2>&1
echo "# Q2 done $(date +%T)" >> $EV/steps.log
