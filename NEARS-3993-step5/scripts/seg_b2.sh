# B2 (Q5) landing observed at the LIST BOTTOM (summary rows, store-36 bar): 3-store basket, details delayed 5 s, flag OFF; then the same with a 2-store rev basket
START_N=950 source $S/lib.sh
echo "# B2 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
logcat_reset
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
dly "stores/details 5"
fresh_nowait 3store; scroll_bottom; watch_landing B3-3store-bottom-delay5 40; settle 3 20; snap B3-final; reqlog "B3 3store bottom delayed"
fresh_nowait rev3; scroll_bottom; watch_landing B4-rev3-bottom-delay5 40; settle 3 20; snap B4-final; reqlog "B4 rev3 bottom delayed"
dly
logcat_grab B2
echo "# B2 done $(date +%T)" >> $EV/steps.log
