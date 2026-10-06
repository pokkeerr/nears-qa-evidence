# Q6b logout -> login -> location restore -> basket -> in-session re-add (flag OFF): the pinned stale pre-clear summary check
START_N=800 source $S/lib.sh
echo "# Q6b VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
fresh 3store; settle 5 30; snap Q6b-basket-before-logout
mark; ui_tap "Profile" --exact >/dev/null 2>&1; w 3; scroll_bottom; ui_tap "Logout" --exact >/dev/null 2>&1; w 2
ui_tap "Yes" --exact >/dev/null 2>&1; w 5; ui_tap "Basket" --exact >/dev/null 2>&1; w 3; step "Q6b-guest-basket"; reqlog "Q6b logout"
ui_tap "Profile" --exact >/dev/null 2>&1; w 3; ui_tap "Log in/ Sign up" >/dev/null 2>&1; w 3
login_emily; w 3
ui_tap "Home" --exact >/dev/null 2>&1; w 4; ui_tap "Change Location" >/dev/null 2>&1; w 4; ui_tap "Use Current Location" >/dev/null 2>&1; w 6
ui_tap "Confirm Location" --exact >/dev/null 2>&1; w 6; snap Q6b-home-after-location
ui_tap "Grocery, " >/dev/null 2>&1; w 5; ui_tap "Basket" --exact >/dev/null 2>&1; w 6; settle 4 20; step "Q6b-basket-after-login"; reqlog "Q6b login + location + basket"
ui_tap "Home" --exact >/dev/null 2>&1; w 4; tapn "Add To Cart" 1; w 4; settle 3 15; snap Q6b-home-after-add
ui_tap "Basket" --exact >/dev/null 2>&1; w 5; settle 4 20; step "Q6b-basket-after-readd"; reqlog "Q6b re-add + basket"
errs > $EV/errs-Q6b.txt
echo "# Q6b done $(date +%T)" >> $EV/steps.log
