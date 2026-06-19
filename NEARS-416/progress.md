# NEARS-416 QA progress — Access Location guest auth-funnel panel

Device: emulator-5554 (Android) | Branch: feat/NEARS-416-access-location-funnel @ 7f83d774
Build tree: MAIN /Users/Apple/Projects/nears/UserApp | baseUrl: http://10.0.2.2:8000 (real local backend)

## Automated backstop
- widget test test/features/location/guest_auth_funnel_panel_test.dart: 4/4 PASS

## Live AC observations
- AC1 PASS: light mode — grab-handle pill + navy heading "You're almost there!" + muted subtext + mint pill CTA with NAVY text (not white-on-mint). Shot 01-guest-funnel-light.png. No runtime errors.
- Logged out via Profile > Logout > Yes; reached Access Location via Home > Change Location (guest path).
- AC3 PASS: tapped mint CTA -> navigated to Sign In screen (Sign In / Create Account / Forgot Password / CONTINUE AS GUEST). No creds submitted. Shot 02-cta-navigates-signin.png. No errors.
- AC2 PASS: "Set From Map" -> opens Pick Location/Google Map (backed out, nothing persisted). "Use Current Location" -> tappable, resolves in-zone, navigates to guest Home (guest local-only, no DB write). System back on Access Location -> "Back press again to exit" snackbar (PopScope preserved, did not exit). Shot 03-popscope-back-snackbar.png. No errors.
- AC4 PASS: dark mode (Settings > Dark Mode ON) — panel surface = dark elevation navy (not frozen light), grab-handle theme-resolved, heading mint/sky legible, subtext legible, mint CTA navy text intact. No invisible text, no frozen colors. Shot 04-guest-funnel-dark.png. No errors.
- AC5 PASS: Arabic/RTL (Settings > Language > Arabic) — heading "أوشكت على الانتهاء!" at logical start (right), subtext legible/wrapped, mint CTA "تسجيل الدخول/إنشاء حساب" mirrored to logical end (left), guest controls mirrored, no overflow. Shot 05-guest-funnel-arabic-rtl.png. No errors. Reverted to EN.
- AC6 PASS: logged in (customer@nears.com) > Access Location shows saved-address list (Home/Demo Zone, Home/Abu Dhabi) + BottomButton; funnel panel ABSENT (guest-only). Logged-in path unchanged, no overflow. Shot 06-loggedin-access-location-no-funnel.png. No errors.

## Regression / error sweep
- Dart MCP get_runtime_errors: No runtime errors found (whole session).
- logcat flutter sweep: no RenderFlex/overflow/exception/subtype error from com.izzes.nears across light/dark/Arabic/logged-in.
- Adjacent surfaces exercised: Access Location (guest+logged-in), Sign In route, guest Home, Pick Location map, Settings (dark+language). All clean.

## VERDICT: PASS — all 6 ACs demonstrated live; widget test 4/4; zero runtime errors.
