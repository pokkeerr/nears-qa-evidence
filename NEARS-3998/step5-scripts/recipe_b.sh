#!/bin/bash
# usage: recipe_b.sh <build> <iter>   guest checkout plain search (guest_delivery_address.dart:269) — flag false: autocomplete only
B=$1; IT=$2; TAG=${B}B${IT}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa
source $S/walk.sh
ACT=$W/${TAG}_actions.log; : > $ACT; CUR=none
sb(){ CUR=$1; mark $TAG $1 start; }
se(){ mark $TAG $CUR end; }
st(){ { echo "--- $1"; python3 $S/rows.py state; } >> $W/${TAG}_${CUR}_state.txt 2>/dev/null; }
tap(){ ui_tap "$@" >> $ACT 2>&1 || echo "TAPFAIL($?) $* [$CUR]" >> $ACT; }
has(){ ui_find "$1" --exact >/dev/null 2>&1; }
waitfor(){ local i=0; while [ $i -lt ${2:-30} ]; do ui_find "$1" ${3:---exact} >/dev/null 2>&1 && return 0; sleep 2; i=$((i+1)); done; echo "WAITFAIL $1 [$CUR]" >> $ACT; return 1; }
mode(){ echo "$1" > $S/proxy_mode; echo "mode $1" >> $ACT; }
rm -f $W/${TAG}_*_state.txt
mode ok
logstart $TAG
adb shell setprop log.tag.FA VERBOSE; adb shell setprop log.tag.FA-SVC VERBOSE
adb install -r $S/apk/$B.apk >> $ACT 2>&1
adb shell am force-stop $PKG; adb shell pm clear $PKG >> $ACT
adb shell pm grant $PKG android.permission.ACCESS_FINE_LOCATION; adb shell pm grant $PKG android.permission.ACCESS_COARSE_LOCATION; adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS 2>/dev/null
adb shell setprop log.tag.FA VERBOSE; adb shell setprop log.tag.FA-SVC VERBOSE
adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1
waitfor "Next" 40; tap "Next" --exact
waitfor "Confirm Location" 40; sleep 8
python3 $S/rows.py tap-edit >> $ACT 2>&1; sleep 0.8; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 1
adb shell input text "Abu%sDhabi"; sleep 6; python3 $S/rows.py tap-label ", Available" >> $ACT 2>&1; sleep 6
tap "Confirm Location" --exact; sleep 14; if has "Continue as guest"; then tap "Continue as guest" --exact; sleep 3; fi
tap "Add To Cart" --first; sleep 4; tap "Basket" --exact; sleep 5; tap "Proceed to Checkout" --first; sleep 9
sb B0_checkout_ready; st checkout_guest_form; se

python3 $S/rows.py tap-edit 4 >> $ACT 2>&1; sleep 0.8; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 3
sb B1_plain_search
adb shell input text "Abu%sDhabi"; sleep 2.0; st t+2s; sleep 4; st t+6s; se

sb B2_select_plain_row
tap "United Arab Emirates" --first; sleep 5; st after_tap_row; se

python3 $S/rows.py tap-edit 4 >> $ACT 2>&1; sleep 0.8; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 3
sb B3_search500
mode search500; adb shell input text "Abu%sDhabi"; sleep 1.2; st t+1.2s; sleep 1.0; st t+2.2s; se
mode ok
logstop $TAG
echo RECIPE_B_DONE >> $ACT
