# NEARS-1753 — live QA evidence log

**Verdict: FAIL** (one task-bug, `breaks_ac: true`, on AC5).

## Build under test
- Worktree `/Users/Apple/Projects/nears-NEARS-1753-existing-user-sheet`, branch
  `feat/NEARS-1753-existing-user-sheet`, `reviewed_sha` `fb2f27da`, tree clean.
- SDK `/Users/Apple/Tools/flutter` (pinned). Device `emulator-5554`, 1344x2992 @ density 480
  = **448x997 dp** (already the baseline geometry — no `wm size` override needed).
- Device clock measured **49 s behind the host** at acquisition; all logcat/proxy timestamp
  joins below account for it.
- Free `/data` at acquisition: 855 644 KB (835 MB) — above the 800 MB floor.
  `emulator-5556` measured 760 272 KB (742 MB) → **below floor, skipped, not locked**.

## Freshness (behavioural, not file-level)
Each build was pointed at a **session-unique proxy port** that only that build's
`--dart-define` can produce:
- pre-fix (base `fda1b44c`) → `API_HOST=10.0.2.2:8151`
- fix (`fb2f27da`) → `API_HOST=10.0.2.2:8152`

Port 8151 traffic stops at the pre-fix submit (`05:03:21`); every post-fix observation is
carried on 8152. An APK swap by another session could not produce 8152 traffic.

