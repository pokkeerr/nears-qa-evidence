# NEARS-3464 QA progress checkpoint

- Device: emulator-5558 (wave56) rejected for GPS/geo-fix instrumentation (known pool issue per nav-guide §5.11 gotcha area / memory lesson "pick-map-camera-idle-qa-instruments" — get-zone-id 404'd after geo fix despite direct backend curl confirming zone-1 match for the same coords). Switched to emulator-5566.
- Backend: shared primary-tree `php artisan serve` on :8000 (Admin/ in /Users/Apple/Projects/nears), confirmed 200 + zone-1 lookup working directly.
- Unit backstop: `flutter test test/features/store/store_details_get_notify_test.dart` — 3/3 PASS (cached-data notify, fresh-fetch pre-await notify, terminal finally exactly-once regression).
- Review lessons: 68 active selected; most relevant to this fix: `getx-retry-missing-preawait-notify` (this IS the exact bug class fixed), `isloading-flag-omitted-try-catch-sibling-methods`, `stale-async-writeback-seals-new-session`.
