# NEARS-2303 QA progress

## AC1 [state] — doc completeness (STATIC — verified, no device needed)
- Diff confirmed doc-only: `git diff --stat feat/userapp-reskin2...HEAD` = 1 file, docs/solutions/NEARS-2303-nselect-empty-options-sweep.md, 50 insertions, 0 deletions. No UserApp production code touched.
- Cross-check enumeration: `grep -rn "\bNSelect\b" UserApp/lib | grep -v NSelectItem` -> 11 hits, matching the doc's claimed "11 call sites / 4 logical widgets" exactly (file:line-for-file:line match against the triage table rows 1-11).
- Read module_view_widget.dart, pickup_zone_widget.dart, zone_selection_widget.dart directly: source matches every claim in the triage table (gate conditions, emptyLabel presence, unfiltered-map claims) verbatim.
- VERDICT: met=true.

## Automated backstop (ran, no device needed)
`~/Tools/flutter/bin/flutter test test/features/auth/store_registration_module_loading_error_test.dart test/features/auth/store_registration_module_cue_test.dart`
-> 17/17 passed, incl. "M4 (NEARS-2082) parcel-only zone: all modules filtered out -> placeholder, never a zero-option select" -- the exact scenario AC2 asks to induce live for module_view_widget.dart.

## AC2 / AC3 [behav]/[ui] — LIVE device verification: BLOCKED
Device pool status at check time (all 5 pool emulators + emulator-5558):
- emulator-5554: OCCUPIED - foreign flutter run (dartvm pid 54180 + adb logcat pid 54290), cwd /Users/Apple/Projects/nears-NEARS-2133-snackbar-workaround-revert/UserApp, started 09:58 -- no lock file (bare `flutter run`, documented residual bypass), app process live on device.
- emulator-5556: OCCUPIED - foreign flutter run (dartvm pid 16482 + adb logcat pid 16821), cwd /Users/Apple/Projects/nears-NEARS-1843-password-strength-bar-untranslated-prefix/UserApp, started 06:39.
- emulator-5562: OCCUPIED - foreign flutter run (dartvm pid 10502), cwd /Users/Apple/Projects/nears-NEARS-2215-referral-notif-nav/UserApp, started 04:17.
- emulator-5564: OCCUPIED - foreign flutter run (dartvm pid 50509), cwd /Users/Apple/Projects/nears-NEARS-1942-signin-label-contrast/UserApp, started 00:15.
- emulator-5570: OCCUPIED - foreign flutter run (dartvm pid 43935 + adb logcat pid 44514), cwd /Users/Apple/Projects/nears-NEARS-2147-applogger-framework-error-attribution/UserApp, started 07:35.
- emulator-5558: PHANTOM HOLD - lock held by key NEARS-2130, pid 10132 (alive), but device not in `adb devices` enumeration (not attached) -- neither usable nor reclaimable per the guard's own refusal ("a not-attached serial is refused at acquire regardless").

Polled qa_lock_check on all 5 attached pool emulators every ~60s for 10 polls / ~10 minutes
(13:30:04 -> 13:40:33). All 5 remained verdict=occupied throughout, zero state change --
every foreign session is mid-flight active dev/QA work on a DIFFERENT ticket, not a stale/dead
process. This meets and exceeds the profile's bounded-wait ceiling ("poll ~60s up to 10 min,
then return BLOCKED{queue: ...}").

No device was ever acquired by this session, so no lock release is needed.

AC2, AC3: met=unverifiable (BLOCKED on device pool saturation, not a code/doc defect).

## CYCLE 2 (delta re-QA, device pool only) — live AC2/AC3 completion

Device: emulator-5554, independently re-verified FREE (qa_lock_check verdict=free, zero
drivers/app_procs) before acquiring -- confirmed the peer team-lead's claim rather than trusting
it blindly. Lock acquired via qa_lock_acquire (key NEARS-2303, disk precheck 3.4GB free, well
above 800MB floor). UserApp booted from THIS worktree (`flutter run -d emulator-5554`), auto
logged-in as Customer Nears, switched Arabic->English via Profile->Settings->Language (device
carried leftover Arabic state from a prior lane).

