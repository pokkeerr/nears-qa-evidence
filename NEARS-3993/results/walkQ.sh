# WALK Q: search-results a11y semantics assertion probe (is it variant-specific?). usage VAR=tip|base
source ./lib.sh
echo "# WALK Q VAR=$VAR start $(date +%T)" >> $EV/steps.log
fresh 3store
M=$(adb -s emulator-5554 logcat -d -v threadtime -s flutter:I | wc -l)
ui_tap "Search" --exact >/dev/null 2>&1; w 3
ui_tap "Search for items" >/dev/null 2>&1; w 1; adb -s emulator-5554 shell input text "Almond"; w 1; adb -s emulator-5554 shell input keyevent KEYCODE_ENTER; w 5
for i in 1 2 3 4 5 6; do echo "dump $i labelled=$(nodes | grep -ac 'label="[^"]')" >> $EV/steps.log; sleep 1.5; done
adb -s emulator-5554 logcat -d -v threadtime -s flutter:I | tail -n +$((M+1)) | grep -a "framework_error" | grep -a "msg=" | sed -E 's/^.*msg=//' | sort | uniq -c > $EV/Q-semantics-asserts.txt
echo "# Q done $(date +%T) asserts: $(cat $EV/Q-semantics-asserts.txt | tr '\n' ' ' | cut -c1-200)" >> $EV/steps.log
adb -s emulator-5554 shell input keyevent KEYCODE_BACK; sleep 1; adb -s emulator-5554 shell input keyevent KEYCODE_BACK
