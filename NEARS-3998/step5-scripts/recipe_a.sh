#!/bin/bash
# usage: recipe_a.sh <build:base|tip> <run#>   pick-map search walk (steps 1-5, 8). Same recipe both builds.
B=$1; RUN=$2; TAG=${B}${RUN}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa
source $S/walk.sh
ACT=$W/${TAG}_actions.log; : > $ACT
CUR=none
sb(){ CUR=$1; echo "== $1" >> $ACT; mark $TAG $1 start; }
se(){ mark $TAG $CUR end; }
st(){ # st <label> : state dump into the window's state file
  { echo "--- $1"; python3 $S/rows.py state; } >> $W/${TAG}_${CUR}_state.txt 2>/dev/null; }
tap(){ ui_tap "$@" >> $ACT 2>&1 || echo "TAPFAIL($?) $* [$CUR]" >> $ACT; }
has(){ ui_find "$1" --exact >/dev/null 2>&1; }
waitfor(){ local i=0; while [ $i -lt ${2:-30} ]; do ui_find "$1" ${3:---exact} >/dev/null 2>&1 && return 0; sleep 2; i=$((i+1)); done; echo "WAITFAIL $1 [$CUR]" >> $ACT; return 1; }
clr(){  python3 $S/rows.py tap-edit >> $ACT 2>&1; sleep 0.8; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 0.8; }
burst(){ adb shell input text "$1"; }
dismiss_sheet(){ if has "Continue as guest"; then echo "dismissing login sheet" >> $ACT; tap "Continue as guest" --exact; sleep 2; fi; }
mode(){ echo "$1" > $S/proxy_mode; echo "mode $1" >> $ACT; }
rm -f $W/${TAG}_*_state.txt
prep(){ mode ok; clr; sleep 3; }
waitsettled(){ local i=0; while [ $i -lt 14 ]; do python3 $S/rows.py state | grep -q 'SUMMARY pending=0 ' && return 0; sleep 1; i=$((i+1)); done; echo WAITSETTLE-FAIL >> $ACT; return 1; }

logstart $TAG
adb shell setprop log.tag.FA VERBOSE; adb shell setprop log.tag.FA-SVC VERBOSE
adb install -r $S/apk/$B.apk >> $ACT 2>&1
adb shell am force-stop $PKG; adb shell pm clear $PKG >> $ACT
adb shell pm grant $PKG android.permission.ACCESS_FINE_LOCATION; adb shell pm grant $PKG android.permission.ACCESS_COARSE_LOCATION; adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS 2>/dev/null
adb shell setprop log.tag.FA VERBOSE; adb shell setprop log.tag.FA-SVC VERBOSE
mode ok
adb shell cmd connectivity airplane-mode disable >/dev/null 2>&1
sleep 2
sb Q0_cold
adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1
waitfor "Next" 40; tap "Next" --exact
waitfor "Confirm Location" 40; sleep 10
st pickmap_ready; se

prep
sb A1_burst_search
mode delayzone:8; burst "Abu%sDhabi"; sleep 2.0; st t+~4s_pending; waitsettled; st settled; sleep 1; se

prep
sb A2_tap_pending_row
mode delayzone:8; burst "Al%sReem%sIsland"; sleep 1.5; tap "Checking availability" --first; sleep 0.3; st after_tap_pending_row; waitsettled; st settled; se

sb A3_tap_unavailable_row
tap "Not available yet" --first; sleep 0.3; st after_tap_unavailable_row; se

sb A4_tap_available_row
mode ok; tap ", Available" --first; sleep 7; st after_tap_available_row; se

prep
sb A5_retype_supersede_and_hint
mode delayzone:8; burst "Emirates%sPalace"; sleep 2.2; clr; burst "Marina"; sleep 1.5; st t+after_retype_pending; sleep 4; st t+old_fanout_settling; waitsettled; st t+settled_hint; sleep 1; se

prep
sb A6_same_visit_repeat
burst "Abu%sDhabi"; sleep 6; st same_visit_repeat; se

sb A7a_leave_pickmap_to_home
tap "Confirm Location" --exact; sleep 14; dismiss_sheet; sleep 2; st home_after_confirm; se
sb A7b_reopen_pickmap_prefilled
tap "Emirates" --first; sleep 9; st pickmap_reopened; mode ok; clr; sleep 3; se
sb A7c_reopen_same_query
burst "Abu%sDhabi"; sleep 7; st reopen_same_query; se

prep
sb A8_search500
mode search500; burst "Abu%sDhabi"; sleep 1.2; st t+1.2s_after_500; sleep 1.0; st t+2.2s; sleep 1.5; st t+4s; se
mode ok
prep
sb A9_after_restore
burst "Yas"; sleep 6; st after_restore; se
logstop $TAG
mode ok
echo RECIPE_A_DONE >> $ACT
