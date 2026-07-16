# NEARS-1137 — QA pass 1 (full), light mode, English/LTR

Worktree: /Users/Apple/Projects/nears-NEARS-1137-autoopened-precedence (base feat/human-review@67867bdb)
Diff: UserApp/lib/features/home/widgets/single_store_hero_view.dart (+1 field) and its test only.
route_helper.dart, store_screen.dart, store_load_failure_view.dart are byte-for-byte UNTOUCHED.

## Environment note (read before the AC table)
Live device verification for AC1/AC2 was blocked by two independent, confirmed-external causes,
NOT a defect in this diff:
1. Host-wide resource contention: load avg peaked at 102.95 (from ~10 baseline), <350MB free RAM,
   /proc/pressure/io avg10=57-65%. Produced repeated real ANRs (`Input dispatching timed out
   (Application does not have a focused window)`, confirmed via `ActivityManager` logcat) on
   every app-launch attempt across multiple retries.
2. Device-pool contention: emulator-5556 was mid-QA for NEARS-802 (later a dead-pid lock,
   legitimately reclaimed), then had an ACTIVE, concurrent VendorApp session repeatedly stealing
   foreground / killing com.izzes.nears without ever touching the QA lock file — filed separately
   by the conductor as an infra bug. emulator-5554/5558 were both below the 500MB free-disk floor
   throughout (485MB / 339MB). emulator-5562 is not in the documented pool (dedicated DeliveryApp
   device, confirmed mid-session).

## AC1 + AC2 (hero-tap path: StoreLoadFailureView "Back to Home" link + PopScope auto-escape)
**Structurally unreachable live for this fixture, independent of the above contention.**
`SingleStoreHeroView` only renders on `home_screen.dart` when `ModuleController.isSingleStoreZone`
(whole zone has exactly 1 module). The SAME predicate is what makes `DestinationResolver`'s
`directStore` tier fire on every cold-boot / address-switch into this zone, which navigates
STRAIGHT into StoreScreen and never renders `home_screen.dart` at all — confirmed live (see AC3
below): switching to the Tower A / zone-3 fixture address never showed the hero card, it landed
directly in the store. This is the same wall NEARS-1098's own QA hit for this exact widget (its
progress.md documents cold-deep-link ACs live but backs the hero-specific claim with code-reading
+ the widget-test mutation-pin, not a live tap-through: docs/qa-evidence/NEARS-1098/progress.md
line 26, docs/qa-evidence/NEARS-1098/bug-autoopened-flag-dead-on-hero-path.log).

Evidence accepted instead (team-lead sign-off):
- **Static code read**: `route_helper.dart:1529` — `Get.arguments ?? StoreScreen(...)`; a non-null
  `arguments:` object always wins over the parsed `auto_opened` query param. Pre-fix,
  `single_store_hero_view.dart:145` passed `StoreScreen(store: store, fromModule: true)` with
  `autoOpened` defaulting false, permanently nullifying it on this path. Post-fix it passes
  `StoreScreen(store: store, fromModule: true, autoOpened: true)`. Both AC1 (`StoreLoadFailureView
  ._stranded` at store_load_failure_view.dart:29-32) and AC2 (`StoreScreen`'s `PopScope` branch at
  store_screen.dart:183/329) key off `widget.autoOpened`, so this single-field fix is the complete
  closure for both.
- **Automated, falsifiable**: `flutter test test/features/home/single_store_hero_view_test.dart` —
  5/5 PASS, including the new pin added by this diff asserting `Get.arguments` is a `StoreScreen`
  with `autoOpened: true` after the hero CTA tap. Reverting only the widget line to the pre-fix
  form (drop `autoOpened: true`) turns this pin RED (mutation-checked, not green-but-blind).
- **Broader regression sweep**: `flutter test test/features/home/ test/features/store/` — 271/271
  PASS (one pre-existing RTL `campaign_screen.dart` overflow render-warning, not a failure, tracked
  separately from this ticket).

## AC3 (regression: deep-link + splash-boot paths still pass autoOpened correctly)
**LIVE PASS.** Logged in as qa.singlestore@nears.com (seeded NEARS-257 QA fixture), switched the
active address to "Tower A, Single Store QA Zone" (zone 3, store id 59
nears-257-fixture-store). This exercises `DestinationResolver.navigateToStore`
(destination_resolver.dart — untouched by this diff), which navigated directly into StoreScreen.
Observed live (accessibility-tree text, no screenshot needed):
- "Showing the only store near you" banner rendered (`only_store_near_j).tr`, store_screen.dart:2262)
  — only mounts when `widget.autoOpened == true`, so autoOpened was NOT nullified on this path.
- `[NET] endpoint=/api/v1/stores/details/59 http_status=200` and `[INFO] msg="location:
  inZone=true"` in the app log — clean, no `[FAIL]`/`[ERR]`.
Confirms the untouched deep-link/splash-boot call site is unaffected by this change, as expected
(route_helper.dart and destination_resolver.dart are both byte-for-byte unchanged by this diff).

## Verdict: PASS
AC1/AC2 via static code review + mutation-checked automated test (team-lead accepted this fallback
given the confirmed structural-unreachability + infra-contention combination, consistent with
NEARS-1098 precedent). AC3 live PASS. Regression: clean (271/271 automated, zero unrelated log
errors observed). No task_bugs, no regression_bugs found in this diff.
