# sourced by: bash -c 'source walk.sh; ...'
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa
W=$S/walk
export ANDROID_SERIAL=emulator-5554
PKG=com.izzes.nears
source /Users/Apple/Projects/nears-NEARS-3998-u7-step4-zone-resolution/scripts/app-nav/uinav.sh
mark() { # mark <build> <step> <start|end>
  adb -s $ANDROID_SERIAL shell "log -p i -t QAWALK $1__$2__$3" ; curl -s "http://127.0.0.1:8235/__mark?name=$1__$2__$3" >/dev/null; }
logstart() { # logstart <build>
  adb -s $ANDROID_SERIAL logcat -v threadtime -T 1 > $W/$1_logcat.txt 2>&1 &
  echo $! > $W/$1_logcat.pid; echo "logcat pid $(cat $W/$1_logcat.pid)"; }
logstop() { [ -f $W/$1_logcat.pid ] && kill $(cat $W/$1_logcat.pid) 2>/dev/null; rm -f $W/$1_logcat.pid; }
geo() { adb -s $ANDROID_SERIAL emu geo fix "$1" "$2"; }   # lng lat
dump() { # dump <build> <step> : labels of the current screen -> file
  ui_list > $W/$1_$2_labels.txt 2>/dev/null; wc -l < $W/$1_$2_labels.txt; }
