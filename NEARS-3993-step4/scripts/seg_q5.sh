# Q5 food row with options (Size Large, Lettuce/Tomato) + add-ons Extra Cheese x1 / Jalapenos x3; flag ON
START_N=500 source $S/lib.sh
echo "# Q5 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh on >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
fresh foodopts; settle 5 30; snap Q5-top-a; w 3; snap Q5-top-b; reqlog "Q5 cold start"
for i in 1 2; do swipe_rel 0.4; w 1.5; snap "Q5-mid$i"; done; scroll_bottom; snap Q5-bottom
reveal "Classic Cheeseburger" "Increase quantity"; rowtap "Classic Cheeseburger" "Increase quantity"; step "Q5-plus-Cheeseburger(options+addons x2)"; settle 3 15
rowtap "Classic Cheeseburger" "Decrease quantity"; step "Q5-minus-Cheeseburger"; settle 3 15
rowtap "Thin Crust Margherita" "Increase quantity"; step "Q5-plus-Margherita"; settle 3 15
rowtap "Thin Crust Margherita" "Decrease quantity"; step "Q5-minus-Margherita"; settle 3 15
errs > $EV/errs-Q5.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
echo "# Q5 done $(date +%T)" >> $EV/steps.log
