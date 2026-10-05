#!/bin/bash
# usage: recipe.sh <build:base|tip> <run#>   — installs the APK, runs the full walk, writes walk/<TAG>_* artifacts
B=$1; RUN=$2; TAG=${B}${RUN}
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
pay_dialog(){ if has "Pay Now"; then echo "closing payment dialog" >> $ACT; tap "Close" --exact; sleep 2; fi; }
pull(){ sw $((SW/2)) $((SH*30/100)) $((SW/2)) $((SH*75/100)) 400; }

logstart $TAG
adb install -r $S/apk/$B.apk >> $ACT 2>&1
adb shell am force-stop $PKG; adb shell pm clear $PKG >> $ACT
adb shell pm grant $PKG android.permission.ACCESS_FINE_LOCATION; adb shell pm grant $PKG android.permission.ACCESS_COARSE_LOCATION; adb shell pm grant $PKG android.permission.POST_NOTIFICATIONS 2>/dev/null
echo ok > $S/proxy_mode
adb shell cmd connectivity airplane-mode disable >/dev/null 2>&1
adb emu geo fix 54.39 24.39 >/dev/null
sleep 2
sb R1_cold_fresh
adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1
waitfor "Next" 40; tap "Next" --exact
waitfor "Confirm Location" 40; sleep 8
se
sb R2a_drag_inzone; smallDrag; sleep 8; se
sb R2b_drag_out_of_zone; for i in 1 2 3 4; do tap "Zoom out" --exact; sleep 1; done; sleep 3; for i in 1 2 3 4; do bigSwipe; sleep 1.5; done; sleep 9; se
sb R2c_fab_back_in_zone; tap "Use my current location" --exact; sleep 9; se
sb R2d_fab_twice_ttl; tap "Use my current location" --exact; sleep 1; tap "Use my current location" --exact; sleep 9; se
sb R2e_zoom_restore; for i in 1 2 3 4; do tap "Zoom in" --exact; sleep 1; done; sleep 8; se
sb R2f_two_quick_drags; adb shell "input swipe $((SW*35/100)) $((SH*55/100)) $((SW*55/100)) $((SH*52/100)) 150; input swipe $((SW*55/100)) $((SH*52/100)) $((SW*35/100)) $((SH*58/100)) 150"; sleep 10; se
sb R3_confirm_to_home; tap "Confirm Location" --exact; sleep 16; se
sb R3b_dismiss_login_sheet; dismiss_sheet; sleep 3; se
sb R4_kill_relaunch_saved_addr; adb shell am force-stop $PKG; sleep 2; adb shell am start -n $PKG/com.izzes.nears.MainActivity >> $ACT 2>&1; sleep 25; dismiss_sheet; se
sb R5_home_pull_refresh; pull; sleep 10; se
sb R6_chip_to_pickmap; tap "Emirates" --first; sleep 8; se
sb R7a_zone500_drag; echo zone500 > $S/proxy_mode; smallDrag; sleep 9; se
sb R7b_zone_restored_drag; echo ok > $S/proxy_mode; smallDragBack; sleep 9; se
sb R7c_back_to_home; ui_back >> $ACT 2>&1; sleep 6; dismiss_sheet; se
sb R7d_zone500_home_refresh; echo zone500 > $S/proxy_mode; pull; sleep 10; se
sb R7e_zone_restored_home_refresh; echo ok > $S/proxy_mode; pull; sleep 10; se
sb R8a_airplane_home_refresh; adb shell cmd connectivity airplane-mode enable >> $ACT 2>&1; sleep 4; pull; sleep 8; se
sb R8b_airplane_off_try_again; adb shell cmd connectivity airplane-mode disable >> $ACT 2>&1; sleep 8; tap "Try Again" --exact; sleep 14; dismiss_sheet; se
sb R9a_profile_login_screen; tap "Profile" --exact; sleep 3; tap "Log in/ Sign up" --exact; sleep 4; se
sb R9b_signin; tap "Email/Phone" --exact; sleep 1; adb shell input text "customer@nears.com"; tap "Password" --exact; sleep 1; adb shell input text "123456789"; adb shell input keyevent KEYCODE_BACK; sleep 1; tap "Sign In" --exact; sleep 12; pay_dialog; se
sb R9c_home_after_login; tap "Home" --exact; sleep 14; pay_dialog; se
