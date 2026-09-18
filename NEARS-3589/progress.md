# NEARS-3589 QA progress checkpoint

Device: emulator-5558 (sdk_gphone16k_arm64), UserApp debug, worktree
`/Users/Apple/Projects/nears-NEARS-3589-basket-uiux-findings`, branch
`feat/NEARS-3589-basket-uiux-findings`, HEAD df37e6767.
Backend: own `php artisan serve --port=8210` from this worktree (freshness-check PASS).
Account: customer@nears.com. Location: mocked Abu Dhabi (cmd location test-provider,
24.4539,54.3773). 2-store basket confirmed live (Fresh supermarket store 13 items
Dish Soap 500ml + Whole Milk 1L; Fresh local store 12 item Honey 500g — matches
NEARS-3590 fixture set, seed data carries accumulated quantities from prior QA runs).

## Source-verified (before device drive)
All 10 findings + AC-DLS/SHARED/ANALYTICS/LOG confirmed present in the diff
(3fc8ae4c3..HEAD) by reading the implementing lines directly — see full envelope.

## Environment bootstrap notes (not ticket defects)
- Fresh worktree needed: `Admin/.env` copy, `composer install`, `php artisan passport:keys`,
  `worktree-bootstrap-images.sh`.
- `UserApp/android/app/google-services.json` absent in worktree (gitignored) — copied from
  primary, then a second `client[]` entry added for the worktree-suffixed package id
  (`com.izzes.nears.nears_nears_3589_basket_uiux_findings`) so `Firebase.initializeApp()`
  and the `processDebugGoogleServices` Gradle task succeed for a per-worktree-suffixed
  UserApp build. Local, gitignored, not a product-code change.
- Google Maps SDK shows "Authorization failure" for the same suffixed package
  (API key not registered for this cert+package combo) — map tile rendering only;
  does not block the geocode/zone REST flow. Unrelated to this ticket, not filed
  (pre-existing infra gap affecting every worktree-suffixed UserApp build, not specific
  to NEARS-3589).
- Location mocking needed `cmd location providers add-test-provider gps` +
  `set-test-provider-location`, not `adb emu geo fix` (per pick-map-camera-idle memory).

## AC-by-AC status (live)
(being filled in as each is demonstrated)
