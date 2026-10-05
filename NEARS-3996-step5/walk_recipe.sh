#!/bin/bash
# usage: recipe.sh <tip|base>   (setup + walk; identical ops for both builds)
B=$1
Q=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3996-s5/qa
source $Q/d.sh
[ $B = tip ] && PKG=$PKG_TIP || PKG=$PKG_BASE
W=$Q/walk/$B; mkdir -p $W; : > $W/actions.log
echo ok > $Q/proxy_mode
log() { echo "$(date +%T) $*" | tee -a $W/actions.log; }
# tap with retries on NOT FOUND (exit 1); ambiguity (3) is a recipe error and is logged
T() { local n=0 rc; while [ $n -lt 6 ]; do ui_tap "$@" >/dev/null 2>$W/.err; rc=$?; [ $rc -eq 0 ] && { log "tap $* ok"; return 0; }; [ $rc -eq 3 ] && { log "tap $* AMBIGUOUS"; return 3; }; n=$((n+1)); sleep 2; done; log "tap $* NOTFOUND(rc=$rc)"; return 1; }
sd() { for i in $(seq 1 $1); do ui_scroll_down >/dev/null 2>&1; sleep 1.5; done; }
su() { for i in $(seq 1 $1); do ui_scroll_up >/dev/null 2>&1; sleep 1; done; }
snap() { sleep "${2:-0.5}"; labels | sort -u > $W/$1.txt; adb exec-out screencap -p > $W/$1.png; log "snap $1 labels=$(wc -l < $W/$1.txt)"; }
M() { mk "$B-$1"; log "== $1"; }
typeq() { # typeq <text>  : focus the in-store search field (hint first time, current text afterwards), clear, type, enter
  if [ -z "$CURQ" ]; then T "Search item in store..." --first; else T "$CURQ" --exact || T "Search item in store..." --first; fi
  sleep 1; adb shell input keyevent KEYCODE_MOVE_END; for i in $(seq 1 14); do adb shell input keyevent 67; done
  adb shell input text "$1"; adb shell input keyevent KEYCODE_ENTER; CURQ="$1"; }
home_grocery() { local n=0; while [ $n -lt 5 ]; do labels > $W/.h; if grep -q "^Grocery$" $W/.h || grep -q "^Delivery Type$" $W/.h; then log "at grocery home"; return 0; fi; ui_back >/dev/null 2>&1; sleep 3; n=$((n+1)); done; log "HOME-NOT-REACHED"; return 1; }
reveal() { local n=0 k=0; while [ $n -lt 14 ]; do ui_find "$1" --first >/dev/null 2>&1 && { log "reveal $1 ok"; return 0; }; ui_scroll_down >/dev/null 2>&1; sleep 1.5; n=$((n+1)); [ $n -eq 6 ] && { su 10; }; done; log "reveal $1 FAILED"; return 1; }
CURQ=""
to_store_list() { local n=0; while [ $n -lt 14 ]; do labels > $W/.h; if grep -q "^Delivery Type$" $W/.h && grep -q "^Newly joined$" $W/.h; then log "store list visible"; return 0; fi; if [ $n -eq 6 ]; then su 12; else ui_scroll_down >/dev/null 2>&1; sleep 1.5; fi; n=$((n+1)); done; log "to_store_list FAILED"; return 1; }
# ---- setup (not counted) -------------------------------------------------
if [ "${SKIP_SETUP:-0}" != 1 ]; then
adb shell am force-stop $PKG; adb shell pm clear $PKG >/dev/null
for p in ACCESS_FINE_LOCATION ACCESS_COARSE_LOCATION POST_NOTIFICATIONS; do adb shell pm grant $PKG android.permission.$p >/dev/null 2>&1; done
adb emu geo fix 54.425 24.45 >/dev/null
adb logcat -v threadtime -T 1 > $W/logcat.txt 2>&1 & echo $! > $W/logcat.pid
launch $PKG; sleep 12
T "English" --exact; sleep 2; T "Next" --exact; sleep 14
T "Confirm Location" --exact; sleep 9
T "Login/Sign Up" --exact; sleep 4
T "Email/Phone" --exact; sleep 1; adb shell input text "<test-account>"; sleep 1
T "Password" --exact; sleep 1; adb shell input text "<test-password>"; sleep 1
T "Sign In" --exact; sleep 4; labels | grep -q "^Sign In$" && { T "Sign In" --exact; }; sleep 10
n=0; while [ $n -lt 10 ]; do labels > $W/.h
  if grep -q "Your payment was Incomplete" $W/.h; then T "Close" --exact; sleep 4
  elif grep -q "^What are you shopping for" $W/.h; then T "Grocery, 15 stores"; sleep 9; break
  elif grep -q "^Grocery$" $W/.h; then T "Grocery" --exact; sleep 9; break
  else sleep 4; fi; n=$((n+1)); done
