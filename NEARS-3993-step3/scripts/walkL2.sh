# WALK L2 (step 3): LIVE STORE DISCOUNT: min_purchase crossing by taps, then the CLOCK crossing the window edge with NO tap.
# usage: VAR=tip|base bash walkL.sh   (single store 1; DB: scratch copy only)
source ./lib.sh
echo "# WALK L2 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
DB=nears_qa_3993s3
# the store-1 grocery items sit in a running flash sale (flash lines never take the store discount): switch it off for this walk only, restored at the end
mysql -u root $DB -e "update flash_sale_items set status=0 where flash_sale_id=1" || exit 1
clear_cache() { ( cd /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s3/qa-base/Admin && php artisan cache:clear 2>&1 | tail -1 ); }
setclock() { # setclock <epoch seconds>: auto_time off, set-time, RE-READ date (NEARS-2218: the setter's own exit is not proof)
  adb -s emulator-5556 shell settings put global auto_time 0
  adb -s emulator-5556 shell cmd alarm set-time $(( $1 * 1000 )) >/dev/null 2>&1
  sleep 2
  echo "clock set target=$(date -r $1 +%H:%M:%S) device-now=$(adb -s emulator-5556 shell date +%H:%M:%S | tr -d '\r') [auto_time=$(adb -s emulator-5556 shell settings get global auto_time | tr -d '\r')]" | tee -a $EV/steps.log
}
realclock() { setclock $(date +%s); adb -s emulator-5556 shell settings put global auto_time 1; }
NOW=$(date +%s); HM=$(date +%H%M)
if [ "$HM" -ge 2255 ] || [ "$HM" -le 5 ]; then echo "L-ABORT: too close to midnight ($HM): the window math is time-of-day" | tee -a $EV/steps.log; exit 9; fi
# ---- L-end: window ends during the walk (no tap), min_purchase 25, max_discount 3.00
END_EPOCH=$((NOW+25*60)); END=$(date -r $END_EPOCH +%H:%M:%S)
mysql -u root $DB -e "update discounts set start_time='00:00:00', end_time='$END', min_purchase=13.00, max_discount=0.50, discount=10.00 where id=1" || exit 1
clear_cache >> $EV/steps.log
echo "L-end window 00:00:00-$END min_purchase 13 max_discount 0.50 percent 10 (Eggs x6 gross 12.78 below the gate, x7 above)" >> $EV/steps.log
fresh eggs; settle 4 25; mark; snap L20-top
for i in 1 2; do rowtap "Brown Eggs 12pk" "Increase quantity"; step "L21-eggs-plus-$i(6->7 crosses min_purchase 13)"; settle 2 10; done
for i in 1 2; do rowtap "Brown Eggs 12pk" "Decrease quantity"; step "L21-eggs-minus-$i(8->7->6 back below the gate)"; settle 2 10; done
# clock crosses the END edge, no tap
snap L23-before-clock
setclock $((END_EPOCH+15*60)); w 4; snap L23-clock-moved-no-rebuild-a; w 3; snap L23-clock-moved-no-rebuild-b
ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "L23-reentry-after-end-edge"
rowtap "Brown Eggs 12pk" "Increase quantity"; step "L23-eggs-plus-after-end-edge"; settle 2 10
rowtap "Brown Eggs 12pk" "Decrease quantity"; step "L23-eggs-minus-after-end-edge"; settle 2 10
realclock
w 3; ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "L23-reentry-after-clock-restored"
reqlog "L-end tail"
errs > $EV/errs-L1.txt
# ---- L-start: window starts during the walk (no tap)
NOW=$(date +%s); START_EPOCH=$((NOW+20*60)); START=$(date -r $START_EPOCH +%H:%M:%S)
mysql -u root $DB -e "update discounts set start_time='$START', end_time='23:59:59', min_purchase=0.00, max_discount=0.50, discount=10.00 where id=1" || exit 1
clear_cache >> $EV/steps.log
echo "L-start window $START-23:59:59 min_purchase 0" >> $EV/steps.log
fresh eggs; settle 4 25; mark; snap L24-top-not-live
rowtap "Brown Eggs 12pk" "Increase quantity"; step "L24-eggs-plus-not-live"; settle 2 10
setclock $((START_EPOCH+15*60)); w 4; snap L25-clock-moved-no-rebuild-a
ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "L25-reentry-after-start-edge"
rowtap "Brown Eggs 12pk" "Increase quantity"; step "L25-eggs-plus-after-start-edge"; settle 2 10
rowtap "Brown Eggs 12pk" "Decrease quantity"; step "L25-eggs-minus-after-start-edge"; settle 2 10
realclock
w 3; ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "L25-reentry-after-clock-restored"
reqlog "L-start tail"
errs > $EV/errs-L2.txt
# restore the scratch discount row to its seed values
mysql -u root $DB -e "update discounts set start_time='00:00:00', end_time='23:59:59', min_purchase=0.00, max_discount=999999.00, discount=10.00 where id=1"
clear_cache >> $EV/steps.log
mysql -u root $DB -e "update flash_sale_items set status=1 where flash_sale_id=1"
clear_cache >> $EV/steps.log
echo "# L done $(date +%T)" >> $EV/steps.log
