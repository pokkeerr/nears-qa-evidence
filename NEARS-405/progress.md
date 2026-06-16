# NEARS-405 Edit-profile — live QA progress (checkpoint log)
Device: emulator-5554 (Pixel) · QA SHA 2844729c · fix-cycle 1 · backend 127.0.0.1:8000 (config HTTP 200)
Login account (UAE +971): customer@nears.com / +971565811199 (phone+email verified)
Config: manual_login_status=1; email_verification_status=0; phone_verification_status=0
Automated backstop: PASS — 5/5 (phone roundtrip + C1 null-safe gate)

## AC verdicts (appended as observed)
AC1+AC2: Edit Profile rendered non-blank, no NPE. Elements seen: +971 prefix, Tap to update photo (FAB caption), Change Password tile, Update Profile sticky CTA, More options (kebab). Shot 01.
AC2 composition (shot 01): navy hero + white title/back/kebab; avatar 128 + mint camera-FAB (navy icon); Name+Email NearsInput; phone CustomTextField re-themed w/ +971; Change Password NearsSettingsTile (mint lock chip+chevron); sticky NearsPrimaryButton 'Update' + check_circle. Widget tree confirms NearsInput/NearsPrimaryButton/NearsSettingsTile/CustomTextField/ProfileBgWidget all present.
AC3 +971 split (shot 01): UAE flag + '+971' in picker prefix; national '565811199' in field; split correct. (Account phone-verified => field disabled => picker locked; dial-code-switch path covered by unit test UAE->UK PASS.)
AC6 verify suffixes (shot 01): email verified => verified_user shield (non-tappable); phone verified => green verified badge + field locked/disabled. (Unverified->tappable branch gated OFF by config email/phone_verification_status=0 — code-verified, not live-triggerable on shared DB.)
AC8 avatar fallback (shot 01): no/loading image => placeholder rendered inside ClipOval, no crash.
AC4 image picker (shot 02 gallery, shot 03 preview): mint camera-FAB tap -> Android system PHOTO PICKER opens directly (NO camera-source chooser bottom sheet — correct); picked photo -> avatar preview shows Image.file(pickedFile), placeholder replaced; no crash; NOT saved.
AC5 change-password tile (shot 04): tile routes to reset-password screen (page:'password-change') — 'Change Password' + 'Enter your new password...' form. Tile shown because manual_login_status=1 (config). Hidden-when-off path is config-gated (code-verified). Did NOT change a real password; backed out.
AC7 validation snackbar (shot 06): invalid email 'notanemail' + Update -> snackbar "Enter a valid email address" (red error icon) fires client-side pre-submit; screen stays, NO save. Also observed LIVE: changing email away from saved value REMOVED the verified shield suffix (matches unit test 'edited email drops to false'). Empty-name path: name field AUTO-REFILLS on rebuild (pre-existing controller logic lines 132-136, frozen) -> empty-name snackbar not reachable via UI; covered by code. Did NOT save.
AC(delete overflow) render-verify (shot 07 kebab, shot 08 dialog): kebab 'More options' -> 'Delete Account' -> ConfirmationDialog "Are you sure to delete your account? It will remove your all information." No/Yes. Tapped NO. NEVER deleted. Account intact (email/phone still shown after dismiss).
AC9 dark mode (shot 09): navy header STAYS navy (white title/back/kebab); scaffold navyDeep; NearsInput fills navyContainer; mint FAB+CTA navy icon/text (const); verified shield + green phone badge + check_circle render; no crash. OBSERVATION: NearsInput body-text contrast in dark is weak (name/email value text dim on navy field) — DLS NearsInput dark-variant concern, NOT this screen's logic; text present + legible-but-low-contrast. Flag as DLS followup.
AC9 RTL/Arabic (shot 10): no crash. Header back-chevron LEADING=right (PositionedDirectional start), kebab TRAILING=left (end). Avatar FAB bottom-START=left. Field labels+values right-aligned. Phone: +971+flag on right, national left, verified badge start/left. Email verified shield trailing->left. Change-pwd tile icon chip right, chevron left (mirrorForRtl). Sticky mint CTA 'تحديث'+check_circle. +971 split intact in RTL.
AC1 C1 crash-fix CRITICAL (shot 11 + cold frames): Edit Profile opened under GSM/GPRS-throttled network (model-null window widened) + 2x hot-restart cold rebuild -> rendered NON-BLANK, NO NPE. Dart MCP get_runtime_errors = "No runtime errors found" (3x). Logcat scan for Null-check/NoSuchMethod/isEmailVerified/_TypeError across full cold-build = EMPTY. Unit test locks the exact pre-fix crash (emailVerifiedOf(null)=false). PASS.
AC9 guest state (shot 12): Edit Profile when logged out -> NotLoggedInScreen ("You are not logged in" / "Please login to continue" / mint Login CTA navy text). No crash. callBack re-init wired (code).
AC9 guest re-init callback: after login from NotLoggedInScreen, returned directly to Edit Profile form (callBack: _initCall re-ran). Session restored (customer@nears.com / +971). No crash.

## Regression sweep (clean — 5 surfaces, shots 13-14)
- Profile tab (sibling reskinned, shares ProfileBgWidget/DLS): renders clean, no errors.
- Reset-password route (change-pwd target): renders clean (shot 04).
- Settings (language+dark toggles used): renders clean.
- My Address (NearsInput consumer — verifies additive textCapitalization param safe): clean.
- Home tab: clean.
- NearsIcon change verified PURELY ADDITIVE ('warning'+'check_circle' map entries; no existing glyph remapped) -> zero app-wide regression risk.
- Dart MCP get_runtime_errors across whole session: "No runtime errors found".

## Automated backstop
- flutter test test/features/profile/ -> 11/11 PASS (phone roundtrip x2 + C1 null-safe gate x3 + profile_controller_pin x6).

## DB-SAFETY: NEVER tapped Save/Update-submit; NEVER changed a password; tapped NO on delete-account. Account customer@nears.com intact.
