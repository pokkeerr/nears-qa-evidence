# NEARS-1665 — QA [8] progress log

Device: `emulator-5558` (Android, Asia/Dubai, 1344x2992) · build installed 2026-08-07 10:49:34
APK: `UserApp/build/app/outputs/flutter-apk/app-debug.apk` sha256 `2c24fc011018ca319ae6…` (identical before + after every observation)
Backend: `php artisan serve` :8000, HTTP 200 · `adb reverse tcp:80 tcp:8000` set
Theme: light only (dark deferred).

Code provenance: `git diff 353261d9 d7dd8aef -- UserApp/ packages/` is EMPTY and the primary tree
has no uncommitted `UserApp/`/`packages/` changes, so the primary-tree build is byte-identical to
the NEARS-1665 worktree's Dart. NEARS-1665 changed zero Dart files.

| # | Observation | Result |
|---|---|---|
| 1 | Login `michael.brown@demo.com` (user 3), Profile shows "Michael Brown" | OK |
| 2 | Notification screen: 7 cards, 4 headers, correct order/buckets/glyphs | PASS (AC6) |
| 3 | Long-body (02 Aug) card clamps to 2 lines + ellipsis; detail sheet shows full body | OK |
| 4 | Runtime logs during AC6 — 0 `[ERR]`/`[FAIL]`/exception/RenderFlex over 565 log lines | clean |
| 5 | Regression: user 6 `customer@nears.com` notification list = `No notification found` | clean |
| 6 | DB footprint: marker `NEARS-1665/*` on ids 341-345 only; 339/340 unmarked/untouched | clean |
| 7 | `flutter test test/features/notification/` | 26/26 pass |
