# WALK B3r (step 3): swipe-delete without a dump between swipe and tap (the pane closes on any row rebuild); then Undo / no Undo. usage VAR=tip|base
source ./lib.sh
echo "# WALK B3r VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
swipe_delete() { # swipe_delete <item> : bounds read once, then swipe + tap in ONE adb call
  local b; b=$(nodes | python3 -c "
import sys,re
name=sys.argv[1]
for l in sys.stdin:
    m=re.search(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if m and m.group(5).startswith(name+'\\\\n'):
        x0,y0,x1,y1=map(int,m.groups()[:4]); print(x0,y0,x1,y1); break
" "$1")
  [ -z "$b" ] && { echo "SWIPEDEL-MISS $1" | tee -a $EV/steps.log; return 1; }
  set -- "$1" $b
  local cy=$(( ($3+$5)/2 )) xa=$(( $4-150 )) xb=$(( $2+150 )) xt=$(( $4-110 ))
  echo "swipe_delete '$1' y=$cy swipe $xa->$xb tap $xt [$(date +%H:%M:%S)]" >> $EV/steps.log
  adb -s emulator-5556 shell "input swipe $xa $cy $xb $cy 350; sleep 0.8; input tap $xt $cy"
}
fresh 3store; settle 3 20; mark
swipe_delete "Cola 1.5L"; w 0.3; snap B3r-delete-a; tapn "Undo" 1; step "B3r-swipe-delete-undo"
swipe_delete "Cola 1.5L"; w 6; step "B3r-swipe-delete-final"
fresh 3store; settle 3 20; mark
swipe_delete "Brown Eggs 12pk"; w 6; step "B3r-swipe-delete-eggs-final"
swipe_delete "Rice 5kg"; w 0.3; snap B3r-delete-rice-a; tapn "Undo" 1; step "B3r-swipe-delete-rice-undo"
errs > $EV/errs-B3r.txt
echo "# B3r done $(date +%T)" >> $EV/steps.log