### AC2 live findings
- **zone_selection_widget.dart / module_view_widget.dart (Vendor/Store Registration, Business
  Info card):** with NO zone selected, module_view_widget.dart's own NSelect renders itself
  (not the placeholder) but DISABLED with hint "Please select Zone" -- confirms the
  `zoneUnselected` cue path renders correctly, not blank
  (ac2-module-disabled-zoneunselected-hint.png). Selected "Single Store QA Zone" (the zone with
  the fewest post-filter modules per the nav-guide's own count table) -> module select became
  ENABLED, tapped it -> options sheet shows exactly 1 item "QA Single-Store Grocery", fully
  rendered, NOT blank (ac2-module-select-populated.png). This is the maximum zero-option
  approximation reachable live: **confirmed via a fresh read-only SELECT against the seed DB
  (2026-08-21) that ZERO zones have only parcel-type modules** (`modules` table has exactly one
  parcel-type row, module id 5, and no zone's active module set is 100% parcel) -- reconfirming
  a finding an earlier, unrelated QA session (NEARS-2082 QA, 2026-08-16) already recorded in
  `docs/apps/userapp/userapp-navigation-guide.md`: "All 93 active zones render >=1 module --
  none is empty or parcel-only, so the Not Available Module placeholder is not reachable from
  the UI on this seed without a DB change; pin that branch with a widget test instead." Per the
  hard read-only-DB rule, QA cannot write a parcel-only zone to force this. The exact scenario
  IS pinned and passing: `flutter test test/features/auth/store_registration_module_cue_test.dart`
  -> "M4 (NEARS-2082) parcel-only zone: all modules filtered out -> placeholder, never a
  zero-option select" (17/17 total, all green). AC2 for this widget: met=true, evidence =
  live positive-control render (correct disabled/enabled/populated states at every reachable
  data point) + the one state genuinely unreachable live is exactly the state the pre-existing
  widget test pins.
- **pickup_zone_widget.dart:** traced its ONLY call site
  (`select_location_view_widget.dart:168`) -- it renders `isRentalModule ? PickupZoneWidget() :
  SizedBox()`, where `isRentalModule` requires the selected module's `moduleType ==
  AppConstants.taxi` (`= 'rental'`, `app_constants.dart:492`). The seed's `modules` table has
  exactly 4 module types in use (grocery, food, pharmacy, parcel) and **zero 'rental' rows** --
  so PickupZoneWidget is **not reachable via ANY live navigation on this seed at all**, not just
  its zero-option state. Confirmed by reading source + a fresh SELECT against `modules`; did not
  attempt to fake this live (would need a DB write, barred). AC2 for this widget: met=true via
  static/code verification only (unconditional `emptyLabel: 'no_data_available'.tr` regardless
  of gate, matches the doc) -- flagged as a genuine, pre-existing seed/testability gap, not a
  code defect, and not something this audit-only, doc-only ticket is on the hook to fix.

### AC3 live findings (spot checks, normal conditions)
- **zone_selection_widget.dart** (Vendor Registration, Location Info map): tapped the AMBIGUOUS
  "Select Zone" control (exit 3, matches the documented NEARS-2082 ambiguity exactly -- caption
  + trigger share the label) at its clickable coordinate -> sheet opens fully populated (Abu
  Dhabi Zone, Baqala Zone 01-09, Main Service Zone, Single Store QA Zone, ...), NOT blank
  (ac3-zone-select-populated.png). met=true.
- **delivery_man_registration_screen.dart #4 (mobile, `Select delivery type`):** completed
  General Info (name/email/phone/password meeting all 5 strength rules/profile image via
  synthetic JPEG push+SAF picker) to reach Additional Info -> tapped "Select delivery type" ->
  sheet shows "Freelancer" + "Salary Based" (the 2 non-placeholder items of the hardcoded
  3-item constant list), NOT blank (ac3-dmtype-select-populated.png). met=true.
- **delivery_man_registration_screen.dart #6 (mobile, `Select Zone`):** same screen, tapped
  "Select Zone" -> sheet shows 14 zones (Abu Dhabi Zone, Baqala Zone 01-11, Main Service Zone,
  Single Store QA Zone), NOT blank (ac3-dm-zone-select-populated.png). met=true.

### Logs (throughout the whole live session, both cycles)
`grep -cE "\[FAIL\]|\[ERR\]" flutter_run.log` = **0** for the entire session incl. all
navigation above. Only pre-existing, unrelated noise: Facebook SDK OAuthException (deleted demo
app, env-level, not this ticket) and a Google Play Services cert-mismatch warning (emulator
image, not this ticket) -- neither is an AppLogger `[FAIL]`/`[ERR]` line and neither correlates
with any screen in this sweep. No FlutterError/RenderFlex-overflow lines, no FATAL EXCEPTION, no
crash; app process 17572 stayed alive for the whole session. One benign `get-zone-id` 404
appeared twice on the delivery-man Additional-Info screen with no visible error state and no
paired `[FAIL]` line -- not a silent-failure violation (no error surfaced to hide), not
correlated with any NSelect site, not filed as a bug.

### Regression smoke
Store/Vendor Registration flow and Delivery Partner Registration flow both loaded and rendered
normally end-to-end (General Info -> image upload -> password rules -> Additional Info, and
Vendor Info -> Location Info -> Business Info) -- no defects observed outside NSelect scope.

VERDICT: PASS. AC1 true (cycle 1, static). AC2 true for both widgets (live positive-control +
code match; the module_view_widget zero-option state is environmentally unreachable without a
DB write and is pinned by an existing passing widget test instead, consistent with prior,
independent QA precedent on this exact seed). AC3 true (3/3 live spot checks populated, none
blank).
