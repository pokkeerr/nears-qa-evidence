# Q1 single store (store 2): Banana, Tomato (10% discount), Dove 250ml (legacy variation row, NEARS-4052 line price). flag OFF.
START_N=100 source $S/lib.sh
echo "# Q1 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
fresh q1; settle 4 25; snap Q1-top; reqlog "Q1 cold start"
for item in "Banana" "Tomato" "Dove Whitening Body Spray"; do
  rowtap "$item" "Increase quantity"; step "Q1-plus-$item"; settle 2 10
  rowtap "$item" "Decrease quantity"; step "Q1-minus-$item"; settle 2 10
done
rowburst_h "Tomato" "Increase quantity" 5; w 0.2; snap Q1-burst5-imm; settle 3 15; snap Q1-burst5-set; reqlog "Q1 burst +5 Tomato (1 PATCH expected)"
rowburst_h "Tomato" "Decrease quantity" 5; w 0.2; snap Q1-burst-5-imm; settle 3 15; snap Q1-burst-5-set; reqlog "Q1 burst -5 Tomato"
rowtap "Tomato" "Decrease quantity"; step "Q1-Tomato-zero"; settle 2 10
rowtap "Banana" "Remove Banana"; tapn "Undo" 1; step "Q1-Banana-close-undo"; settle 2 10
swipe_delete "Dove Whitening Body Spray"; w 0.3; snap Q1-dove-swipe-a; tapn "Undo" 1; step "Q1-dove-swipe-delete-undo"; settle 2 10
swipe_delete "Dove Whitening Body Spray"; w 6; step "Q1-dove-swipe-delete-final"
errs > $EV/errs-Q1.txt
echo "# Q1 done $(date +%T)" >> $EV/steps.log
