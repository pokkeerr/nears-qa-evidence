# WALK H: stale-gate probe in the mixed basket: Garlic Bread (Pizza Heaven, min 10): qty 1 -> 2 -> 3 with long settles + late re-snaps
source ./lib.sh
echo "# WALK H VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
fresh mixed; settle 4 25; mark
reveal "Garlic Bread" "Increase quantity"; snap H0-garlic1
rowtap "Garlic Bread" "Increase quantity"; settle 4 20; snap H1-garlic2-settled
rowtap "Garlic Bread" "Increase quantity"; w 0.5; snap H2-garlic3-a; settle 5 25; snap H2-garlic3-settled; w 8; snap H2-garlic3-late
reqlog "H plus plus"
rowtap "Garlic Bread" "Decrease quantity"; settle 5 25; snap H3-garlic2-settled; w 6; snap H3-garlic2-late
rowtap "Garlic Bread" "Increase quantity"; settle 5 25; snap H4-garlic3-again-settled; w 6; snap H4-garlic3-again-late
echo "# H done $(date +%T)" >> $EV/steps.log
