# Q6 re-entry + pull reload + module switch + logout/login (flag OFF); Q8 cold start request log
START_N=600 source $S/lib.sh
echo "# Q6 VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
logcat_reset
fresh 3store; settle 6 30; reqlog "Q8 cold-start-to-settled"; snap Q8-cold-settled
ui_tap "Home" --exact >/dev/null 2>&1; w 3; settle 4 20; mark
ui_tap "Basket" --exact >/dev/null 2>&1; w 3; settle 5 20; step "Q6-reentry-basket"
swipe_rel -0.5; w 2; settle 5 20; step "Q6-pull-reload"
mark; ui_tap "Home" --exact >/dev/null 2>&1; w 4; ui_tap "Restaurant" --exact >/dev/null 2>&1; w 6; snap Q6-restaurant-home
ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "Q6-basket-in-restaurant-module"
ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Grocery" --exact >/dev/null 2>&1; w 6
ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "Q6-basket-back-in-grocery"
mark; ui_tap "Profile" --exact >/dev/null 2>&1; w 3; scroll_bottom; ui_tap "Logout" --exact >/dev/null 2>&1; w 2; snap Q6-logout-dialog
ui_tap "Yes" --exact >/dev/null 2>&1; w 5; ui_tap "Basket" --exact >/dev/null 2>&1; w 3; step "Q6-guest-basket-after-logout"; reqlog "Q6 logout"
ui_tap "Profile" --exact >/dev/null 2>&1; w 3; ui_tap "Log in/ Sign up" >/dev/null 2>&1; w 3
login_emily; ui_tap "Home" --exact >/dev/null 2>&1; w 4; ui_tap "Grocery, " >/dev/null 2>&1; w 6
ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "Q6-basket-after-login"; reqlog "Q6 login"
logcat_grab Q6
errs > $EV/errs-Q6.txt
echo "# Q6 done $(date +%T)" >> $EV/steps.log
