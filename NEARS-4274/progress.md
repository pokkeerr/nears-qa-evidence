# NEARS-4274 [8] QA progress (iOS simulator replay)

Build feff407b0 (feat/NEARS-4274-maestro-ios). iPhone 17 AEE5A54D-5DF0-48B5-A3B0-7ABF14136136, iOS 27.0, Xcode 27.0 (27A266a), Maestro 2.11.0, Flutter 3.41.9.
Backend: /Users/Apple/Projects/nears-NEARS-4274-maestro-ios @ feff407b0 (port 8274, DB clone multi_food_db_qa4274, dropped at end).

- AC1 FAIL - official run 1 (maestro/20261020-230004-59642): rc 1, 0/5 flows; every flow stops at "Use my current location" because the app shows "No internet connection". Gate DIRTY (LocationNoInternetAbort, ZoneOverlayViewportQueryFailure).
  - Exploration 1 (scratch flow copy, iOS-only Try Again workaround; maestro/20261020-231222-51597): 1/5, next stop is "Sign In" hidden by the keyboard (hideKeyboard is a no-op on iOS).
  - Exploration 2 (+ iOS-only tap "done"; maestro/20261020-231933-3191): 3/5 (02, 03, 04 PASS). 01: the Login/Sign Up sheet tap did not open login. 05: "No internet connection" again mid-flow. Gate DIRTY (UncaughtAsyncError FirebaseException apns-token-not-set x22).
  - Runs 2 and 3 not attempted: run 1 failed deterministically.
- AC2 PASS - live: a second wrapper run started while run 1 held maestro-ios-host (app not yet running) was refused with rc 2, naming pid 59642 (ac2-live-demo.log). Run 1 was not disturbed. The device-free suite qa-maestro-run.ios.test.sh ran 198/198.
- AC3 PASS - qa-maestro-run.test.sh 277/277, nightly 335/335, lock-guard 497, 11 scripts/qa-maestro suites PASS, flow-edit-check PASS; frozen-file three-dot diff empty; fresh-login.yaml has only added lines.
