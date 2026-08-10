# NEARS-1749 QA progress (live, appended as observed)

Tested sha: 7889eddf · worktree /Users/Apple/Projects/nears-NEARS-1749-newuser-setup-states
Device: emulator-5562 (lock held for NEARS-1749, anchor pid 28462). Light mode only (dark deferred).

## Navigation finding (OBSERVED) — blocks live AC demo, NOT a product defect
- `am start ... --es route '/new-user-setup-screen?...'` DOES reach the route (flutter's own
  `--route` invocation fails first: it passes the route unquoted to `adb shell`, so the `&`
  between query params splits the command — `exit code 127: --ez: inaccessible or not found`).
- On that cold route launch the screen throws `Null check operator used on a null value`:
  `new_user_setup_screen.dart` initState reads
  `Get.find<SplashController>().configModel!.country!`, and config is only ever fetched by the
  splash screen (`splash_screen.dart` -> `getConfigData`); `main.dart` does not prefetch it and
  `SplashController` has no onInit cache load. Route-launching bypasses splash => config null.
- `route_helper.dart` `_waitForModule`/`checkModuleId` cannot supply it either: with no saved
  address it takes the `else` branch (modules only, no config); with a saved address and
  `fromDeeplink:false` (which is what the newUserSetup GetPage passes) it early-returns.
- => The red screen is an artifact of QA route injection, NOT a defect. Not reported as a bug.
- Shot: nav-coldroute-configmodel-null-NOT-A-DEFECT.png

## Real-flow reachability (OBSERVED)
- Entry points to the screen: verification_screen.dart (PostVerifyAction.newUserSetup),
  social_login_widget.dart, sign_in_view.dart, existing_user_bottom_sheet.dart,
  login_suggestion_bottomsheet.dart — all post-auth, all for a NEW (unregistered) user.
- DB (read-only): `SELECT ... FROM users WHERE f_name IS NULL OR f_name='' OR email IS NULL
  OR email=''` returns ZERO rows (10 users total). No seeded incomplete-profile account exists,
  so no existing login lands on this screen.
- Reaching it therefore requires registering a new phone/social account = a DB write. QA is
  read-only on the DB, so this was NOT done.

## How the screen WAS driven (OBSERVED) — reusable recipe
Route injection is impossible cold, but the screen is reachable in a fully-configured app:
1. `am start -n com.izzes.nears/com.izzes.nears.MainActivity` (normal boot -> splash loads config).
2. Read the VM-service URI from `adb logcat` ("Dart VM service is listening on ..."), `adb forward`.
3. `flutter attach --debug-url=<uri>` from the worktree (registers the expression compiler; HTTP-only
   RPC returns `_compileExpression: No compilation service available`, WebSocket + attach works).
4. Over `ws://.../ws`: `evaluate(targetId=rootLib, expression=
   'Get.toNamed("/new-user-setup-screen?name=QA Tester&login_type=social&phone=&email=&back_from_this=false&module=null")')`.
   Pre-check `Get.find<SplashController>().configModel != null` -> "true" before navigating.
No product code was modified. All taps re-derived from a live uiautomator dump (no hardcoded coords).

## a11y bridge control (OBSERVED) — emulator-5562 is HEALTHY
Dumped twice on the target screen; control "dump contains >=1 node with a non-empty label" is
SATISFIED (6 labelled nodes). So an unnamed node on this device is a real finding, not bridge fault.

## AC results (all OBSERVED live on emulator-5562, light mode, sha 7889eddf)
| AC | result | evidence | logs |
|---|---|---|---|
| AC1 invalid-phone inline error (was a toast) | PASS | ac1-invalid-phone-inline-error.png — "Invalid phone number." under the field, error border, NO toast | `[WARN] msg="new-user setup: phone failed validation"` |
| AC1 clear-on-edit (phone errorText) | PASS | one KEYCODE_DEL shrank the field 183px->126px, message gone | clean |
| AC1 server-failure panel + retry | PASS | ac1-server-failure-panel-backend-message.png — panel carries the BACKEND message "The email field is required." (403), warning icon, "Try Again"; no generic copy | `[FAIL] endpoint=/api/v1/auth/update-info http_status=403 ... correlation_id=9ceca347` + screen `[FAIL] "new-user setup update-info failed"` |
| AC1 retry re-invokes, single fire | PASS | one tap on Try Again -> exactly ONE new request (correlation_id 2094be29), no double-fire | as above |
| AC1 transport failure | PASS | ac1-transport-failure-panel-no-global-toast.png (airplane mode) — panel shows "Connection to API server failed due to internet connection"; NO global snackbar beside it (DoD 0.2) | `[FAIL] ... msg="api request threw" correlation_id=5133aafb` |
| AC2 AppLogger coverage, PII-safe | PASS | validation -> `.warn` (no e/st pair), server+transport -> `.failure`; no phone/name/payload in any line | see above |
| AC3 CTA loading state | PASS | ac3-cta-loading-spinner-and-retry.png — spinner replaces "Done" in the mint CTA mid-flight; panel cleared on submit | clean |
| AC4 toast census | PASS | `ScaffoldMessenger` 0, `showCustomSnackBar` 0 in new_user_setup_screen.dart (was 2) | n/a |
| AC5 a11y | PARTIAL, as ruled at [2] | 6 interactive nodes OBSERVED: Back(named), +971 picker(named), Done/Try Again(named), 3 EditTexts announce their VALUE only. `semanticLabel` count 0 is correct by design. 2 nodes escalated to NEARS-1848 — NOT re-flagged | n/a |
| AC6 success navigates | UNVERIFIABLE live | needs an authenticated 200 from update-info = a new/updated user row. QA is read-only on the DB and no seeded incomplete-profile user exists. Covered only by the green pin in new_user_setup_submit_error_test.dart | n/a |
| AC7 no regression | PASS | Back from the screen returns to Home (module list renders: Grocery & Food 20 stores, Food & Restaurant 5, Pharmacy 5); no red screen, no new [ERR]/[FAIL]/overflow after the smoke | clean |

## Automated backstop
- Full suite at HEAD (worktree, /Users/Apple/Tools/flutter): `+3309 ~2 -6`.
- Both new pin files ran green (new_user_setup_a11y_test.dart, new_user_setup_submit_error_test.dart).
- The 6 failures ISOLATED and re-run standalone in BOTH trees:
  - HEAD (worktree 7889eddf): `+20 -6`
  - base (primary tree, branch feat/userapp-reskin2 @ 4d6b4396; merge-base with this branch is d84d464b): `+20 -6`
  - IDENTICAL failure-name set in both: category_screen_back_button_test.dart x1,
    coupon_controller_test.dart x3, dls_golden_test.dart x2 (light+dark).
  => all six are pre-existing; NEARS-1749 introduces none. Section 8 gate satisfied.

## DEFECT (task_bug, breaks AC1) — silent CTA on the non-social entry path
Independently reproduced live at 16:12 (see bug-silent-cta-nonsocial-empty-phone.log/.png).
`loginType != 'social'` => NPhoneField is not built => `_phoneErrorText` has no renderer =>
tapping Done with a valid name+email does NOTHING visible and dispatches NO request.
Pre-change this branch showed a visible toast. VERDICT: FAIL.
