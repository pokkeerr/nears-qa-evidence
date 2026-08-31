# NEARS-1850 — QA (first pass)

- tested_sha: `4f49015e7` (worktree `/Users/Apple/Projects/nears-NEARS-1850-response-model-field-key`,
  branch `feat/NEARS-1850-response-model-field-key`)
- device: `emulator-5556`, SDK `/Users/Apple/Tools/flutter` 3.41.9 (absolute), debug build from the worktree

## §8 automated backstop — OBSERVED
`flutter test test/features/auth/` at `4f49015e7`: **417/417 passed**, including all 3
`auth_service_field_key_test.dart` unit tests (AC1) and all `new_user_setup_submit_error_test.dart`
widget tests (the NEARS-1850-tagged ones covering AC2, AC3, and the ux-f1 fix-cycle-1 finding —
these drive the REAL `NewUserSetupScreen` widget with only the network layer faked).

## Code-flow confirmation (static, backs the automated result)
- `UserApp/lib/common/models/response_model.dart`: `fieldKey` field added, defaults null.
- `UserApp/lib/features/auth/domain/services/auth_service.dart` `updatePersonalInfo`: on a
  non-200 response with `body['errors']` present, re-parses via the existing `ErrorResponse`
  model and threads `errors[0].code` onto `ResponseModel.fieldKey`; absent/null body -> null.
- `UserApp/lib/features/auth/controllers/auth_controller.dart` `updatePersonalInfo` (line 267-296):
  returns the `ResponseModel` from the service UNMODIFIED — `fieldKey` survives to the screen.
- `UserApp/lib/features/auth/screens/new_user_setup_screen.dart` `_updatePersonalInfo`:
  `_clearPhoneError()` now runs on every submit (line 413, the ux-f1 fix), and the routing
  condition is `response.fieldKey == 'phone' && _isSocial` (line 458) — panel otherwise.
- Backend: `Admin/app/Http/Controllers/Api/V1/Auth/CustomerAuthController.php::update_info`
  (line 1152+) — `unique:users,phone` is appended to the phone rule ONLY when
  `$request->login_type == 'social'` (line 1161-1163); `Helpers::error_processor` (CentralLogics)
  emits `{code: <validator field key>, message: <first error>}` — matches
  `ErrorResponse`/`Errors.fromJson` exactly.

## LIVE demonstration — the REAL reachable chain (OBSERVED, emulator-5556)
No DML, no injected route, no VM-service state force (this QA session's tool grant does not
include Dart VM-service evaluate/hot-reload — see UNVERIFIABLE section below for what that
blocks). Chain driven end-to-end through the UI:
1. Sign Up: full name `0` (falsy in PHP), email `qa1850d@example.com`, phone `+971561850061`,
   password, terms checkbox -> `POST /api/v1/auth/sign-up` succeeds, auto-logs in.
   DB confirms: `users.id=418, f_name='0'`.
2. Profile -> Logout -> Yes.
3. Sign In with the same email + password -> `manual_login` returns `is_personal_info=0`
   (`if($user->f_name)` is falsy for the string `'0'`) -> `AuthFlowOutcome.needPersonalInfo`
   -> `NewUserSetupScreen(loginType:'manual', phone:null)`.
   Screen OBSERVED: "Complete your profile" / "User Name" / "E-mail" — **no phone field**,
   confirming `_isSocial == false`.
