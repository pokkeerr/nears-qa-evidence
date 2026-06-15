# NEARS-396 QA progress checkpoint (live)

Device: emulator-5554 (Android 17 / API 37). Branch feat/NEARS-396-auth-forms. baseUrl http://10.0.2.2:8000 (real local backend, up).

## Automated backstop
- flutter analyze: CLEAN (8 pre-existing infos, none in the 5 auth screens / DLS) — PASS
- flutter test: 872 passed (expected 872, incl. new nears_auth_widgets_test.dart) — PASS

## Live config (gates what renders) — from /api/v1/config zone 1
- centralize_login: manual_login_status=1, otp_login_status=0, social_login_status=0 -> MANUAL-ONLY mode live
- social (google/fb/apple): all status=false -> social blocks gated OFF live (verify by source)
- ref_earning_status=0 -> refer-code field gated OFF live (verify by source)
- firebase_otp_verification=1 -> forgot-pass phone channel active; OTP via Firebase (no live SMS completion)

## Per-AC / per-scope verdicts (appended as observed)

### Sign In (live, emulator-5554, light)
- Hero navy + mint "Nears" wordmark + tagline -> PASS (01,02)
- Sign In CTA mint + NAVY text + ambient glow (NOT white-on-mint) -> PASS (02)
- Remember-me toggles ON -> mint fill + NAVY tick (NOT white-on-mint) -> PASS (02) [persist-across-restart: source-verified saveUserNumberAndPasswordSharedPref]
- Password obscured-by-default + eye toggle (NearsGlassPasswordField _obscure=true, NearsIcon visibility) -> PASS (source nears_glass_password_field.dart + 04/05)
- Validators preserved in FormField migration (email/phone validator + password validateEmptyText) -> PASS (source manual_login_widget L116,140)
- Email<->phone auto-detect + dial-code (toggleIsNumberLogin regex) -> PASS (source L99-116; field accepts input live)
- T&C footer Terms/Privacy links + CONTINUE AS GUEST present -> PASS (01,02)
- Language pill present -> PASS (01)
- OTP-login toggle + social block ABSENT live = CORRECT (config manual-only, social off). Source-verify config gating.
- ui_errors: clean (no overflow/red-screen)

### Sign Up (live, light)
- Hero + "Join the Elite" + tagline + mint wordmark -> PASS (06)
- 5 fields: name/phone(+971 picker)/email/password/confirm, uppercase eyebrow labels + required * -> PASS (06)
- Password + Confirm eye toggles present -> PASS (06)
- Refer-code field ABSENT = CORRECT (ref_earning_status=0) -> PASS
- T&C GATES CTA: unchecked -> CTA dimmed + Sign Up tap does NOT navigate (gated) -> PASS (06 + no-nav)
- T&C checked -> mint tick (NAVY tick, not white) + CTA brightens to full mint -> PASS (08)
- T&C link routes to Terms page (body empty = pre-existing empty business_setting, NOT reskin defect) -> link PASS
- Already have account? Sign In present -> PASS
- ui_errors clean
