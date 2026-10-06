# Q4 live store discount (store 1: 10 percent, min_purchase 13, max_discount 0.50): cross min_purchase by taps, then the device CLOCK crosses the window END edge with NO tap; flag OFF
START_N=400 source $S/lib.sh
echo "# Q4 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
DB=nears_qa_3993s4
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
mysql -u root $DB -e "update flash_sale_items set status=0 where flash_sale_id=1" || exit 1
clear_cache() { ( cd $S/base/Admin && php artisan cache:clear 2>&1 | tail -1 ); }
setclock() { # NEARS-2218: the setter's own exit is not proof, re-read
  adb -s $DEV shell settings put global auto_time 0
  adb -s $DEV shell cmd alarm set-time $(( $1 * 1000 )) >/dev/null 2>&1
  sleep 2
  echo "clock set target=$(date -r $1 +%H:%M:%S) device-now=$(adb -s $DEV shell date +%H:%M:%S | tr -d '\r') [auto_time=$(adb -s $DEV shell settings get global auto_time | tr -d '\r')]" | tee -a $EV/steps.log
}
realclock() { setclock $(date +%s); adb -s $DEV shell settings put global auto_time 1; }
NOW=$(date +%s)
END_EPOCH=$((NOW+25*60)); END=$(date -r $END_EPOCH +%H:%M:%S)
mysql -u root $DB -e "update discounts set start_time='00:00:00', end_time='$END', min_purchase=13.00, max_discount=0.50, discount=10.00 where id=1" || exit 1
clear_cache >> $EV/steps.log
echo "Q4 window 00:00:00-$END min_purchase 13 max_discount 0.50 percent 10 (Eggs x6 gross 12.78 below the gate, x7 above)" >> $EV/steps.log
fresh eggs; settle 4 25; mark; snap Q4-top
rowtap "Brown Eggs 12pk" "Increase quantity"; step "Q4-eggs-plus(6->7 crosses min_purchase 13)"; settle 2 10
rowtap "Brown Eggs 12pk" "Decrease quantity"; step "Q4-eggs-minus(7->6 back below the gate)"; settle 2 10
snap Q4-before-clock
setclock $((END_EPOCH+15*60)); w 4; snap Q4-clock-moved-no-rebuild-a; w 3; snap Q4-clock-moved-no-rebuild-b
ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "Q4-reentry-after-end-edge"
rowtap "Brown Eggs 12pk" "Increase quantity"; step "Q4-eggs-plus-after-end-edge"; settle 2 10
realclock
w 3; ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "Q4-reentry-after-clock-restored"
reqlog "Q4 tail"
errs > $EV/errs-Q4.txt
mysql -u root $DB -e "update discounts set start_time='00:00:00', end_time='23:59:59', min_purchase=0.00, max_discount=999999.00, discount=10.00 where id=1; update flash_sale_items set status=1 where flash_sale_id=1"
clear_cache >> $EV/steps.log
echo "# Q4 done $(date +%T)" >> $EV/steps.log
