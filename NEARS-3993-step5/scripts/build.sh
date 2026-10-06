#!/bin/bash
Q=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s5/qa
PORT=8593
F=/Users/Apple/Tools/flutter/bin/flutter
for v in tip base; do
  W=$Q/$v; SUF=nears_3993_s5_qa_$v
  echo "=== $v start $(date +%T) suffix=$SUF" >> $Q/build.progress
  ( cd $W/UserApp && python3 ~/.nears/bin/mem-guard.py --label NEARS-3993-s5-qa-pubget-$v --max-gb 6 --wait-s 3600 -- $F pub get ) > $Q/pubget-$v.log 2>&1
  echo "pubget $v rc=$? $(date +%T)" >> $Q/build.progress
  ( cd $W/UserApp && export NEARS_PKG_SUFFIX=$SUF && python3 ~/.nears/bin/mem-guard.py --label NEARS-3993-s5-qa-build-$v --max-gb 9 --wait-s 3600 -- $F build apk --debug --dart-define=API_HOST=10.0.2.2:$PORT ) > $Q/build-$v.log 2>&1
  echo "=== $v rc=$? $(date +%T)" >> $Q/build.progress
  cp $W/UserApp/build/app/outputs/flutter-apk/app-debug.apk $Q/app-$v.apk 2>>$Q/build.progress
done
echo ALLDONE >> $Q/build.progress
