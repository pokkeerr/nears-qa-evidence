# NEARS-1749 — delta re-QA (fix cycle 1)

- tested_sha: `57bb0e4c` (worktree `/Users/Apple/Projects/nears-NEARS-1749-newuser-setup-states`, branch `feat/NEARS-1749-newuser-setup-states`)
- device: `emulator-5554` (see DRIFT below — 5562/5556 were NOT free)
- SDK: `/Users/Apple/Tools/flutter` 3.41.9 (absolute), debug build from the worktree

## DRIFT — device pool
- Brief said locks on `emulator-5562` + `emulator-5556` were "already held for NEARS-1749".
  OBSERVED: both `owner.json` carry `key: NEARS-1554`, `pid 4523` (a live `claude`, NOT my
  session anchor 28462). `qa_lock_check` returned rc=1 (BLOCKED) on 5556, 5562 AND 5558.
  I did not steal them. Fell back to `emulator-5554`.
- `emulator-5554` disk precheck initially **816072 KB = 796 MB free — 3 MB UNDER the 800 MB
  floor**. Every other pool device was locked. Reclaimed by uninstalling a stale, unowned
  `com.izzes.nearsdelivery` (70 MB APK, no lock on 5554) -> 1153184 KB = 1126 MB free, then
  acquired the lock. `pm trim-caches 2000M` freed nothing.

## §8 automated gate — OBSERVED
`flutter test` (full UserApp suite) at 57bb0e4c: **`+3313 ~2 -6`** — matches the predicted
+3313 (baseline +3309 + 4 new pins). Extracted by `[E]` marker over the COMPLETE log
(8611+ lines), not counter-increments, not a tail.
- `[E]` count = 6, mapping exactly to the 3 confirmed pre-existing files:
  - `test/features/category/category_screen_back_button_test.dart` x1
  - `test/features/coupon/coupon_controller_test.dart` x3
  - `test/golden/dls_golden_test.dart` x2
- **No seventh name** -> no isolation/standalone re-run needed.

## AC table (delta rows only)
(filled in below as observed)

## FALSE PREMISE in the brief — the named chain is unreachable (OBSERVED)
The brief's chain ("unverified email -> PostAuthDecision(verifyEmail, loginType: manual) with
number unset -> sign_in_view.dart:214") **cannot occur on this backend**:
1. `Admin/app/Http/Controllers/Api/V1/Auth/CustomerAuthController.php` `manual_login()` has a
   SINGLE success return and it **hardcodes** `'is_phone_verified'=>1, 'is_email_verified'=>1`.
   So `_decideManualPostAuth` (auth_controller.dart) can never reach its `verifyEmail` branch —
   `isEmailVerified` is always true. `sign_in_view.dart:214` is dead on this backend.
2. `register()`'s email-verify branch is gated on `email_verification_status == 1`; that
   business_settings row **does not exist** (query returned only `manual_login_status=1`).
   No `otp_login_status`, no `social_login_status`, no `phone_verification_status` either.
3. DB: 0 users with `is_phone_verified=1 AND is_email_verified=0`.

## The chain that IS real and reachable (used instead)
`phone: null` on the MANUAL path comes from `AuthFlowOutcome.needPersonalInfo`:
- `CustomValidator.isPhoneValid()` returns `phone: ''` when `PhoneNumber.parse` throws (an email
  input), so `validateAndLogin` sets `numberWithCountryCode = ''`.
- `sign_in_view.dart:198` -> `getNewUserSetupScreen(phone: '')` -> URL `phone=` ->
  `route_helper.dart` maps `'' -> null`. => `NewUserSetupScreen(loginType:'manual', phone: null)`.
- Precondition: `is_personal_info == 0`, i.e. `if($user->f_name)` falsy. Register's validator is
  `'name' => 'required'`, which ACCEPTS the string `"0"` — and `'0'` is falsy in PHP.
  So a real UI signup with full name `0` produces the state. No DML, no injected route.

