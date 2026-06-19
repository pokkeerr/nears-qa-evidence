# NEARS-460 QA progress (dark-mode error tokens, UserApp DLS)
Device: emulator-5554 (Android 17/API 37) | Branch feat/NEARS-460-dls-dark-error @ c75f9cd5

## Pre-flight
- AC-5 (static): grep 0xFF000080 in nears_empty_state.dart -> 0 matches. MET.
- Code verify: dark scheme error->errorDark #FFB4AB, errorContainer->onErrorSurface #93000A, onErrorContainer->errorSurface #FFDAD6. Light scheme untouched (error #BA1A1A, errorContainer #FFDAD6). Matches spec.
- Automated backstop: 20/20 passed (theme error scheme + empty_state + menu reskin).

## Live ACs (to demonstrate)

## Live observations
- DARK MODE confirmed active: persisted 6ammart_theme=true; Settings scaffold = navyDeep #00003C (light would be #EDEDF6). main.dart line 258 uses single theme slot ternary darkTheme?dark():light().
- AC-1 (dark validation error): PARTIAL. Field LABEL + error BORDER = #FFB4AB warm pink @7.77:1 on navyContainer (theme-driven, CORRECT). BUT NearsInput helper TEXT ("Enter email...", "Please enter password") = #BA1A1A @3.05:1 navyDeep (hardcoded NearsTokens.error, line 167-190; pre-existing NEARS-394 gap, not touched by 460). Shot: ac1-dark-validation-error.png. -> regression_bug (pre-existing widget gap).
- AC-2 (errorContainer #93000A): token set correctly in dark scheme + locked by passing test, BUT zero app widgets consume colorScheme.errorContainer/onErrorContainer (grep confirms only nears_theme.dart). No live surface to paint -> UNVERIFIABLE via UI (verified code+test). Error toast uses hardcoded #334257/#FF9090; Logout button uses colorScheme.error tint (not errorContainer) and is logged-in-only (skipped per no-login rule).

- AC-3 (NearsEmptyState): live-confirmed NearsEmptyState renders correctly in DARK (ac3-dark-emptystate.png, navyDeep scaffold + gray illustration + "No item available") and LIGHT (ac3-light-emptystate.png, off-white). The CTA-bearing variant is login/backend-gated for a guest (guest-track empty needs API success-with-null but local backend 404s; address/orders CTAs login-gated), so the mint-pill+navy-text CTA is verified via code (0xFF000080 == NearsTokens.navy, value-identical) + passing nears_empty_state_test.dart (asserts mint fill + navy text in BOTH themes). Home "Claim Deal" mint pill w/ navy text rendered correctly in dark (banner CTA, same mint/navy idiom).
- AC-4 (light no-regression): CONFIRMED. Light validation error = #BA1A1A (16738 px, 0 px FFB4AB) — unchanged. Light NearsEmptyState composition unchanged. menu logout follows colorScheme.error per-mode (test-locked).
- Regression: search-empty NearsEmptyState OK both themes. 458 logout dark warm-pink tint: login-gated live, asserted by passing menu_screen_reskin_test (dark->errorDark #FFB4AB, light->#BA1A1A). No runtime errors entire session.
- Theme left in LIGHT (as found). No DB writes (track lookups read-only 404; no login).