## Instrument (transport only — zero DB writes)
`faultproxy1753.py`, stdlib reverse proxy in front of the shared dev backend on
127.0.0.1:8000. The shared backend was never stopped; port 8099 (another ticket's proxy)
was left alone.

Reachability had to be bridged, and this is stated plainly because it bounds the evidence:
this dev DB has `otp_login_status = 0`, `firebase_otp_verification = 1`, all social-login
flags `false`, and **zero rows in `phone_verifications`**. There is therefore no live route
to this sheet at all without a DB write, which QA is forbidden to make. The proxy supplies:

1. `/api/v1/config` — flips **only** `centralize_login.otp_login_status` to 1 and
   `firebase_otp_verification` to 0. Every other config value is the backend's.
2. `/api/v1/auth/login` (send-otp shape) and `/api/v1/auth/verify-phone` — synthetic 200s
   mirroring `CustomerAuthController::send_otp` / `verify_phone_or_email` field-for-field,
   the latter carrying `is_exist_user` so the sheet mounts.
3. `/api/v1/auth/login` (submit, carries `verified`) — mode-driven:
   `off` = **passthrough to the real Laravel backend**, `fail500`, `failempty`, `ok0`, `ok1`.
   An optional `MODE:SECONDS` suffix holds the submit in flight so the loading state can be
   observed without racing it.

**Everything downstream of the mount is genuine app code.** The headline failure was produced
with mode `off` — a real 404 `{"message":"OTP does not match"}` from the real backend, no
injection at all.

## PRE-FIX PIN — the defect reproduced (required before any PASS could mean anything)
Base `fda1b44c`, same device, same real-backend 404.

- `prefix-01-sheet-mounted.png` — sheet up, opaque white surface measured from y=1898 px.
- `prefix-02-sheet-vanished-after-failure.png` — **sheet gone**; the app is back on Phone
  Verification. The old `Get.back()` fired as the first statement of `_responseHandle`.
- `prefix-03-failure-log.txt` — the only failure surface was a transient toast:
  `[ERR] msg="error snackbar shown"`, raised from
  `existing_user_bottom_sheet.dart` `_responseHandle` inside a `Future.delayed(600ms)`.

The pin is valid: the pre-fix build visibly loses the sheet on failure.

## THE HEADLINE — post-fix
Mode `off` (real backend 404), submit held 8 s to make the in-flight state observable.

- In flight: `No` reads `clickable="false" enabled="false"`; the pressed choice is replaced
  by a node labelled `Loading`; **the row never disappears** — no bare centred spinner.
- **Three taps on the dimmed choice during the hold produced ZERO extra requests**
  (submit count delta = 1). That is `IgnorePointer`, measured, not inferred.
- After the failure the sheet is **still mounted** with both choices back and a persistent
  inline panel carrying the server message — `fix-04-panel-after-failure.png`.
- Re-pressing on the settled sheet re-submits (delta = 1, fresh correlation id).
- Log: `[FAIL] type=ApiFailure msg="existing user sheet submit failed"` paired with the
  api_client `[FAIL] endpoint=/api/v1/auth/login http_status=404 ... correlation_id=...`.
  **No `[ERR] msg="error snackbar shown"`** — the sheet's own toast is gone.

## THE DEFECT — the sheet paints no surface on mobile
`bug-sheet-has-no-surface.png` (= `fix-04`). The sheet's avatar, name, "Is it you?" and the
body copy are drawn straight over the dimmed Phone Verification screen with nothing behind
them; the body text collides with the underlying "END-TO-END SECURE" row and phone number.
Only the error panel and the two `NButton`s read normally, because they paint their own fills.

Measured, not eyeballed:
- pre-fix `prefix-01`: sheet surface is `(255,255,255)` from y=1898 px down.
- post-fix `fix-09-sheet-clean-geometry.png`: the same rows are the scrim `(117,117,117)`;
  the only non-scrim pixels are the dimmed mint of the *underlying* Verify button.
  The defect is present on a clean mount, not only when the panel shows.

Root cause, pinned at source:
- The changed file's own comment (lines 146–147) asserts *"Get.bottomSheet's route paints the
  surface and tightens width on mobile"*. That is false.
  `get-4.7.3/lib/get_navigation/src/extension_navigation.dart` passes
  `backgroundColor: backgroundColor ?? Colors.transparent`.
- All three mount sites call `Get.bottomSheet(...)` with **no** `backgroundColor`
  (`verification_screen.dart:467`, `social_login_widget.dart:464`,
  `login_suggestion_bottomsheet.dart:297`); the app declares no `bottomSheetTheme`.
- `NBottomSheet`'s widget constructor paints no surface by design — the surface comes only
  from its `NBottomSheet.show()` presenter, which sets
  `backgroundColor: Theme.of(context).cardColor`.
- The in-repo precedent agrees: the only other widget-constructor consumer,
  `item_bottom_sheet.dart` (NEARS-1586), wraps its `NBottomSheet` in
  `Container(decoration: BoxDecoration(color: Theme.of(context).cardColor, …))`.
  Verified live — `reg-01-item-sheet-neighbour.png` samples `(255,255,255)` across its body.

So the change kept the surface for desktop and dropped it for mobile on a false premise about
what the GetX route paints. The 16 pins are all green because none of them asserts a surface.

## Font-scale reachability
`font_scale` 1.3 and 2.0 produce **byte-identical** bounds, because `main.dart` clamps
`textScaler` to `[1.0, 1.3]` app-wide. 1.3 is therefore the ceiling of this axis. At 1.3 with
the panel showing: panel `[60,2455][1284,2644]`, `No` `[60,2707][650,2857]`,
`Yes, It's Me` `[695,2704][1284,2860]` — all inside the 2992 px viewport, no scrolling
needed. `fix-11-fontscale130-panel-reachable.png`, `fix-12-fontscale200-panel-reachable.png`.

## RTL (Arabic)
`fix-13-rtl-arabic-panel.png`. Choices mirror correctly (`نعم، إنه أنا` left,
`لا` right — the inverse of LTR). The panel's warning glyph sits at the start edge (right) and
is not mirrored (`mirrorForRtl: false`; the glyph is symmetric so this is a source-level
check). The transparent-surface defect is present in RTL too.

## Accessibility
- Flattened tree: exactly **one** node carries the panel message — `excludeSemantics` holds,
  no duplication.
- Tap targets at density 480 (dpr 3.0): `No` 197x50 dp, `Yes, It's Me` 196x52 dp — both
  well over 44 dp; both carry a semanticLabel (baseline was zero).
- The **audible** single-announcement check is **BLOCKED (env)** — TalkBack speech is not
  capturable from this harness.

## Success paths
- `ok0` (success, `isPersonalInfo` false): sheet dismissed, routed to "Complete your profile"
  (`NewUserSetupScreen`). Logs clean. `fix-08-success-newuser-setup.png`.
- `ok1` (success, `isPersonalInfo` true): sheet dismissed **and** the verification screen
  popped, landing back on the module home — the `backFromThis && address != null` arm.
  `fix-10-success-personalinfo-nav.png`. The 401 `[FAIL]` lines in that window are
  **instrument artifacts** (the synthesized token is not a real Passport token), not defects.
  The other arm (`navigateToLocationScreen`) was not reachable without wiping the stored
  address; that block is byte-identical pre/post fix.

## Panel message binding
- Real backend 404 → "OTP does not match" (populated `{message}` branch).
- `{errors:[{code,message}]}` 500 → "Server is temporarily unavailable".
- Empty `message` → "Sorry, something went wrong" (the fallback). Recorded as supplementary
  only; the empty case is owned by pins P2/P2b.
The panel was never blank in any observed state.

## Geometry
Both builds are content-sized well under the 0.5-of-screen cap (498 dp), so the cap is not
what sets the height on this mount. Intrinsic content height differs by ~27 dp from the
chrome swap (handle + scroll padding replacing the old `EdgeInsets.all(paddingSizeLarge)`
container). No cap/size regression observed.

## Automated backstop
`flutter test` (UserApp, fix worktree): **+3463 ~2 -4**. All 16 of the ticket's own pins in
`test/features/auth/existing_user_sheet_error_test.dart` passed. The 4 failures are in
`category_screen_back_button_test.dart` and `coupon_controller_test.dart` and **reproduce
identically on base `fda1b44c`** (`+20 -4` for those two files alone) — pre-existing.

## Regression sweep (adjacent surfaces, all light mode)
Module grid, Grocery module home, store screen, item-detail sheet, verification screen,
sign-in (manual + OTP), new-user setup, login-suggestion sheet, settings/language.
`ui_errors` over the sweep: 0 matches. No new red screens or overflows.
