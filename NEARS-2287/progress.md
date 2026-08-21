# NEARS-2287 QA progress (iOS Simulator, iPhone 17 Pro, iOS 26.5)

Device pool saturated at spawn (documented Android pool 5554/5556/5558 all
busy/locked; non-pool 5562/5564/5570 also busy with other lanes' flutter runs)
-- moved to the iOS Simulator arm per the platform's documented iOS support
(userapp-navigation-guide.md §8b). Build: UserApp debug, commit a2e4a3e0,
worktree /Users/Apple/Projects/nears-NEARS-2287-module-loading-error-state.
Backend: primary tree `Admin/` (php artisan serve :8000), routed through a
local QA rewriting proxy (127.0.0.1:8899, --dart-define=API_HOST override) so
loading/failure/empty responses on GET /api/v1/module could be staged
deterministically without touching the shared DB or the shared backend
process (other sessions' flutter runs share the same :8000 backend).

All 3 ACs are [behav]-tagged -> verified via the live Dart VM Service
semantics tree (ext.flutter.debugDumpSemanticsTreeInTraversalOrder) and app
logs, not screenshots (NEARS-567's [ui] gate does not fire for [behav] ACs).
Zone driven via Get.find<StoreRegistrationController>().setZoneIndex(n) /
.retryGetModules() over the VM Service `evaluate` RPC -- same production code
path the NSelect's onChange/NErrorRetry's onRetry invoke; used because the
zone-dropdown's overlay-tap pixel mapping was unreliable in this sim/window
config (module tile taps and the Pick-Location CTA DID resolve correctly by
tap; the zone NSelect trigger did not -- documented in the QA envelope).

## AC1 -- loading skeleton while fetch is in flight
delay:5 staged on the proxy, setZoneIndex(0) fired.
Tree (mid-flight): `[10.0, 1382.0, 362.0, 1427.0]  'Loading modules'`
-> NSkeleton(semanticLabel: 'loading_modules'.tr) confirmed live.
Logs: `[NET] GET endpoint=/api/v1/module` ... `http_status=200` (delayed, no [FAIL]/[ERR]).
PASS.

## AC2 -- retry-capable error state + retry re-fetches the SAME zone
proxy state `fail` (599), setZoneIndex(0) fired.
Tree: `"Couldn't load modules"` title + `'Retry'` button (NErrorRetry).
Log: `[FAIL] endpoint=/api/v1/module http_status=599 type=ApiFailure msg="store registration modules fetch failed"`
Retry (still failing): 2nd 599 + 2nd identical [FAIL] line, same zone_id=1 (proxy access log).
Retry (proxy flipped to passthrough): resolved clean, `loading=false failed=false modules=5`,
tree shows `Select Module` / `Select Module Type` -- error state fully cleared, NSelect populated.
PASS.

## AC3 -- resolved-empty zone still renders static text (regression control)
proxy state `empty` (200, body []), setZoneIndex(0) fired.
Tree: `'Not Available Module'` (unchanged static Container), no NSkeleton/NErrorRetry.
Controller: `loading=false failed=false modules=0`. No new [FAIL] logged (this is
a clean success, not a failure). PASS.

## Extra QA points
- Rapid re-pick mid-fetch (G1 live spot-check): delay:4 staged, setZoneIndex(0)
  fired, then setZoneIndex(1) fired immediately (proxy back to passthrough).
  Landed state: `zoneIdx=1 loading=false failed=false modules=4` (Abu Dhabi
  Zone). After the stale delayed zone[0] response later arrived (confirmed via
  proxy access log), state was STILL `zoneIdx=1 modules=4` -- the
  `_moduleRequest` stale-response guard held live, no clobber.
- Busy-latch / double-fire guard: verified structurally -- NErrorRetry's own
  `_busy` flag (packages/nears_dls/lib/components/nerrorretry/n_error_retry.dart)
  latches synchronously before the first await and releases in a `finally`
  covering both success and error; getModules()'s existing `_moduleRequest`
  counter covers the stale-response race. Not independently re-derived live
  beyond the G1 check above (unit-covered: G2 test passes in
  store_registration_module_loading_error_test.dart).
- AR/RTL: `Get.updateLocale(Locale('ar','SA'))` forced live.
  Loading: `تحميل الوحدات`. Error: `تعذّر تحميل الوحدات` / `يرجى المحاولة مرة أخرى`
  / `أعد المحاولة`. Empty (regression): `الوحدة غير متوفرة` (unchanged key).
  All 4 render within the card's existing width bounds (max x=362, matching
  every other full-width field on the form) -- no clipping/overflow observed.
  Reverted to `Locale('en','US')` after.
- Other `moduleList` consumers (`custom_time_picker_widget.dart`,
  `select_location_view_widget.dart`): both gate on
  `selectedModuleIndex != -1`, untouched by this diff (confirmed by grep +
  solution doc's blast-radius section). Ran `selectModuleIndex(0)` live after
  a successful resolve -- no crash, no `ui_errors_ios` hit, app stayed stable.
- `[FAIL] endpoint=/api/v1/module ... type=ApiFailure` confirmed firing
  PII-safe (status + endpoint only, no body/URL) exactly on genuine failure,
  never on the empty-success path -- matches the logging-contract allow-list.

## Automated backstop
`flutter test test/features/auth/store_registration_module_loading_error_test.dart
test/features/auth/deliveryman_registration_repository_modules_failure_log_test.dart`
-> 15/15 pass.
`flutter test test/features/auth/` (full feature dir) -> 299/299 pass,
"All tests passed!".

## Regression sweep
`ui_errors_ios` clean throughout the session. No red screens, no GetX
exceptions, no overflow banners observed across English + Arabic passes.

## Environment notes / drift
- Documented Android QA pool (emulator-5554/5556/5558) was fully saturated at
  spawn (5554/5556 running other lanes' `flutter run`, 5558 legitimately
  locked by NEARS-2130, live pid). Non-pool 5562/5564/5570 also busy with
  other lanes. Moved to the iOS Simulator (iPhone 17 Pro,
  53F3807C-3BF6-46ED-8487-DEC957036BAA) per the profile's documented iOS
  support -- this is the SAME UDID the userapp-navigation-guide.md §8b pins
  as the standard iOS QA device.
- `scripts/qa-lock-guard.sh`'s probe enumerates ONLY `adb devices` -- it has
  no simctl/iOS awareness, so a normal `qa_lock_acquire <udid>` on a booted
  iOS simulator refuses with "NOT ATTACHED" even though the device genuinely
  is booted and free. Worked around with the documented `--no-probe` escape
  hatch (verified the UDID was freshly booted by me, not held by anyone,
  before using it). This is real drift from `.claude/workflow-profile.md`'s
  §"iOS: pin locks to simulator UDIDs" guidance -- the guidance describes an
  iOS locking contract the code-enforced guard does not implement. Flagged in
  the QA envelope `drift[]`.
- A separate, unrelated navigation quirk was observed on this iOS build: from
  a guest session with a GPS-derived (not saved-address-book) location, the
  customer Home module-select flow ("What are you shopping for?") repeatedly
  bounced back to the "Pick Location" map-confirm screen on every module-tile
  tap, even immediately after confirming the same location. Reproduced twice.
  This is on the CUSTOMER Home entry path, not the Store Registration screen
  NEARS-2287 touches, and was bypassed for this QA run via a direct
  `Get.toNamed('/store-registration')` VM-Service call (the same call
  `Get.toNamed` the real "Open Vendor" button performs). Root cause not
  diagnosed -- flagged as a followups[] regression-candidate, not filed as a
  bug of this ticket.
