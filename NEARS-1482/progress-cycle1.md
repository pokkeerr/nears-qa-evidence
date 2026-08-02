# NEARS-1482 — DELTA re-QA (fix cycle 1)

Build: worktree `nears-NEARS-1482-shared-state-widgets` @ `c7fc3d2f`
APK md5 `97e3829f7fd30727c54314092e27e7e1` — verified identical on device (`pm path` + `md5sum`).
Device: emulator-5554 (Android, light mode). Backend: local `php artisan serve` :8000, `baseUrl=http://10.0.2.2:8000`.

| # | AC | Result | Evidence |
|---|----|--------|----------|
| AC3 | offline retry gives visible feedback (default path) | PASS | `ac3-offline-retry-toast-en.png`; `[ERR] msg="error snackbar shown"`; 0 assertions |
| AC4 | Arabic RTL toast | PASS | `ac4-offline-retry-toast-ar-rtl.png`; glyph mirrored right; swipe-dismiss proven vs control |
| AC3e | splash onRetry override shows NO toast | PASS | `[FAIL] endpoint=/api/v1/config` re-fetch, no snackbar breadcrumb |
| reg | online retry navigates, no toast | PASS | landed home, 0 toast nodes |
| reg | isRetrying hides CTA + NSpinner | PASS | `regress-splash-isretrying.png` |
| reg | AC2 glyphs | PASS (spot) | `Symbols.wifi_off` live in en + ar |

Automated: `flutter test no_internet_screen_test.dart no_data_screen_test.dart` -> 14/14 pass.

Offline was genuine airplane mode: `airplane_mode_on=1`, active default network `none`,
`ping 10.0.2.2 -> Network is unreachable`; airplane glyph visible in every shot's status bar.
