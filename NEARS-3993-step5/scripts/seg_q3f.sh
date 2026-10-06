# Q3f store-record FAILURE via proxy fault injection (stores/details/<id> -> HTTP 500): fetchStoreForHero swallows it -> null record: bar absent, section met, no request loop; flag ON mixed: cross-module [FAIL] line
START_N=700 source $S/lib.sh
echo "# Q3f VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
logcat_reset
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
failx "stores/details/36 500"
fresh 3store; settle 6 30; snap Q3f-top-a; w 3; snap Q3f-top-b; reqlog "Q3f cold start store 36 details 500"
w 12; reqlog "Q3f idle 12s (request loop check)"
scroll_bottom; snap Q3f-bottom
rowtap "Ground Coffee 250g" "Increase quantity"; step "Q3f-plus-Coffee(no bar, section met)"; settle 2 10
rowtap "Ground Coffee 250g" "Decrease quantity"; step "Q3f-minus-Coffee"; settle 2 10
ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "Q3f-reentry"; reqlog "Q3f re-entry (no re-fetch loop)"
mark; tapn "Proceed to Checkout" 1; w 9; snap Q3f-checkout-top; settle 4 20; reqlog "Q3f checkout open (store 36 failed)"
ui_back >/dev/null 2>&1; w 3
logcat_grab Q3f-flagoff
logcat_reset
bash $S/flag.sh on >> $EV/steps.log 2>&1
failx "stores/details/7 500"
fresh mixed; settle 6 30; snap Q3g-top-a; w 3; snap Q3g-top-b; reqlog "Q3g mixed flag ON, store 7 details 500"
w 8; reqlog "Q3g idle 8s"
for i in 1 2; do swipe_rel 0.4; w 1.5; snap "Q3g-mid$i"; done; scroll_bottom; snap Q3g-bottom
logcat_grab Q3g-flagon
errs > $EV/errs-Q3f.txt
failx
bash $S/flag.sh off >> $EV/steps.log 2>&1
echo "# Q3f done $(date +%T)" >> $EV/steps.log
