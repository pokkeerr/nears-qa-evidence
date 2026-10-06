# ZP2 cold-start arrival-order noise probe: rev3 x4 and 3store x3 per variant, details delayed 4 s; first ~12 s of arrivals per cold start (no dumps)
START_N=900 source $S/lib.sh
echo "# ZP2 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
dly "stores/details 4"
for r in 1 2 3 4; do fresh_nowait rev3; w 12; reqlog "ZP rev3 r$r"; done
for r in 1 2 3; do fresh_nowait 3store; w 12; reqlog "ZP 3store r$r"; done
dly
echo "# ZP2 done $(date +%T)" >> $EV/steps.log