## Live demonstration — the REAL production chain (all OBSERVED, emulator-5554)
Chain driven end-to-end through the UI, no injected route, no DML:
1. UI signup (Create Account): full name `0`, email `qa1749d@example.com`, phone `+971561749051`,
   password, terms checkbox (unlabeled CheckBox, `content-desc=""` — tapped at its live
   tree-reported centre, not a hardcoded coordinate).
   -> `[NET] POST /api/v1/auth/sign-up` -> `http_status=200`. DB row id=413, `f_name='0'`.
2. Profile -> Logout -> Yes.
3. Sign In with the EMAIL + password.
   -> `manual_login` returns `is_personal_info = 0` (because `if($user->f_name)` is falsy for '0')
   -> `AuthFlowOutcome.needPersonalInfo` -> `sign_in_view.dart:198`
   -> **NewUserSetupScreen(loginType:'manual', phone: null)**.
   Screen OBSERVED: "Complete your profile" / "User Name" / "E-mail" / "REFER CODE(OPTIONAL)" /
   "Done" — and **NO phone field** (confirms `_isSocial == false`, `phone == null`).
4. Tap Done with E-mail empty -> visible inline `⚠ Email field is required`, **no dispatch**.
   (Client-side validation, correctly surfaced — not a silent path.)
5. Fill E-mail, tap Done.

### The five required confirmations — ALL OBSERVED
| # | Required | Observed |
|---|---|---|
| 1 | a panel appears | YES — panel rendered on screen |
| 2 | it carries the backend message | YES — `The phone field is required.` |
| 3 | a retry affordance exists | YES — `Try Again` |
| 4 | an AppLogger line is emitted | YES — see excerpt below |
| 5 | **`[NET] POST /api/v1/auth/update-info` IS dispatched** | **YES — this is the regression's closure** |

```
I/flutter: [NET] POST endpoint=/api/v1/auth/update-info
I/flutter: [NET] endpoint=/api/v1/auth/update-info http_status=403
I/flutter: [FAIL] endpoint=/api/v1/auth/update-info http_status=403 type=ApiFailure msg="unhandled api response" correlation_id=d7de6e4c-b8c0-4c44-ad8d-26bc1b5da0b8
I/flutter: [FAIL] endpoint=/api/v1/auth/update-info http_status=null type=ApiFailure msg="new-user setup update-info failed"
   (thrown from new_user_setup_screen.dart:435 -> AppLogger.failure)
```
Per the BINDING instruction in the brief, the uncompletable-ness ("phone required" on a screen
with no phone field) is the SEPARATE pre-existing defect owned by **NEARS-1859** and is scored
**PASS** here: the failure is now visible, accurate and logged instead of silent.

### Correlation join (NEARS-564) — OBSERVED
App `correlation_id=d7de6e4c-b8c0-4c44-ad8d-26bc1b5da0b8` found in
`Admin/storage/logs/laravel.log` (6 lines, same `trace_id=455194d68b8198fc73505e56802876ca`).
Those 6 BE lines are all pre-existing OTel-exporter noise (OpenObserve not running), unrelated.

### Retry single-fire — OBSERVED
One tap of `Try Again` -> **exactly 1** `[NET] POST /api/v1/auth/update-info` (grep count = 1),
fresh `correlation_id=9a3dbfda-6ceb-4722-b5e8-c3ce66565084`, panel persists, both `[FAIL]` lines
re-emitted. No double-fire.

### No new silent path on this screen — OBSERVED
`ui_errors` validity: **scanned 518 flutter-tag lines of 173376 buffer lines; 5 matches**
(a real validity count, not a vacuous zero). All 5 accounted for: 4 are the intended
update-info failures above; the 5th is an UNRELATED pre-existing `update-interest` 403 —
see `bug-update-interest-403-treated-as-success.log`.
Every failure path exercised on this screen produced BOTH a user-visible surface AND a log line.

### Social spot-check — NOT live-drivable in this environment
`social_login_status` business_settings row does not exist -> no social entry point in the UI.
INFERRED (not observed): the fix only ADDS `_isSocial &&` to the condition, so when `_isSocial`
is true the expression is identical to pre-fix; the social path cannot have changed. The prior
cycle demonstrated it live at 7889eddf.

### Core-path smoke — OBSERVED
Cold start -> splash -> language -> onboarding -> location -> module list -> Grocery home ->
Profile tab. Clean.
