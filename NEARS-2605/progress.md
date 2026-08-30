# NEARS-2605 QA — DeliveryApp dm_registration_screen.dart configModel! unwrap fix

Worktree: /Users/Apple/Projects/nears-DeliveryApp-NEARS-2605-configmodel-dmreg
Branch: fix/NEARS-2605-dm-registration-configmodel-unwrap @ ee9a74037a66a9222b3f05ffc5f3e1f96c1f6ee2
Device: emulator-5554 (Android), iOS sim 53F3807C-3BF6-46ED-8487-DEC957036BAA locked but not driven
  (structural pre-check + fresh iOS tooling doc from same-day NEARS-2604 QA showed synthetic taps
  don't land on Flutter GestureDetectors on this host's sim right now — kept Android as primary).

## Code verification
- grep -c "configModel!" dm_registration_screen.dart -> 0. PASS.
- grep -rn "configModel!" DeliveryApp/lib -> 33 remaining elsewhere, untouched. PASS (unregressed).
- Line 57 (initState) + line 198 (build ternary) both read
  `Get.find<SplashController>().configModel?.country ?? "AE"` — structurally IDENTICAL pattern
  to sign_in_screen.dart lines 37/39/76 (the verified-working NEARS-2409 fix).
- flutter analyze on the file: No issues found.

## AC1 (cold-race, null-safe default AE/+971)
Repro method (per ticket): logged in via UI (Ali Hassan, +971565656656), re-logged-in same DM via
direct API call to /api/v1/auth/delivery-man/login (rotates token, staling the cached device
token), then `adb shell am force-stop` + relaunch.
- Logs confirmed a genuine live race on THIS host/session:
  05:08:58.202 GET /delivery-man/profile ; 05:08:58.207 GET /config
  05:08:59.784 profile 401 (resolves FIRST) ; 05:09:00.288 config 200 (resolves ~1.1s later)
  -> contradicts NEARS-2409's own "not reliably reproducible on Android" finding; timing is
     evidently host/load dependent.
- No crash / no red-screen / no [ERR] on sign-in screen during the live null-configModel window
  (only the expected `[FAIL] endpoint=/api/v1/delivery-man/profile http_status=401` line, which
  IS the paired AppLogger.failure() line for that expected 401 — not a silent failure).
- **Could not force live entry into DmRegistrationScreen itself during the null window**: its
  sole entry point, the "Join as a Delivery man" button on sign_in_screen.dart, is itself gated
  `configModel?.toggleDmRegistration ?? false` inside `GetBuilder<AuthController>` (not
  `<SplashController>`) — it does not rebuild when configModel resolves, so it stays hidden
  during the race and only re-evaluates on the next unrelated AuthController.update() (e.g.
  tapping Remember Me), by which point configModel is already non-null. Confirmed live: tapped
  Remember Me ~50s after config had resolved -> button appeared immediately (already-populated
  configModel). This is a structural property of sign_in_screen.dart (NEARS-2409's file, not
  this ticket's), documented in deliveryapp-screen-inventory.md, flagged as a non-blocking
  regression_bugs/followups candidate.
- Verdict: AC1 evidence tier achieved = **structural-correctness (code matches proven pattern)
  + strong live corroboration (confirmed the exact race timing occurs on this host/session, and
  confirmed the sibling already-fixed screen renders cleanly with no crash under that live
  race)** — NOT a full live crash-repro of dm_registration_screen.dart's pre-fix code
  specifically, because the app's only navigation path into that screen cannot structurally be
  taken while configModel is null. Per the ticket's own fallback-tier guidance, this is reported
  as this exact tier, not silently upgraded.

## AC2 (warm-state, no visible regression)
- Fresh cold boot (no stale token) -> sign-in screen -> "Join as a Delivery man" -> DM
  Registration screen rendered cleanly: fields Basic/Account Information, Phone *, dial code
  "+971", First/Last name, E-mail, Password/Confirm Password, Profile Picture, Next button.
  0 runtime errors (ui_errors scan clean).
- Config's actual `country` field IS "AE" (curl-verified), so warm vs null-default resolve to
  the same visible "+971"/"AE" value in this environment — expected, not a false positive.
- Tapped the "+971" dial-code field -> full country picker opened correctly (UAE entry present,
  RTL Arabic country names rendering, Scrim overlay) -> confirms the countryDialCode field (line
  198) is fully interactive post-fix, matching pre-fix behavior.
- Regression sweep (bounded): Sign-in screen normal login (Ali Hassan) -> dashboard -> Profile ->
  back to sign-in -> Forgot Password screen. All rendered cleanly, 0 new runtime errors.

## Automated backstop
`flutter test` (DeliveryApp, full suite): 376 passed, 0 failed. Matches engineer's reported run.

## Regression finding (non-blocking, filed as regression_bugs / followups)
sign_in_screen.dart's "Join as a Delivery man" button visibility does not reactively update when
SplashController.configModel resolves (GetBuilder is scoped to AuthController only) — it stays
hidden through a stale-token cold-start race until some unrelated AuthController.update() fires.
Pre-existing, outside NEARS-2605's file, not introduced/regressed by this fix.
