# NEARS-3993-s4 QA walk library (source me). VAR=base|tip, DEV=emulator serial. Label-driven only.
export ANDROID_SERIAL=$DEV
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s4/qa
cd /Users/Apple/Projects/nears-NEARS-3993-u2-step4 || return 9
source /Users/Apple/Projects/nears-NEARS-3993-u2-step4/scripts/app-nav/uinav.sh
EV=$S/evidence/walk-$VAR
mkdir -p $EV
N=${START_N:-0}
nodes() { ui_nodes 2>/dev/null | grep -a '^class='; }
snap() { # snap <tag> : full node dump, stable across variants
  N=$((N+1)); local tag; tag=$(printf "%s" "$1" | tr -c "A-Za-z0-9._-" "_"); local f; f=$(printf "%s/%03d-%s.txt" $EV $N "$tag")
  nodes > "$f"; echo "SNAP $f ($(wc -l < $f) nodes)" >> $EV/steps.log
  # compact digest: row/header/caption/summary labels only
  grep -a 'label="[^"]' "$f" | sed -E 's/^class=[^ ]+ clickable=(true|false) bounds=\[[0-9,]+\]\[[0-9,]+\] //' | tr '\n' '|' > "${f%.txt}.labels"
}
tapn() { # tapn <exact label> <nth 1-based, top-to-bottom> [--dry]
  local label="$1" n="$2"
  local xy; xy=$(nodes | python3 -c "
import sys,re
label=sys.argv[1]; n=int(sys.argv[2]); hits=[]
for l in sys.stdin:
    m=re.search(r'clickable=(\w+) bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if not m: continue
    lab=m.group(6)
    if lab==label or (label.endswith('*') and lab.startswith(label[:-1])):
        hits.append(((int(m.group(3))+int(m.group(5)))//2,(int(m.group(2))+int(m.group(4)))//2,m.group(1)))
hits.sort()
if len(hits)>=n: print(hits[n-1][1],hits[n-1][0],hits[n-1][2])
else: print('NONE %d'%len(hits))
" "$label" "$n")
  case "$xy" in NONE*) if [ "${TAPN_RETRY:-0}" -lt 6 ]; then sleep 2; TAPN_RETRY=$(( ${TAPN_RETRY:-0}+1 )) tapn "$label" "$n"; return $?; fi
                      echo "TAPN-MISS '$label' #$n ($xy)" | tee -a $EV/steps.log; return 1;; esac
  set -- $xy
  echo "tapn '$label' #$n -> $1 $2 (clickable=$3) [$(date +%H:%M:%S.%3N 2>/dev/null || date +%H:%M:%S)]" >> $EV/steps.log
  adb -s $DEV shell input tap $1 $2
}
burst() { # burst <label> <n> <count> : <count> rapid taps on the same node
  local label="$1" n="$2" c="$3"
  local xy; xy=$(nodes | python3 -c "
import sys,re
label=sys.argv[1]; n=int(sys.argv[2]); hits=[]
for l in sys.stdin:
    m=re.search(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if m and m.group(5)==label: hits.append(((int(m.group(2))+int(m.group(4)))//2,(int(m.group(1))+int(m.group(3)))//2))
hits.sort(); print(hits[n-1][1],hits[n-1][0]) if len(hits)>=n else print('NONE')
" "$label" "$n")
  [ "$xy" = NONE ] && { echo "BURST-MISS $label #$n" | tee -a $EV/steps.log; return 1; }
  local cmd=""; for i in $(seq $c); do cmd="$cmd input tap $xy;"; done
  echo "burst '$label' #$n x$c at $xy [$(date +%H:%M:%S)]" >> $EV/steps.log
  adb -s $DEV shell "$cmd"
}
mark() { wc -l < $S/access.log > $EV/.mark; }
reqs() { # print requests since last mark, normalized (non-asset)
  local m=$(cat $EV/.mark 2>/dev/null || echo 0)
  tail -n +$((m+1)) $S/access.log | grep -av '/storage/\|/public/assets\|\.png\|\.jpg' | awk -F'\t' '{printf "%s %s %s\n",$2,$3,$4}' | sed -E 's#/cart/(update|remove)\?cart_id=[0-9]+#/cart/\1?cart_id=<ID>#; s#cart_id=[0-9]+#cart_id=<ID>#'
}
reqlog() { local t="$1"; { echo "## $t"; reqs; } >> $EV/requests.txt; mark; }
w() { sleep "$1"; }
errs() { ui_errors $DEV 2>&1 | grep -av "^ui_errors" | head -5; }

# ---- row-addressed taps (by item NAME, buttons found inside the row's own bounds) ----
swipe_rel() { # swipe_rel <dy fraction of height, + = scroll down (finger up)>
  local wh w h; wh=$(adb -s $DEV shell wm size | tr -d '\r' | awk -F': ' '/size/{print $2}' | tail -1); w=${wh%%x*}; h=${wh#*x}
  python3 - "$w" "$h" "$1" <<'PY' | xargs -I{} adb -s $DEV shell input swipe {} 500
import sys
w,h,f=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3])
x=w//2; y0=int(h*0.62); y1=int(h*0.62-f*h)
print(x,y0,x,y1)
PY
}
# find button center: rowbtn_xy <item name prefix> <button label>  -> "x y" or NONE/OFFSCREEN
rowbtn_xy() {
  nodes | python3 -c "
import sys,re
name=sys.argv[1]; btn=sys.argv[2]
rows=[];btns=[]
for l in sys.stdin:
    m=re.search(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if not m: continue
    x0,y0,x1,y1=map(int,m.groups()[:4]); lab=m.group(5)
    if lab.startswith(name+'\\\\n'): rows.append((x0,y0,x1,y1))
    if lab==btn: btns.append((x0,y0,x1,y1))
if not rows: print('NOROW'); sys.exit()
r=rows[0]
for b in btns:
    if b[0]>=r[0] and b[2]<=r[2] and b[1]>=r[1]-5 and b[3]<=r[3]+5:
        cy=(b[1]+b[3])//2
        if 340<=cy<=2390: print((b[0]+b[2])//2,cy)
        else: print('OFFSCREEN')
        sys.exit()
print('NOBTN')
" "$1" "$2"
}
rowtap() { # rowtap <item> <Increase quantity|Decrease quantity|Remove <item>> 
  local xy tries=0
  while :; do
    xy=$(rowbtn_xy "$1" "$2")
    case "$xy" in
      NOROW|NOBTN|OFFSCREEN) tries=$((tries+1)); [ $tries -gt 9 ] && { echo "ROWTAP-MISS $1 / $2 ($xy after scrolling)" | tee -a $EV/steps.log; return 1; }
                 swipe_rel 0.22; sleep 1.2;;
      *) break;;
    esac
  done
  echo "rowtap '$1' '$2' -> $xy [$(date +%H:%M:%S)]" >> $EV/steps.log
  adb -s $DEV shell input tap $xy
}
rowburst() { # rowburst <item> <button> <count>
  local xy; xy=$(rowbtn_xy "$1" "$2")
  case "$xy" in NOROW|NOBTN|OFFSCREEN) echo "ROWBURST-MISS $1 ($xy)" | tee -a $EV/steps.log; return 1;; esac
  local cmd=""; for i in $(seq $3); do cmd="$cmd input tap $xy;"; done
  echo "rowburst '$1' '$2' x$3 -> $xy [$(date +%H:%M:%S)]" >> $EV/steps.log
  adb -s $DEV shell "$cmd"
}
scroll_top() { for i in 1 2 3; do swipe_rel -0.6; sleep 0.4; done; sleep 0.8; }
scroll_bottom() { for i in 1 2 3; do swipe_rel 0.6; sleep 0.4; done; sleep 0.8; }
PKG_tip=com.izzes.nears.nears_3993_s4_qa_tip
PKG_base=com.izzes.nears.nears_3993_s4_qa_base
waitfor() { # waitfor <label substring> <timeout s> : poll the a11y tree
  local end=$((SECONDS+$2))
  while [ $SECONDS -lt $end ]; do nodes | grep -aq "label=\"[^\"]*$1" && return 0; sleep 1; done
  echo "WAITFOR-TIMEOUT '$1' ${2}s" | tee -a $EV/steps.log; return 1
}
fresh() { # fresh <3store|1store|empty> : reseed scratch basket, cold start, enter Grocery + Basket
  $S/seed.sh "$1" >> $EV/steps.log 2>&1
  mark
  [ -n "$PRE_LAUNCH" ] && eval "$PRE_LAUNCH"
  local pk; case $VAR in tip) pk=$PKG_tip;; base) pk=$PKG_base;; esac
  adb -s $DEV shell am force-stop $pk; sleep 1
  adb -s $DEV shell monkey -p $pk -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
  waitfor "Grocery, " 10 && ui_tap "Grocery, " >/dev/null 2>&1
  waitfor "Basket" 30; sleep 3
  ui_tap "Basket" --exact >/dev/null 2>&1
  if [ "$1" != empty ]; then waitfor "Remove " 25 ; fi; sleep 2
}
rowswipe() { # rowswipe <item> <left|right> : horizontal drag across the row card (opens the Slidable pane)
  local b; b=$(nodes | python3 -c "
import sys,re
name=sys.argv[1]
for l in sys.stdin:
    m=re.search(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if m and m.group(5).startswith(name+'\\\\n'):
        x0,y0,x1,y1=map(int,m.groups()[:4]); print(x0,y0,x1,y1); break
" "$1")
  [ -z "$b" ] && { echo "ROWSWIPE-MISS $1" | tee -a $EV/steps.log; return 1; }
  set -- "$1" "$2" $b
  local cy=$(( ($4+$6)/2 )) xa xb
  if [ "$2" = left ]; then xa=$(( $5-150 )); xb=$(( $3+150 )); else xa=$(( $3+150 )); xb=$(( $5-150 )); fi
  echo "rowswipe '$1' $2 y=$cy $xa->$xb [$(date +%H:%M:%S)]" >> $EV/steps.log
  adb -s $DEV shell input swipe $xa $cy $xb $cy 350
}
rowdelete() { # open the Slidable end pane on <item> and tap its delete action (position derived from the row bounds)
  local b; b=$(nodes | python3 -c "
import sys,re
name=sys.argv[1]
for l in sys.stdin:
    m=re.search(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if m and m.group(5).startswith(name+'\\\\n'):
        x0,y0,x1,y1=map(int,m.groups()[:4]); print(x1-110,(y0+y1)//2); break
" "$1")
  [ -z "$b" ] && { echo "ROWDELETE-MISS $1" | tee -a $EV/steps.log; return 1; }
  echo "rowdelete-tap '$1' -> $b [$(date +%H:%M:%S)]" >> $EV/steps.log
  adb -s $DEV shell input tap $b
}
step() { # step <tag> : settle then immediate+settled snaps of the current state, with request log
  local tag="$1"; w 0.4; snap "$tag-a"; w 2.4; snap "$tag-b"; reqlog "$tag"
}

login_emily() {
  ui_tap "Email/Phone" --exact >/dev/null 2>&1; sleep 1; adb -s $DEV shell input text "<seeded-test-email>"
  ui_tap "Password" --exact >/dev/null 2>&1; sleep 1; adb -s $DEV shell input text "<seeded-test-password>"
  adb -s $DEV shell input keyevent KEYCODE_BACK; sleep 1
  ui_tap "Sign In" --exact >/dev/null 2>&1; sleep 8
}
settle() { # settle [quiet s] [max s] : wait until the backend access log is quiet
  local q=${1:-2} max=${2:-14} end last cur qs
  end=$((SECONDS+max)); last=$(wc -l < $S/access.log); qs=$SECONDS
  while [ $SECONDS -lt $end ]; do
    cur=$(wc -l < $S/access.log)
    if [ "$cur" != "$last" ]; then last=$cur; qs=$SECONDS; fi
    [ $((SECONDS-qs)) -ge $q ] && return 0
    sleep 0.5
  done
  echo "SETTLE-MAX ${max}s" >> $EV/steps.log; return 1
}
reveal() { # reveal <item> <button> : scroll (from the top) until the row's button is on screen
  local xy tries=0
  scroll_top
  while :; do
    xy=$(rowbtn_xy "$1" "$2")
    case "$xy" in NOROW|NOBTN|OFFSCREEN) tries=$((tries+1)); [ $tries -gt 10 ] && { echo "REVEAL-MISS $1" | tee -a $EV/steps.log; return 1; }; swipe_rel 0.22; sleep 1.2;; *) return 0;; esac
  done
}
revealL() { # revealL <exact label> : scroll from the top until the label's node centre is inside the list viewport
  local tries=0 y
  scroll_top
  while :; do
    y=$(nodes | python3 -c "
import sys,re
for l in sys.stdin:
    m=re.search(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if m and m.group(5)==sys.argv[1]:
        cy=(int(m.group(2))+int(m.group(4)))//2
        print(cy if 400<=cy<=2300 else 'OFF'); break
else: print('NONE')" "$1")
    case "$y" in OFF|NONE) tries=$((tries+1)); [ $tries -gt 10 ] && { echo "REVEALL-MISS $1" | tee -a $EV/steps.log; return 1; }; swipe_rel 0.22; sleep 1.2;; *) return 0;; esac
  done
}
tap_near() { # tap_near <anchor label> <button exact label> : tap the button node whose centre is vertically closest to the anchor node's centre
  local xy; xy=$(nodes | python3 -c "
import sys,re
anc=sys.argv[1]; btn=sys.argv[2]; A=None; B=[]
for l in sys.stdin:
    m=re.search(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label=\"(.*)\"',l)
    if not m: continue
    x0,y0,x1,y1=map(int,m.groups()[:4]); lab=m.group(5)
    if lab==anc and A is None: A=(y0+y1)//2
    if lab==btn: B.append(((x0+x1)//2,(y0+y1)//2))
if A is None or not B: print('NONE'); sys.exit()
B.sort(key=lambda p:abs(p[1]-A)); print(B[0][0],B[0][1])
" "$1" "$2")
  [ "$xy" = NONE ] && { echo "TAPNEAR-MISS '$1' '$2'" | tee -a $EV/steps.log; return 1; }
  echo "tap_near '$1' -> '$2' at $xy [$(date +%H:%M:%S)]" >> $EV/steps.log
  adb -s $DEV shell input tap $xy
}

rowburst_h() { # rowburst_h <item> <button> <count> : <count> taps at human pace (~250 ms), xy read once (adb 70 ms bursts lose ~15% of taps on BOTH builds, step 3)
  local xy; xy=$(rowbtn_xy "$1" "$2")
  case "$xy" in NOROW|NOBTN|OFFSCREEN) echo "ROWBURSTH-MISS $1 ($xy)" | tee -a $EV/steps.log; return 1;; esac
  echo "rowburst_h '$1' '$2' x$3 -> $xy [$(date +%H:%M:%S)]" >> $EV/steps.log
  for i in $(seq $3); do adb -s $DEV shell input tap $xy; sleep 0.15; done
}
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
  adb -s $DEV shell "input swipe $xa $cy $xb $cy 350; sleep 0.8; input tap $xt $cy"
}
nsnap() { ls $EV/*.txt 2>/dev/null | grep -vc 'steps\|requests\|errs'; }
