S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa
W=$S/walk
export ANDROID_SERIAL=emulator-5556
PKG=com.izzes.nears
source /Users/Apple/Projects/nears-NEARS-3998-u7-step5-suggestions/scripts/app-nav/uinav.sh
mark() { adb -s $ANDROID_SERIAL shell "log -p i -t QAWALK $1__$2__$3"; curl -s "http://127.0.0.1:8335/__mark?name=$1__$2__$3" >/dev/null; }
logstart() { adb -s $ANDROID_SERIAL logcat -v threadtime -T 1 > $W/$1_logcat.txt 2>&1 & echo $! > $W/$1_logcat.pid; }
logstop() { [ -f $W/$1_logcat.pid ] && kill $(cat $W/$1_logcat.pid) 2>/dev/null; rm -f $W/$1_logcat.pid; }
