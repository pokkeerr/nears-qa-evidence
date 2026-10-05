#!/bin/bash
# usage: recipe.sh <build:base|tip> <run#>   — installs the APK, runs the full walk, writes walk/<TAG>_* artifacts
B=$1; RUN=$2; N=${3:-3}; TAG=s${B}${RUN}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa
cd /Users/Apple/Projects/nears-NEARS-3998-u7-step4-zone-resolution
source $S/walk.sh
export ANDROID_SERIAL=emulator-5554
ACT=$W/${TAG}_actions.log; : > $ACT
read SW SH <<< $(adb shell wm size | sed 's/.*: //; s/x/ /' | tr -d '\r')
CUR=none
sb(){ CUR=$1; echo "== $1" >> $ACT; mark $TAG $1 start; }
se(){ mark $TAG $CUR end; python3 $S/uistate.py > $W/${TAG}_${CUR}_state.txt 2>/dev/null; }
tap(){ ui_tap "$@" >> $ACT 2>&1 || echo "TAPFAIL($?) $* [$CUR]" >> $ACT; }
has(){ ui_find "$1" --exact >/dev/null 2>&1; }
waitfor(){ local i=0; while [ $i -lt ${2:-30} ]; do ui_find "$1" ${3:---exact} >/dev/null 2>&1 && return 0; sleep 2; i=$((i+1)); done; echo "WAITFAIL $1 [$CUR]" >> $ACT; return 1; }
sw(){ adb shell input swipe $1 $2 $3 $4 $5; }
smallDrag(){ sw $((SW*35/100)) $((SH*55/100)) $((SW*65/100)) $((SH*50/100)) 300; }
smallDragBack(){ sw $((SW*65/100)) $((SH*50/100)) $((SW*35/100)) $((SH*55/100)) 300; }
bigSwipe(){ sw $((SW*22/100)) $((SH*635/1000)) $((SW*74/100)) $((SH*435/1000)) 300; }
dismiss_sheet(){ if has "Continue as guest"; then echo "dismissing login sheet" >> $ACT; tap "Continue as guest" --exact; sleep 2; fi; }
chip(){ ui_tap "Emirates" --first >> $ACT 2>&1 || ui_tap "Demo Zone" --first >> $ACT 2>&1 || ui_tap "Marina Heights" --first >> $ACT 2>&1 || echo "TAPFAIL chip [$CUR]" >> $ACT; }
pay_dialog(){ if has "Pay Now"; then echo "closing payment dialog" >> $ACT; tap "Close" --exact; sleep 2; fi; }
pull(){ sw $((SW/2)) $((SH*30/100)) $((SW/2)) $((SH*75/100)) 400; }

logstart $TAG
adb install -r $S/apk/$B.apk >> $ACT 2>&1
adb shell am force-stop $PKG; adb shell pm clear $PKG >> $ACT
adb shell pm grant $PKG android.permission.ACCESS_FINE_LOCATION; adb shell pm grant $PKG android.permission.ACCESS_COARSE_LOCATION; adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS 2>/dev/null
echo ok > $S/proxy_mode; adb emu geo fix 54.39 24.39 >/dev/null
sleep 2
sb S0_setup
adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1
waitfor "Next" 40; tap "Next" --exact
waitfor "Confirm Location" 40; sleep 8
for k in 1 2 3; do if ui_list 2>/dev/null | /usr/bin/grep -qE "Bangladesh|Dhaka|Service not available in this area"; then echo "setup: out-of-zone default, FAB retry $k" >> $ACT; ui_tap "Use my current location" --exact >> $ACT 2>&1; sleep 9; else break; fi; done
tap "Confirm Location" --exact; sleep 16; dismiss_sheet; sleep 2
tap "Profile" --exact; sleep 3; tap "Log in/ Sign up" --exact; sleep 4
tap "Email/Phone" --exact; sleep 1; adb shell input text "customer@nears.com"; tap "Password" --exact; sleep 1; adb shell input text "123456789"; adb shell input keyevent KEYCODE_BACK; sleep 1; tap "Sign In" --exact; sleep 12; pay_dialog
tap "Home" --exact; sleep 14; pay_dialog; se
for k in $(seq 1 $N); do
  sb d$k; chip; sleep 5; tap "Select address: Home, Demo Zone" --first; sleep 40; pay_dialog; se
  sb m$k; chip; sleep 5; tap "Select address: Home, Marina Heights" --exact; sleep 40; pay_dialog; se
done
logstop $TAG
echo PROBE_DONE >> $ACT
