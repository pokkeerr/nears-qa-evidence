# NEARS-2515 QA — fix-cycle 0 (first pass)

**Verdict: BLOCKED** — no device surface reachable this pass. No AC demonstrated. No task_bugs/regression_bugs raised (nothing about the fix observed, good or bad).

Build under test: worktree `/Users/Apple/Projects/nears-NEARS-2515-cart-add-timeout-orphan`,
branch `fix/NEARS-2515-cart-add-timeout-orphan`, HEAD `f3dc0271` (code review PASS sha).
Backend: primary tree `php artisan serve --port=8000`, confirmed live (`200` on `/api/v1/config`),
real local baseUrl (not demo server).

## Android — pool capacity-exhausted
`adb devices -l`: 8 AVDs online.
- 6 genuinely occupied by other live foreign sessions (`qa_lock_check` verdict=occupied,
  confirmed via live host dart/adb driver pids attached — not residue): emulator-5554/5556/5558/5562/5564/5568.
- 2 lock-free: emulator-5560 (608MB free /data), emulator-5566 (712MB free /data) — both below
  the 800MB disk-precheck floor. `qa_disk_reclaim --clean` run once per device per protocol:
  no change either side (712->712, 608->608; dumpsys couldn't report cache size).
- `emulator -list-avds` == the 8 already booted — no spare AVD to promote.
- Re-surveyed after ~2min wait: unchanged.
- Whole platform pool low-disk/locked -> BLOCKED per profile carve-out. Never mkdir'd a lock on
  either disk-gated candidate.

## iOS — fallback attempted, pre-existing infra blocker (pool-wide, not this ticket)
Free simulator: iPhone 17 Pro, UDID 53F3807C-3BF6-46ED-8487-DEC957036BAA. Lock acquired
(`qa_lock_acquire ... NEARS-2515`, pid 50695 anchor), then released clean after failure.
`flutter run -d <udid>` -> `pod install` failure: firebase_analytics pub resolves to
FirebaseAnalytics 12.14.0, `ios/Podfile.lock` pinned 12.12.0. `pod install --repo-update`
(bounded run) fails identically; confirmed `git status` clean on UserApp/ios after (no
Podfile.lock mutation left behind). Cross-checked PRIMARY tree: identical Podfile.lock +
pubspec.lock state (12.12.0 / same unresolved pin) -- confirms this predates and is unrelated
to this ticket's diff (cart_controller.dart only). Did not touch Podfile.lock (outside QA write
remit).

## Disposition
- AC1-4: unverifiable this pass, pending device availability -- not a code defect.
- Automated backstop not independently re-run (no toolchain surface reachable); engineer's
  phase-6 `flutter test` (cart suite 167/167, full suite green) stands as the only test evidence,
  explicitly insufficient alone for PASS per project policy.
- Posted BLOCKED QA-evidence comment: NEARS-2515#15737.
- No evidence gallery this pass (zero screenshots/logs captured -- nothing ran).
