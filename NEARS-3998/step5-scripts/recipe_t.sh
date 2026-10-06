#!/bin/bash
# usage: recipe_t.sh <build> <iter>  debounce timing: T1 fast keys (<400 ms apart) = 1 search; T2 two keys 1.0 s apart = 2 searches
B=$1; IT=$2; TAG=${B}T${IT}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa
source $S/walk.sh
ACT=$W/${TAG}_actions.log; : > $ACT; CUR=none
sb(){ CUR=$1; mark $TAG $1 start; }
se(){ mark $TAG $CUR end; }
st(){ { echo "--- $1"; python3 $S/rows.py state; } >> $W/${TAG}_${CUR}_state.txt 2>/dev/null; }
tap(){ ui_tap "$@" >> $ACT 2>&1 || echo "TAPFAIL($?) $* [$CUR]" >> $ACT; }
waitfor(){ local i=0; while [ $i -lt ${2:-30} ]; do ui_find "$1" ${3:---exact} >/dev/null 2>&1 && return 0; sleep 2; i=$((i+1)); done; echo "WAITFAIL $1 [$CUR]" >> $ACT; return 1; }
clr(){ python3 $S/rows.py tap-edit >> $ACT 2>&1; sleep 0.8; adb shell input keyevent KEYCODE_MOVE_END; adb shell input keyevent $(printf '67 %.0s' $(seq 1 90)); sleep 3; }
rm -f $W/${TAG}_*_state.txt
echo ok > $S/proxy_mode
logstart $TAG
adb install -r $S/apk/$B.apk >> $ACT 2>&1
adb shell am force-stop $PKG; adb shell pm clear $PKG >> $ACT
adb shell pm grant $PKG android.permission.ACCESS_FINE_LOCATION; adb shell pm grant $PKG android.permission.ACCESS_COARSE_LOCATION; adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS 2>/dev/null
adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1
waitfor "Next" 40; tap "Next" --exact
waitfor "Confirm Location" 40; sleep 8
clr
sb T1_fast_keys
adb shell 'for c in Y a s; do input text $c; sleep 0.05; done'; sleep 7; st settled; se
clr
sb T2_two_keys_1s_apart
adb shell 'input text Y; sleep 1.0; input text a'; sleep 8; st settled; se
logstop $TAG
echo RECIPE_T_DONE >> $ACT
