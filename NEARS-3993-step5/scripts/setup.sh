#!/bin/bash
# setup.sh <tip|base>: install + first-run flow + login on $DEV (generous waits)
cd /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s5/qa
export VAR=$1; source ./lib.sh; mkdir -p $EV
pk=$( [ $VAR = tip ] && echo $PKG_tip || echo $PKG_base )
adb -s $DEV reverse tcp:80 tcp:8593 >/dev/null
adb -s $DEV install -r $S/app-$VAR.apk 2>&1 | tail -1
for p in ACCESS_FINE_LOCATION ACCESS_COARSE_LOCATION POST_NOTIFICATIONS; do adb -s $DEV shell pm grant $pk android.permission.$p 2>&1 | tail -1; done
adb -s $DEV emu geo fix 90.3693 23.8169 >/dev/null 2>&1
adb -s $DEV shell monkey -p $pk -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
waitfor "English" 90; sleep 3; ui_tap "English" --exact >/dev/null 2>&1; sleep 1; ui_tap "Next" --exact >/dev/null 2>&1
waitfor "Use my current location" 60; sleep 3; ui_tap "Use my current location" --exact >/dev/null 2>&1; sleep 6
waitfor "Confirm Location" 40; ui_tap "Confirm Location" --exact >/dev/null 2>&1
waitfor "Login/Sign Up" 60; ui_tap "Login/Sign Up" --exact >/dev/null 2>&1; sleep 3
login_emily; waitfor "Basket" 60
echo "setup $VAR done $(date +%T)" >> $EV/steps.log
