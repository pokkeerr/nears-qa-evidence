# WALK M4 (step 3, rerun): add-on row in a mixed basket (flag ON), longer settles so no tap lands on a half-loaded screen. usage VAR=tip|base
source ./lib.sh
echo "# WALK M4 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh on >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
fresh addon; settle 6 40; sleep 3; mark; snap M4r-top
reveal "Double Bacon Burger" "Increase quantity"; snap M4r-bacon-view
rowtap "Double Bacon Burger" "Increase quantity"; step "M4r-bacon-plus"; settle 3 15
rowtap "Double Bacon Burger" "Decrease quantity"; step "M4r-bacon-minus"; settle 3 15
rowtap "Thin Crust Margherita" "Increase quantity"; step "M4r-margherita-plus"; settle 3 15
rowtap "Thin Crust Margherita" "Decrease quantity"; step "M4r-margherita-minus"; settle 3 15
rowburst "Double Bacon Burger" "Increase quantity" 3; w 0.3; snap M4r-burst3-imm; settle 3 20; snap M4r-burst3-set; reqlog "M4r burst +3 bacon"
rowburst "Double Bacon Burger" "Decrease quantity" 3; w 0.3; snap M4r-burst-3-imm; settle 3 20; snap M4r-burst-3-set; reqlog "M4r burst -3 bacon"
rowtap "Double Bacon Burger" "Decrease quantity"; step "M4r-bacon-zero"; settle 3 15
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
errs > $EV/errs-M4r.txt
echo "# M4 done $(date +%T)" >> $EV/steps.log
