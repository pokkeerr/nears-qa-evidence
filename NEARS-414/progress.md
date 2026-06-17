# NEARS-414 QA progress (theme reverts to light on locale switch)
Device: emulator-5554 (Pixel_10_Pro) | branch feat/NEARS-414-theme-locale-race @ ecf7a38c
Started: 2026-06-17

## AC checkpoints (appended as observed)

- AC6 automated: theme_controller_test.dart 3/3 GREEN; flutter analyze theme_controller.dart 0 issues. PASS
- AC1 (EN->AR, dark): enabled Dark Mode (02-settings-dark-on.png dark navy + mint toggle ON), switched EN->AR (03-dark-after-EN-to-AR.png). App STAYED dark, RTL applied, Dark Mode toggle still ON. No flash to light. PASS so far.
- AC1 (AR->EN, dark): switched AR->EN, stayed dark, toggle still ON (04-dark-after-AR-to-EN.png). AC1 PASS both directions. No runtime errors (DTD).
- AC2 (light, EN<->AR both): light mode preserved through EN->AR (06) and AR->EN (07); Dark Mode toggle stayed OFF. AC2 PASS both directions.
- AC3 (dark cold restart): enabled dark, force-stop com.izzes.nears, cold relaunch. First Flutter frame (splash) = dark navy lum 8 (09-coldstart-dark-firstframe.png), settled Home dark (10). White native-splash frame is OS-level, theme-independent; no light Flutter flash. PASS (dark half).
- AC3 (light cold restart): disabled dark, force-stop, cold relaunch. First Flutter frame (splash) = light cream lum 247 (12-coldstart-light-firstframe.png), settled light (13). No dark flash. AC3 PASS both halves. Contrast proves fix: dark-persist first-frame lum 8 vs light-persist lum 247.
- AC4 (rapid toggle + immediate locale): from light, toggled Dark Mode 5x rapidly -> ended DARK with toggle ON (14). Immediately switched EN->AR: stayed DARK, toggle still ON, RTL (15). Last-toggled state in sync, no stuck/inverted. AC4 PASS.
- AC5 (map-style regression): opened address map picker in DARK (16/16b) and LIGHT (17). Both render + lay out without crash; app chrome correct per theme. Map screens consume `style: Get.isDarkMode ? ThemeController.darkMap : lightMap` (grep: order_tracking, traking_map_widget, map_screen, pick_map_screen, add_address, delivery_eta_banner, nears_map_preview). _loadCurrentTheme() async JSON load UNCHANGED by fix; no flutter exceptions / "Unable to load asset". Tile TINT not visually confirmable: Google Maps tiles blocked on emulator by GoogleCertificatesRslt:not allowed (pre-existing API-key/cert env issue, affects all builds). AC5 met w/ env caveat — regression concern (async map load intact) fully answered: yes.
