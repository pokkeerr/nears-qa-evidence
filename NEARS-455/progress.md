# NEARS-455 QA progress (live checkpoint)
device: emulator-5554 | branch: feat/NEARS-455-nears-logo-sweep @ e68cbeb1
backend: http://10.0.2.2:8000 (config 200)

## static pre-flight
- AC-3 grep "Images\.logo" UserApp/lib -> 0 matches (PASS)
- 5 changed files match diff; SVG assets exist + registered; flutter_svg ^2.2.3
- onnavy svg = #ffffff + #00FF99 (light); navy svg = #000080 + #00FF99 (dark-on-light)
- auth_dialog card = Theme.cardColor -> dark card + light wordmark in dark mode (visible)
- sign_up_widget logo + footer = isDesktop-gated (web-only)

## live demos
- AC-1 Support DARK (support-light.png, system shot @ dark): mint headset disc only, NO green wordmark, clean spacing, no errors -> MET
- AC-1 Support LIGHT (support-light-mode.png): navy headset disc only, NO green wordmark, clean spacing, no errors -> MET

## KEY SCOPE FINDING (blast radius)
4 of 5 changed logo-swap call-sites render ONLY on desktop/web (width>=1300 via ResponsiveHelper.isDesktop):
- auth_dialog_widget.dart: isDesktop-gated at ALL 6 call sites (menu_drawer, menu_screen, not_logged_in, order_successful, digital_payment_failed, new_pass) -> NEVER shown on mobile
- sign_up_screen.dart w125 SVG: inside _buildDesktop() only; mobile uses storefront-icon + 'nears'.tr text wordmark
- sign_up_widget.dart: isDesktop-gated branch
- footer_view.dart: web-only (no web/ platform dir in UserApp at all)
UserApp has NO web/macos/desktop platform dir; device pool is phones (448 logical px << 1300). So these 4 are NOT live-bootable in this workspace -> automated backstop + static verification only.
ONLY support_screen REMOVAL is mobile-visible -> AC-1 demonstrated live (light+dark). AC-3 grep=0.

## automated backstop
- focused (support+auth+dls auth): 79/79 passed (superset of engineer's "16"); incl tablet 1000x1300 light/dark/RTL (desktop logo render path) + support headset-disc-present + old-art-absent + RTL
- full UserApp suite: +1122: All tests passed! (0 real failures)
- 4 "EXCEPTION CAUGHT" in log = pre-existing RenderFlex overflows at footer_view.dart:190 (become-store-owner links Row) + campaign_screen.dart:82 — NOT touched by this commit (commit only changed footer_view L1/7/54 = the SvgPicture swap). Tolerated by tests. Pre-existing, unrelated to NEARS-455.

## AC-2 / UX dark-mode-visibility (auth_dialog_widget — desktop/web only, not phone-bootable)
- VERIFIED STATICALLY (only available path): dark dialog card = cardColor = NearsTokens.navyContainer #1A1A8C; dark wordmark logoOnNavy = #ffffff + #00FF99.
- white #ffffff on #1A1A8C ~= 13:1 contrast (>WCAG AAA). Wordmark CLEARLY VISIBLE, not white-on-white. UX concern resolved.
- light: logoNavy (#000080 + #00FF99) on surfaceCard #FFFFFF = high contrast.
- automated: registration_screens_render_test @ tablet 1000x1300 light/dark/RTL -> no exception / no missing-asset crash.

## AC-4 mobile auth screens (reachable)
- signup-light/dark, signin-light/dark: render clean, no overflow, no errors. (NB: mobile login/signup use a TEXT 'nears' mint wordmark, not the changed SVG — the SVG sites are all desktop/web-gated.)

## regression (live, mobile)
- sign-up <-> sign-in toggle works; Back exits cleanly; support buttons present (3 SupportButtonWidget). No errors throughout.

## device left: emulator-5554, dark mode (original state)
