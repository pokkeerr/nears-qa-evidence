# NEARS-454 QA progress (live checkpoints)

- Device: emulator-5554 (lock acquired)
- Branch: feat/NEARS-454-support-hero @ 8e155acf
- baseUrl: http://10.0.2.2:8000 (Android local backend) — OK
- _names['headset_mic'] -> Symbols.headset_mic confirmed in source; not in _directional (no RTL mirror)

## Automated backstop (PASS)
- flutter analyze (3 changed files): No issues found! (zero new)
- flutter test test/features/support/support_screen_render_test.dart: All 6 tests passed
  - 4x size×mode render guards (hero glyph present, no supportImage Image.asset, disc=primaryColor@0.10, not navy literal)
  - _names('headset_mic') -> Symbols.headset_mic; Symbols.help findsNothing
  - RTL no-exception

## Live demonstration (Android emulator-5554, debug build, zone 2)
- AC1 PASS (light): Hero = navy-tinted disc + navy headset_mic glyph. NO orange "SUPPORT" wordmark, NO help-fallback question mark. supportImage Image.asset absent from live widget tree (count=0). Shot 01-support-light.png.
- AC2 light PASS: disc navy tint + glyph navy.
- AC4 content: help_support section header + 3 contact rows (Address / Call +971565811159 / Email Us admin@admin.com) present; ui_errors clean.
- FINDING (regression_bug, pre-existing, NOT this change): logo below hero is 6amMart green stock logo (Images.logo), not Nears brand logo. Diff did not touch the logo line; out of scope for NEARS-454. Does not affect verdict.

- AC2 dark PASS: disc mint tint + glyph mint, dark-safe (no navy literal bleed). Shot 03-support-dark.png.
- AC3 RTL/Arabic PASS: headset glyph NOT mirrored (headset_mic not in _directional), disc centered, layout intact (rows mirror, chevrons left, text right-aligned), ui_errors clean. Shot 04-support-rtl-arabic.png. EN+light restored after (05-support-light-restored.png).
- AC4 PASS: Call row -> tel: launcher fired, Google Dialer foregrounded (NO call placed), backed out clean. Shot 06-call-dialer-launched.png. Email row -> mailto: fired, Gmail ComposeActivityGmailExternal launched. Shot 07-email-gmail-launched.png.
- AC4 content rows: Address/Call/Email present in EN, AR, light & dark; section header present.
