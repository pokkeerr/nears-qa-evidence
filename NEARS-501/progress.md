# NEARS-501 QA Progress — floating glassy icon-only bottom nav

Device: emulator-5554 (API 37, skiagl HW renderer) · branch feat/NEARS-501-bottom-nav-floating-glassy @ 3a1e30e6
Backend: http://10.0.2.2:8000 (config 200) · seed customer w/ running order #158 + cart (1 item)

## AC verdicts (live)
- AC1 floating inset — PASS. L/R inset 48-75px (~16-18dp), bottom inset above gesture bar; not edge-to-edge on Home/all tabs. shot: ac1-ac16-home-nav-with-running-order-banner.png
- AC2 rounded + frosted glass + shadow — PASS. 24dp corners; fill is backdrop-blended navy (light 40,40,147 / dark 2,2,111) NOT pure const #000080 => BackdropFilter compositing on skiagl HW renderer; visible drop shadow (F1 fix renders). shots: ac1/ac2-blur*
- AC3 icon-only 5 tabs — PASS. No text labels, no oversized pill. all shots
- AC4 active mint / inactive muted — PASS. active Home = 1941 mint px (#00FF99); inactive = muted-white outlined. sampled
- AC5 basket badge — PASS. mint badge "1" top-trailing of basket icon inside floating card when cart non-empty; hidden@0 covered by widget test AC6-9. shots
- AC6 matches target (labels omitted, owner decision) — PASS.
- AC7 no nav regression — PASS. all 5 tabs route correctly (Home/Categories/Search/Basket→cart/Profile→menu_screen); back-press from Profile → Home page0. shots ac7-*
- AC8 dark + RTL — PASS. dark fill more transparent, mint legible; RTL mirror (Profile leftmost, Home rightmost), badge flips top-LEFT; no overflow. shots ac8-*

## Regression
- location-suggestion flow: nav correctly HIDDEN (first boot shot)
- keyboard-open hide: emulator built-in HW keyboard gives 0 IME inset → can't trigger soft-kbd inset live; verified STRUCTURALLY (gating unchanged from NEARS-340) + noted
- desktop hidden: structural (isDesktop gate unchanged) — phone emu always mobile
- NEARS-340 banner #158: 300px clear gap between banner content bottom and nav top → NOT clipped. PASS
- a11y: each tab content-desc=label, selected=true on active, clickable=true (excludeSemantics+onTap re-expose works)
- back-press double-exit: structural (PopScope _canExit snackbar intact)

## Automated
flutter test: 1215 passed (incl. 7 NEARS-501 bottom-nav cases). DLS file: 23 passed.
