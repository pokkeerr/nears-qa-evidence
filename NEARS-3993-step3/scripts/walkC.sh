# WALK C: checkout entry, module switch, new-store add via search, logout/login (flag OFF, 3-store)
source ./lib.sh
echo "# WALK C VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
# C1 checkout entry (all minimums met after Coffee +)
fresh 3store; mark
scroll_bottom; rowtap "Ground Coffee 250g" "Increase quantity"; step "C1-coffee-plus"
snap C1-proceed-state
tapn "Proceed to Checkout" 1; w 9; snap C1-checkout; reqlog "C1 checkout open"
scroll_top; snap C1-checkout-top
ui_back >/dev/null 2>&1; w 3; snap C1-back-to-cart; errs > $EV/errs-C1.txt
# C2 module switch
mark; ui_tap "Home" --exact >/dev/null 2>&1; w 4; snap C2-home
ui_tap "Restaurant" --exact >/dev/null 2>&1; w 6; snap C2-restaurant-home
ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "C2-basket-in-restaurant-module"
ui_tap "Home" --exact >/dev/null 2>&1; w 3; ui_tap "Grocery" --exact >/dev/null 2>&1; w 6
ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "C2-basket-back-in-grocery"
# C3 new store via search (store 37 Daily Fresh Market: Almond Milk 1L); NOTE the search results screen later breaks the a11y tree (Flutter semantics assertion, see findings), so tap at once
mark; ui_tap "Search" --exact >/dev/null 2>&1; w 3; snap C3-search
ui_tap "Search for items" >/dev/null 2>&1; w 1; adb -s emulator-5556 shell input text "Almond"; w 1; adb -s emulator-5556 shell input keyevent KEYCODE_ENTER; w 4
TAPN_RETRY=9 tapn "Add To Cart" 1; w 3; reqlog "C3 add from search"
adb -s emulator-5556 shell input keyevent KEYCODE_BACK; w 1; adb -s emulator-5556 shell input keyevent KEYCODE_BACK; w 2
waitfor "Basket" 15; ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "C3-basket-with-new-store"
errs > $EV/errs-C3.txt
# C4 logout + login
mark; ui_tap "Profile" --exact >/dev/null 2>&1; w 3; scroll_bottom; ui_tap "Logout" --exact >/dev/null 2>&1; w 2; snap C4-logout-dialog
ui_tap "Yes" --exact >/dev/null 2>&1; w 5; ui_tap "Basket" --exact >/dev/null 2>&1; w 3; snap C4-guest-basket; reqlog "C4 logout"
ui_tap "Profile" --exact >/dev/null 2>&1; w 3; ui_tap "Log in/ Sign up" >/dev/null 2>&1; w 3
login_emily; ui_tap "Home" --exact >/dev/null 2>&1; w 4; ui_tap "Grocery, " >/dev/null 2>&1; w 6
ui_tap "Basket" --exact >/dev/null 2>&1; w 4; step "C4-basket-after-login"; reqlog "C4 login"
errs > $EV/errs-C4.txt
echo "# C done $(date +%T)" >> $EV/steps.log
