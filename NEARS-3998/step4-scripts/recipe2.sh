#!/bin/bash
# usage: recipe.sh <build:base|tip> <run#>   — installs the APK, runs the full walk, writes walk/<TAG>_* artifacts
B=$1; RUN=$2; TAG=${B}${RUN}
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa
cd /Users/Apple/Projects/nears-NEARS-3998-u7-step4-zone-resolution
source $S/walk.sh
export ANDROID_SERIAL=emulator-5554
ACT=$W/${TAG}_actions.log; : # keep $ACT
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

# ---- R10 logged in (continues the same logcat capture started by recipe.sh)
sb R10_home_after_login; sleep 6; pay_dialog; se
sb R11a_chip_sheet; tap "Emirates" --first; sleep 5; se
sb R11b_select_marina; tap "Select address: Home, Marina Heights" --exact; sleep 14; pay_dialog; se
sb R12a_basket; tap "Basket" --exact; sleep 6; se
sb R12b_checkout; tap "Proceed to Checkout" --exact; sleep 10; se
sb R12c_change_select_addr; tap "Change" --exact; sleep 4; tap "FC2G+22" --first; sleep 8; se
sb R12d_change_use_current_location; tap "Change" --exact; sleep 4; tap "Use my current location" --exact; sleep 12; se
sb R12e_back_to_home; ui_back >> $ACT 2>&1; sleep 2; ui_back >> $ACT 2>&1; sleep 2; tap "Home" --exact; sleep 8; pay_dialog; se
sb R13_chip_select_dhaka; tap "Emirates" --first; sleep 5; tap "Select address: Home, Demo Zone" --first; sleep 16; pay_dialog; se
logstop $TAG
adb shell cmd connectivity airplane-mode disable >/dev/null 2>&1; echo ok > $S/proxy_mode
echo RECIPE2_DONE >> $ACT
