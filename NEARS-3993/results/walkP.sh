# WALK P: pixel equivalence probe (no image is read back into context; compared by script). usage VAR=tip|base
source ./lib.sh
PX=$S/px; mkdir -p $PX
shot() { adb -s emulator-5554 exec-out screencap -p > "$PX/$VAR-$1.png"; echo "shot $1 [$(date +%T)]" >> $EV/steps.log; }
echo "# WALK P VAR=$VAR start $(date +%T)" >> $EV/steps.log
fresh 3store; settle 4 25; sleep 2; shot 3store-top
swipe_rel 0.4; sleep 2; shot 3store-mid
scroll_bottom; sleep 2; shot 3store-bottom
fresh mixed; settle 4 25; sleep 2; shot mixed-top
swipe_rel 0.4; sleep 2; shot mixed-mid1
swipe_rel 0.4; sleep 2; shot mixed-mid2
scroll_bottom; sleep 2; shot mixed-bottom
echo "# P done $(date +%T)" >> $EV/steps.log
