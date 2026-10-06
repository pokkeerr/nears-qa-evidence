# Q3 store record failure: store 36 (flag OFF) / store 7 (flag ON mixed) moved OUT of the ambient zone in the SCRATCH DB copy -> store-detail null: bar absent, section counts as met, no request loop, [FAIL] cross-module line at flag ON
START_N=300 source $S/lib.sh
echo "# Q3x VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
DB=nears_qa_3993s5
clear_cache() { ( cd $S/base/Admin && php artisan cache:clear 2>&1 | tail -1 ); }
logcat_reset
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
mysql -u root $DB -e "update stores set zone_id=2 where id=36" || exit 1; clear_cache >> $EV/steps.log
fresh 3store; settle 6 30; snap Q3x-top-a; w 3; snap Q3x-top-b; reqlog "Q3x cold start store 36 out of zone"
w 12; reqlog "Q3x idle 12s (request loop check)"
scroll_bottom; snap Q3x-bottom
rowtap "Ground Coffee 250g" "Increase quantity"; step "Q3x-plus-Coffee(no bar, section met)"; settle 2 10
rowtap "Ground Coffee 250g" "Decrease quantity"; step "Q3x-minus-Coffee"; settle 2 10
ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "Q3x-reentry"; reqlog "Q3x re-entry (no re-fetch loop)"
mysql -u root $DB -e "update stores set zone_id=1 where id=36" || exit 1
# flag ON mixed basket with the pharmacy store 7 out of zone
bash $S/flag.sh on >> $EV/steps.log 2>&1
mysql -u root $DB -e "update stores set zone_id=2 where id=7" || exit 1; clear_cache >> $EV/steps.log
fresh mixed; settle 6 30; snap Q3y-top-a; w 3; snap Q3y-top-b; reqlog "Q3y mixed flag ON, store 7 out of zone"
for i in 1 2; do swipe_rel 0.4; w 1.5; snap "Q3y-mid$i"; done; scroll_bottom; snap Q3y-bottom
logcat_grab Q3x
errs > $EV/errs-Q3x.txt
mysql -u root $DB -e "update stores set zone_id=1 where id in (7,36)"; clear_cache >> $EV/steps.log
bash $S/flag.sh off >> $EV/steps.log 2>&1
echo "# Q3x done $(date +%T)" >> $EV/steps.log
