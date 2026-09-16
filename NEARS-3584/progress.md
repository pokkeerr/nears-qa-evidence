# NEARS-3584 QA progress checkpoint

## Environment
- Worktree: /Users/Apple/Projects/nears-NEARS-3584-module-picker-landing, branch feat/NEARS-3584-module-picker-landing, HEAD 569a345c9
- Backend: own php artisan serve on port 8010 from this worktree's Admin/ (freshness-check PASS)
- Device: emulator-5554, lock held (NEARS-3584)
- Env gap found: worktree has no UserApp/android/app/google-services.json (gitignored, not copied on worktree creation) -> Firebase.initializeApp() fails -> later configureFirebaseMessaging() (pre-existing code, untouched by this diff, location_controller.dart:1102) throws UNCAUGHT and silently blocks the whole post-zone-resolve navigation chain (app stuck on pick-location map screen forever, no further log lines). This is the known class of gap already logged in docs/data-qa/verification-checks.md ("no google-services.json client for the derived suffix", NEARS-3429) -- pre-existing, not part of this ticket's diff.
- Workaround (matches NEARS-3429's documented workaround): bypass qa-run.sh's worktree package-suffixing for this run; bare `flutter run -d emulator-5554 --dart-define API_HOST=10.0.2.2:8010` from this worktree's UserApp/ (base package com.izzes.nears, matches primary tree's google-services.json). Device lock already held via qa_lock_acquire before this launch, so exclusivity preserved independently of qa-run.sh's own check (identical rationale to NEARS-3429).