4. Filled User Name = `QATester`, E-mail = `qa1850d@example.com` (the SAME email already on
   this user's own row — deliberately, to force a real `unique:users,email`-shaped failure).
   Tapped Done.
5. **Real backend response observed**: `403` with `errors:[{code:'phone', message:'The phone
   field is required.'}]` — this is the pre-existing NEARS-1859 defect (phone required on a
   screen with no phone field), reached here as a byproduct, not injected.

### AC3 (non-social branch) — confirmed LIVE, for real
This IS the exact "also verify" scenario in the brief: a `code:'phone'` failure landing on the
**non-social** branch, which has no `NPhoneField` slot to absorb it (`_isSocial == false`, so the
routing condition `response.fieldKey == 'phone' && _isSocial` is false regardless of the code).
**OBSERVED on screen**: the form-level panel rendered with the real message "The phone field is
required." and a "Try Again" affordance — the failure was NOT swallowed and did NOT route to a
non-existent inline slot. Screenshot: `ac3-nonsocial-phonecoded-panel.png`.

### Logs-first check — OBSERVED, clean
```
I/flutter: [FAIL] endpoint=/api/v1/auth/update-info http_status=403 type=ApiFailure msg="unhandled api response" correlation_id=d430fa0e-f467-4712-b326-83628ff9ef4f
I/flutter: [FAIL] endpoint=/api/v1/auth/update-info http_status=null type=ApiFailure msg="new-user setup update-info failed"
```
Both are the EXPECTED paired AppLogger.failure call for this deliberately-forced failure —
PII-safe sentinel (`ApiFailure`), path-only endpoint, correlation id present. `ui_errors` scanned
125 pid-scoped flutter-tag lines (of 654 buffer lines), 2 matches, both accounted for. No
unexpected `[ERR]`/`[FAIL]` anywhere else in the session.
`Admin/storage/logs/laravel.log` does not exist in this worktree (fresh worktree, no BE log yet)
— best-effort BE-log correlation skipped, noted rather than faked.

## UNVERIFIABLE — the SOCIAL branch could not be reached live in this environment
Every code path that constructs `NewUserSetupScreen(loginType:'social', ...)` requires a
COMPLETED Google/Apple/Facebook OAuth handshake (`social_login_widget.dart`,
`existing_user_bottom_sheet.dart`, `login_suggestion_bottomsheet.dart`, `sign_in_view.dart:308-310`
all pass `loginType` from a real social-auth callback). The social-login UI entry point itself is
also hidden: `business_settings.social_login_status = 0` on the shared dev DB (verified via
`SELECT`), and `SocialLoginWidget`'s build gates on
`configModel.socialLoginStatus` — confirmed live: the Sign In screen rendered with NO social
buttons at all. Facebook's own SDK additionally errors in the log
(`Application has been deleted`, OAuthException 190) — a second, independent signal social auth
is not functional in this environment.

**This QA session's tool grant does not include a Dart VM-service evaluate/hot-reload capability**
(only `mcp__dart__get_runtime_errors` is granted), so the "VM-service client-state force" technique
referenced in the brief (used for NEARS-1752's `otp_login_status` case) was not available to me here —
stated plainly rather than fabricated. I also checked for a generic deep-link fallback
(`LinkConverter.convertDeepLink` / `navigateFromLink`): confirmed it only maps a fixed allow-list
of known link shapes (home, store, item-details, refer-and-earn) with an `else` branch that falls
back to the initial route for anything else — `new-user-setup-screen` is not one of the mapped
shapes, so a deep link cannot reach it either.

This is the SAME environmental constraint NEARS-1749's QA hit on this identical screen
(`docs/qa-evidence/NEARS-1749/progress.md`, "Social spot-check — NOT live-drivable in this
environment").

**Consequently unverifiable live, backed by automated + static evidence instead:**
- AC2 core routing (a `phone`-coded failure on the SOCIAL branch -> inline `NPhoneField.errorText`,
  not the panel) — pinned live-shaped by `new_user_setup_submit_error_test.dart`'s
  `'NEARS-1850: a fieldKey of "phone" routes to the inline phone error, not the panel'` test,
  which drives the real screen widget with a faked network layer. Also: the real backend CAN
  produce this exact shape for a genuine social signup (duplicate phone + `login_type=social` ->
  `unique:users,phone` validator rule, confirmed by reading `update_info`'s validation rules) —
  the mechanism is real, only the OAuth entry point is unreachable here.
- The fix-cycle-1 "ux-f1" finding (stale inline phone error must clear on a fresh unrelated
  failure) — this is specifically a social-branch behavior (the inline phone slot only exists
  there). Pinned by the widget test `'NEARS-1850 ux-f1: resubmitting without touching the phone
  field clears a stale inline phone error...'`, same real-screen/faked-network approach.
- The "phone code on the non-social branch" negative control was ALSO confirmed live for real
  (see above) — the automated widget test for it (`'a "phone" fieldKey on the non-social (email)
  branch still shows the panel'`) is corroborating, not the only evidence.

## Regression — clean
No unexpected `[FAIL]`/`[ERR]` anywhere in the session. Core-path smoke clean: language ->
onboarding -> location permission -> module home -> sign-up -> logout -> sign-in -> new-user-setup
(both entry conditions) -> profile. `flutter test test/features/auth/` 417/417.
