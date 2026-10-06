#!/bin/bash
# usage: recipe_x.sh <build> <iter>   refined supersede window: old fan-out settles WHILE the new list is pending (old delay 3 s, new delay 10 s)
B=$1; IT=$2; TAG=${B}X${IT}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa
source $S/walk.sh
ACT=$W/${TAG}_actions.log; : > $ACT; CUR=none
sb(){ CUR=$1; mark $TAG $1 start; }
se(){ mark $TAG $CUR end; }
st(){ { echo "--- $1"; python3 $S/rows.py state; } >> $W/${TAG}_${CUR}_state.txt 2>/dev/null; }
tap(){ ui_tap "$@" >> $ACT 2>&1 || echo "TAPFAIL($?) $* [$CUR]" >> $ACT; }
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
waitfor "Confirm Location" 40; sleep 10
python3 $S/rows.py tap-edit >> $ACT 2>&1; sleep 0.8; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 3
sb X1_supersede_old_settles_during_new_pending
mode delayzone:3; adb shell input text "Emirates%sPalace"; sleep 1.6
mode delayzone:10; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 0.3; adb shell input text "Marina"
sleep 3.0; st t+new_pending_before_old_settles
sleep 1.0; st t+old_settled_new_still_pending
sleep 1.5; st t+old_settled_new_still_pending_2
i=0; while [ $i -lt 14 ]; do python3 $S/rows.py state | grep -q 'SUMMARY pending=0 ' && break; sleep 1; i=$((i+1)); done; st t+settled_hint; sleep 1; se
logstop $TAG
mode ok
echo RECIPE_X_DONE >> $ACT
