# NEARS-3529 QA progress

Device: emulator-5554 (Pixel_10_Pro AVD, google_apis_playstore_ps16k), worktree nears-NEARS-3529-campaign-null-date-crash
Login: demo.store@gmail.com (vendor id 1, store 1 "Nears Mart", module 1) — already-logged-in session found on cold boot.

- Pre-flight: had to copy VendorApp/android/app/google-services.json from primary tree into worktree
  (gitignored, absent from fresh worktree -> app crashed full-red-screen at boot on
  `Get.find<AnalyticsService>().observer` inside GetMaterialApp navigatorObservers,
  `[core/no-app]`). Confirmed pre-existing/unrelated to this ticket's diff (NEARS-2964 reverted
  NEARS-968's inline-FirebaseOptions resilience fix back to google-services.json-only). Flagged
  as regression_bugs + drift, not a task_bug of NEARS-3529.
- AC1 PASS: Menu > Campaign renders both seeded rows (QA Single-Store Campaign A, B), no crash,
  no blank/frozen screen. Logs clean (ui_errors: 0 matches).
- AC2 PASS: neither row shows a date/date-icon (both campaigns.start_date NULL) - confirms hide-on-null.
  Screenshot: ac1-ac2-campaign-list.png
