# B5 (Q5) summary-row landing probe (text only, no dumps kept): 3-store basket, store details delayed 5 s; scroll to the list bottom repeatedly and read Items Total / Discount / Total + minimum captions
START_N=1500 source $S/lib.sh
echo "# B5 VAR=$VAR start $(date +%T)" >> $EV/steps.log
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
dly "stores/details 5"
fresh_nowait 3store
for k in 1 2 3 4 5 6 7 8 9; do scroll_bottom; echo "B5-$k $(date +%T) :: $(nodes | python3 $S/sumprobe.py)" >> $EV/probe-b5.txt; done
dly; settle 3 20; scroll_bottom; echo "B5-final $(date +%T) :: $(nodes | python3 $S/sumprobe.py)" >> $EV/probe-b5.txt
echo "# B5 done $(date +%T)" >> $EV/steps.log
