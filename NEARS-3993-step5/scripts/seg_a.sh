# A (Q1) cold start with a saved multi-store basket, store-detail responses DELAYED so the landing order is observable; flag OFF
START_N=100 source $S/lib.sh
echo "# A VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
logcat_reset
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
dly "stores/details 5"
fresh_nowait 3store; watch_landing A1-3store-delay5 38; settle 3 20; snap A1-final; reqlog "A1 3store cold start delayed 5s"
dly "stores/details 4"
fresh_nowait rev3; watch_landing A2-rev3-delay4 32; settle 3 20; snap A2-final; reqlog "A2 rev3 cold start delayed 4s"
dly
fresh 3store; settle 6 30; snap A3-3store-nodelay-a; w 3; snap A3-3store-nodelay-b; reqlog "A3 3store cold start no delay"
logcat_grab A
errs > $EV/errs-A.txt
echo "# A done $(date +%T)" >> $EV/steps.log
