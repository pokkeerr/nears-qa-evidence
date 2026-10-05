#!/bin/bash
# usage: recipe.sh <build:base|tip> <run#>   — installs the APK, runs the full walk, writes walk/<TAG>_* artifacts
B=$1; RUN=$2; TAG=p${B}${RUN}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa
cd /Users/Apple/Projects/nears-NEARS-3998-u7-step4-zone-resolution
source $S/walk.sh
export ANDROID_SERIAL=emulator-5554
ACT=$W/${TAG}_actions.log; : > $ACT
read SW SH <<< $(adb shell wm size | sed 's/.*: //; s/x/ /' | tr -d '\r')
CUR=none
sb(){ CUR=$1; echo "== $1" >> $ACT; mark $TAG $1 start; }
se(){ mark $TAG $CUR end; adb exec-out screencap -p > $S/evidence/NEARS-3998/step4-${TAG}-${CUR}.png 2>/dev/null; python3 $S/uistate.py > $W/${TAG}_${CUR}_state.txt 2>/dev/null; }
tap(){ ui_tap "$@" >> $ACT 2>&1 || echo "TAPFAIL($?) $* [$CUR]" >> $ACT; }
has(){ ui_find "$1" --exact >/dev/null 2>&1; }
waitfor(){ local i=0; while [ $i -lt ${2:-30} ]; do ui_find "$1" ${3:---exact} >/dev/null 2>&1 && return 0; sleep 2; i=$((i+1)); done; echo "WAITFAIL $1 [$CUR]" >> $ACT; return 1; }
sw(){ adb shell input swipe $1 $2 $3 $4 $5; }
smallDrag(){ sw $((SW*35/100)) $((SH*55/100)) $((SW*65/100)) $((SH*50/100)) 300; }
smallDragBack(){ sw $((SW*65/100)) $((SH*50/100)) $((SW*35/100)) $((SH*55/100)) 300; }
bigSwipe(){ sw $((SW*22/100)) $((SH*635/1000)) $((SW*74/100)) $((SH*435/1000)) 300; }
dismiss_sheet(){ if has "Continue as guest"; then echo "dismissing login sheet" >> $ACT; tap "Continue as guest" --exact; sleep 2; fi; }
pay_dialog(){ if has "Pay Now"; then echo "closing payment dialog" >> $ACT; tap "Close" --exact; sleep 2; fi; }
pull(){ sw $((SW/2)) $((SH*30/100)) $((SW/2)) $((SH*75/100)) 400; }

logstart $TAG
adb install -r $S/apk/$B.apk >> $ACT 2>&1
adb shell am force-stop $PKG; adb shell pm clear $PKG >> $ACT
adb shell pm grant $PKG android.permission.ACCESS_FINE_LOCATION; adb shell pm grant $PKG android.permission.ACCESS_COARSE_LOCATION; adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS 2>/dev/null
echo ok > $S/proxy_mode
adb shell cmd connectivity airplane-mode disable >/dev/null 2>&1
sleep 2
sb Q0_cold_fresh
adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1
waitfor "Next" 40; tap "Next" --exact
waitfor "Confirm Location" 40; sleep 8
se
# P1: overtaken-response guard live: every 200 answer is held 25 s, the out-of-zone 404 is not
sb P1_stale200_then_out_of_zone
echo delay200:25 > $S/proxy_mode
smallDrag; sleep 1
for i in 1 2 3 4; do tap "Zoom out" --exact; sleep 1; done; sleep 2; for i in 1 2 3 4; do bigSwipe; sleep 1.5; done
sleep 4; python3 $S/uistate.py > $W/${TAG}_P1_early_state.txt 2>/dev/null
sleep 32; echo ok > $S/proxy_mode; se
# restore: FAB back in zone, zoom in
sb P1b_restore; tap "Use my current location" --exact; sleep 9; for i in 1 2 3 4; do tap "Zoom in" --exact; sleep 1; done; sleep 8; se
# P2: PD-S4-1 probe
sb P2a_confirm_home; tap "Confirm Location" --exact; sleep 14; dismiss_sheet; sleep 2; se
sb P2b_plain_sync_overtaken_by_marker; echo delayall:6 > $S/proxy_mode; pull; sleep 1.5; tap "Emirates" --first; sleep 16; echo ok > $S/proxy_mode; se
sb P2c_drag_inzone_after; smallDrag; sleep 9; se
sb P2d_back_home_pull; ui_back >> $ACT 2>&1; sleep 5; dismiss_sheet; pull; sleep 10; tap "Emirates" --first; sleep 9; se
logstop $TAG
echo ok > $S/proxy_mode
echo PROBE_DONE >> $ACT
