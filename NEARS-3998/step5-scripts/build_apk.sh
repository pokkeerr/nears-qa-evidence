#!/bin/bash
# usage: build_apk.sh <label base|tip>
L=$1; S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa; APP=$S/wt/$L/UserApp
unset NEARS_PKG_SUFFIX
cd "$APP" || exit 9
LOG=$S/apk/$L.build.log
echo "HEAD $(git rev-parse HEAD)  status: $(git status --short | wc -l)" > $LOG
/Users/Apple/Tools/flutter/bin/flutter pub get >> $LOG 2>&1
python3 ~/.nears/bin/mem-guard.py --label "NEARS-3998-s5-qa-build-$L" --max-gb 6 --wait-s 3600 -- /Users/Apple/Tools/flutter/bin/flutter build apk --debug --target-platform android-arm64 --dart-define API_HOST=10.0.2.2:8335 >> $LOG 2>&1
rc=$?
echo "BUILD_RC=$rc" >> $LOG
[ $rc -eq 0 ] && cp build/app/outputs/flutter-apk/app-debug.apk $S/apk/$L.apk
echo "HEAD-after $(git rev-parse HEAD)  status: $(git status --short | wc -l)" >> $LOG
echo DONE >> $LOG
