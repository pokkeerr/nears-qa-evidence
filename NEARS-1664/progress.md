# NEARS-1664 — live QA gate [8], fix_cycle 0

- **Build under test:** worktree `/Users/Apple/Projects/nears-NEARS-1664-support-empty-contact`,
  branch `feat/NEARS-1664-support-empty-contact` @ `34058e92` (rebased on `feat/userapp-reskin2` @ `60dc1bc6`).
- **Device:** `emulator-5558` (Android, 1344x2992 @ 3.0 → 448x997dp). Lock held for NEARS-1664.
  Disk reclaimed to 959MB free before install (uninstalled own package only); 800MB floor PASS.
- **APK identity (before AND after every observation):** installed `base.apk` md5
  `2c1ecfb3fdafdbf04dd8570ddb26b2a8` == worktree `build/app/outputs/flutter-apk/app-debug.apk` md5.
- **Backend:** local `php artisan serve` :8000, `/api/v1/config` HTTP 200. `baseUrl` = `http://10.0.2.2:8000` (real local BE).
- **Seeded config (read-only SELECT):** address `Abu Dhabi` · phone `+971565811159` · email `admin@admin.com` — all three present.
- **Theme:** light only (dark deferred per reskin policy).

| AC | Result | Evidence | Logs |
|---|---|---|---|
| AC1 (all-missing → NEmptyState) | not live-observed — widget-test-only | needs a DB write to `business_settings` (forbidden) | n/a |
| AC2 (per-row hide on null/empty/blank) | not live-observed — widget-test-only | same | n/a |
| AC3 (3 rows, order, gaps, hero disc, section header) | PASS | `ac3-support-ltr-three-rows.png`; row bounds y 906/1152/1398, 30px(=10dp) gaps, order Address→Call→Email | clean (0 [ERR]/[FAIL]) |
| AC4 (Call → dialer, Email → composer, can_not_launch unchanged) | PASS | `ac4-call-dialer.png`, `ac4-cannot-launch-snackbar.png`, `ac4-launch-intents.log` | 2 [ERR] — both the deliberately fault-injected can_not_launch taps, correctly paired with the snackbar |
| AC5 (RTL mirror, digits unreversed) | PASS | `ac5-support-rtl-arabic.png`, `ac5-chevron-ltr-vs-rtl-zoom.png` | clean |

Regression sweep (5 surfaces): Help & Support en/ar/es · Profile menu · Settings + Language picker.
Automated backstop: `flutter test test/features/support/support_screen_render_test.dart` → 20/20 pass.
