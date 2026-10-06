#!/bin/bash
# usage: recipe_m.sh <build> <iter> <variant: M1 search-then-confirm | M0 confirm-only>   race probe for the Confirm->home load
B=$1; IT=$2; V=$3; TAG=${B}${V}i${IT}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa
source $S/walk.sh
ACT=$W/${TAG}_actions.log; : > $ACT; CUR=none
sb(){ CUR=$1; mark $TAG $1 start; }
se(){ mark $TAG $CUR end; }
tap(){ ui_tap "$@" >> $ACT 2>&1 || echo "TAPFAIL($?) $* [$CUR]" >> $ACT; }
has(){ ui_find "$1" --exact >/dev/null 2>&1; }
waitfor(){ local i=0; while [ $i -lt ${2:-30} ]; do ui_find "$1" ${3:---exact} >/dev/null 2>&1 && return 0; sleep 2; i=$((i+1)); done; echo "WAITFAIL $1 [$CUR]" >> $ACT; return 1; }
clr(){ python3 $S/rows.py tap-edit >> $ACT 2>&1; sleep 0.8; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 0.8; }
echo ok > $S/proxy_mode
logstart $TAG
adb install -r $S/apk/$B.apk >> $ACT 2>&1
adb shell am force-stop $PKG; adb shell pm clear $PKG >> $ACT
adb shell pm grant $PKG android.permission.ACCESS_FINE_LOCATION; adb shell pm grant $PKG android.permission.ACCESS_COARSE_LOCATION; adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS 2>/dev/null
adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1
waitfor "Next" 40; tap "Next" --exact
waitfor "Confirm Location" 40; sleep 10
if [ "$V" = "M1" ]; then
  clr; sleep 3; adb shell input text "Abu%sDhabi"; sleep 6
  tap ", Available" --first; sleep 6
fi
sb CONFIRM_TO_HOME
tap "Confirm Location" --exact; sleep 14
se
logstop $TAG
echo RECIPE_M_DONE >> $ACT
