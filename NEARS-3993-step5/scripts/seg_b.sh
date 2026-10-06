# B (Q5) live store discount landing on a 3-store basket, details delayed 5 s each; the server basis flips only at the last store landing; flag OFF
START_N=200 source $S/lib.sh
echo "# B VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
logcat_reset
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
dly "stores/details 5"
fresh_nowait 3store; watch_landing B1-3store-discount-delay5 38; settle 3 20; snap B1-final; reqlog "B1 3store discount delayed cold start"
dly
rowtap "Rice 5kg" "Increase quantity"; step "B2-plus-Rice"; settle 2 10
rowtap "Rice 5kg" "Decrease quantity"; step "B2-minus-Rice"; settle 2 10
logcat_grab B
errs > $EV/errs-B.txt
echo "# B done $(date +%T)" >> $EV/steps.log
