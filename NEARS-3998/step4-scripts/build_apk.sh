#!/bin/bash
# usage: build_apk.sh <UserApp dir> <label> <outapk>
APP="$1"; LABEL="$2"; OUT="$3"
S=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa
unset NEARS_PKG_SUFFIX
cd "$APP" || exit 9
echo "HEAD $(git rev-parse HEAD)  status: $(git status --short | wc -l)" > $S/apk/$LABEL.build.log
python3 ~/.nears/bin/mem-guard.py --label "NEARS-3998-s4-qa-build-$LABEL" --max-gb 6 --wait-s 3600 -- /Users/Apple/Tools/flutter/bin/flutter build apk --debug --target-platform android-arm64 --dart-define API_HOST=10.0.2.2:8235 >> $S/apk/$LABEL.build.log 2>&1
rc=$?
echo "BUILD_RC=$rc" >> $S/apk/$LABEL.build.log
[ $rc -eq 0 ] && cp build/app/outputs/flutter-apk/app-debug.apk "$OUT"
echo "HEAD-after $(git rev-parse HEAD)  status: $(git status --short | wc -l)" >> $S/apk/$LABEL.build.log
echo DONE >> $S/apk/$LABEL.build.log
