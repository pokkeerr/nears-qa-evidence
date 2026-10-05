# WALK E: single-store basket (store 1: Rice / Cola / Eggs), flag OFF
source ./lib.sh
echo "# WALK E VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
fresh 1store; mark; snap E0-single-top
for item in "Rice 5kg" "Cola 1.5L" "Brown Eggs 12pk"; do
  rowtap "$item" "Increase quantity"; step "E-plus-$item"
  rowtap "$item" "Decrease quantity"; step "E-minus-$item"
done
rowburst "Brown Eggs 12pk" "Increase quantity" 5; w 0.2; snap E1-burst5-imm; w 3; snap E1-burst5-set; reqlog "E1 burst +5 Eggs"
rowtap "Cola 1.5L" "Decrease quantity"; step "E2-Cola-zero(nonlast;below min 20? 17.16+eggs)"
rowburst "Brown Eggs 12pk" "Decrease quantity" 5; w 3; snap E2-eggs-burst-minus5; reqlog "E2 burst -5 Eggs"
rowtap "Brown Eggs 12pk" "Decrease quantity"; step "E2-Eggs-zero-last"
rowtap "Rice 5kg" "Decrease quantity"; step "E2-Rice-zero-only-row"
errs > $EV/errs-E.txt
echo "# E done $(date +%T)" >> $EV/steps.log