snap SETUP-grocery-home
fi
# ---- walk ------------------------------------------------------------------
M A01-open-store12-from-home
to_store_list; T "Fresh local" --first; sleep 9; snap A01
labels | grep -q "All Products" && log "CHECK store page open: yes" || { log "CHECK store page open: NO ABORT"; kill $(cat $W/logcat.pid) 2>/dev/null; exit 1; }
M A02-grid-scroll-pages-2-3;      sd 6; snap A02
M A03-scroll-top;                  su 8; snap A03
M A04-tab-FreshVegetables;         T "Fresh Vegetables" --exact; sleep 5; snap A04
M A05-tab-GeneralItems;            T "General Items" --exact; sleep 5; snap A05
M A06-tab-Milk;                    T "Milk" --exact; sleep 5; snap A06
M A07-tab-All;                     T "All" --exact; sleep 5; snap A07
M A08-offers-chip;                 T "Offers filter" --exact; sleep 5; snap A08
M A09-offers-sub-NEARS600Deals;    T "NEARS600 Deals" --first; sleep 5; snap A09
M A10-offers-sub-Burgers;          T "Burgers" --first; sleep 5; snap A10
M A11-offers-then-normal-Milk;     T "Milk" --exact; sleep 5; snap A11
M A12-tab-All;                     T "All" --exact; sleep 5; snap A12
M A13-filter-rating4;              T "Filter" --exact; sleep 2; T "4 stars" --exact; sleep 1; T "Filter" --exact; sleep 5; snap A13
M A14-filter-discounted;           T "Filter" --exact; sleep 2; T "Discounted Items" --first; sleep 1; T "Filter" --exact; sleep 5; snap A14
M A15-filter-price;                T "Filter" --exact; sleep 2; adb shell input swipe 138 2263 520 2263 400; sleep 1; T "Filter" --exact; sleep 5; snap A15
M A16-filter-clear;                T "Filter" --exact; sleep 2; T "Clear Filter" --exact; sleep 1; T "Filter" --exact; sleep 5; snap A16
M A17-grid-error-first-page;       echo "failpath:items/latest" > $Q/proxy_mode; T "Fresh Vegetables" --exact; sleep 5; sd 2; snap A17
M A18-grid-retry-still-failing;    T "Retry" --exact; sleep 5; snap A18
M A19-grid-retry-after-restore;    echo ok > $Q/proxy_mode; T "Retry" --exact; sleep 5; snap A19
M A20-tab-All-after-recovery;      su 3; T "All" --exact; sleep 5; snap A20
M A21-page2-error;                 echo "failpath:offset=2&limit=13" > $Q/proxy_mode; sd 4; snap A21
M A22-page2-retry;                 echo ok > $Q/proxy_mode; T "Retry" --exact; sleep 5; snap A22
M A23-scroll-up-to-header;         su 10; snap A23
M A24-instore-search-open;         T "Search" --exact; sleep 3; snap A24
M A25-search-query-e;              typeq e; sleep 5; snap A25
M A26-search-scroll-pages-2-3;     sd 8; snap A26
M A27-search-new-query-NEARS;      su 8; typeq NEARS; sleep 5; snap A27
M A28-search-no-results-zzzz;      typeq zzzz; sleep 5; snap A28
M A29-search-error;                echo "failpath:items/search" > $Q/proxy_mode; typeq milk; sleep 5; snap A29
M A30-search-retry-after-restore;  echo ok > $Q/proxy_mode; T "Retry" --exact; sleep 5; snap A30
M A31-search-sortfilter-organic;   T "Sort & Filter" --exact; sleep 3; T "Organic" --exact; sleep 1; T "Apply" --exact; sleep 5; snap A31
M A32-back-from-search;            ui_back; sleep 4; snap A32
M A33-tab-Milk-then-search;        T "Milk" --exact; sleep 5; su 6; T "Search" --exact; sleep 3; typeq milk; sleep 5; snap A33
M A34-back-from-search-2;          ui_back; sleep 4; snap A34
M A35-back-to-home;                ui_back; sleep 5; snap A35
M A36-open-store13-B;              home_grocery; to_store_list; T "Fresh supermarket" --first; sleep 9; snap A36
M A37-storeB-scroll-page2;         sd 5; snap A37
M A38-storeB-offers-chip;          su 8; T "Offers filter" --exact; sleep 5; snap A38
M A39-back-to-home-from-B;         ui_back; sleep 5; snap A39
M A40-reenter-store12;             home_grocery; to_store_list; T "Fresh local" --first; sleep 9; snap A40
M A41-store12-scroll;              sd 3; snap A41
M A42-back-to-home;                ui_back; sleep 5; snap A42
M A43-global-search-open;          home_grocery; su 6; T "Search" --first; sleep 4; snap A43
M A44-global-search-Fresh;        T "Search for items..." --exact; sleep 1; adb shell input text "Fresh"; adb shell input keyevent KEYCODE_ENTER; sleep 6; adb exec-out screencap -p > $W/A44.png; log "snap A44 (png only: the a11y tree of this results page goes stub ~12s after it settles)"
M A45-open-store12-from-search;    T "Fresh local" --first; sleep 9; snap A45
M A46-store-from-search-tab-and-scroll; sd 3; su 3; T "Fresh Vegetables" --exact; sleep 5; snap A46
M A47-back-to-search;              ui_back; sleep 4; snap A47
M A48-back-to-home;                ui_back; sleep 3; ui_back; sleep 3; snap A48
log "WALK_DONE"
kill $(cat $W/logcat.pid) 2>/dev/null
