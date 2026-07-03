# NEARS-743 QA — RTL directional-geometry fix (light mode only; dark deferred)
Device: emulator-5560 | Branch: fix/NEARS-743-rtl-directional @ b7ac0186 | Backend: 127.0.0.1:8000 (api/v1/config 200)

## AC verdicts
- AC1 (store card RTL logo-right, no overlap): PASS — LIVE. Pharmacy stores-near-you (StoreCardWithDistance fromAllStore:true). Logo on RIGHT (leading), names left-indented, no overlap. Also LTR mirror shown (logo LEFT). Evidence: AC1-storecard-rtl-logo-right-nooverlap.png (06), AC3-storecard-ltr-logo-left-nooverlap.png (13).
- AC2 (registration + tab bars): PASS.
  - Part2 (step TabBars anchor RIGHT under RTL): LIVE — store reg (Vendor/Owner + English/Arabic tabs) + DM reg (General/Additional). Evidence 07,12.
  - Part1 (TIN/doc delete icon on trailing/left, clear of file icon): TEST-SUBSTANTIATED + code-verified (PositionedDirectional end:0 + Row w/ 35px reserved gap) + upload-preview mechanism live-verified (logo/cover). Live TIN upload gated behind deep multi-field onboarding validation wall.
  - Part3 (Orders tab bar anchor RIGHT): TEST-SUBSTANTIATED — changed Align is in _buildDesktop (desktop/tablet-only, not rendered on phone); contract test proves AlignmentDirectional.centerStart -> centerRight under RTL.
- AC3 (LTR pixel-identical regression): PASS — LIVE. Store card (logo LEFT), store reg tabs (anchor LEFT), all-store filter chips (LEFT), item bottom sheet — all byte-identical legacy layout under English.

## Logs
2x [FAIL] endpoint=/api/v1/config/get-zone-id http_status=404 at STARTUP only (pre-existing backend/env; properly logged w/ correlation_id; NOT triggered by any AC action). 0 [ERR], 0 RenderFlex overflow. All ACs logs-clean for scoped actions.

## Backstop
flutter test store_card_rtl_logo_overlap_test.dart + rtl_directional_geometry_test.dart = 7/7 PASS (overlap test fails on pre-fix physical-left logo).
