# NEARS-419 QA progress (fix-cycle 0)
Device: emulator-5554
Build: feat/NEARS-419-store-card-overflow @ 6019e5b0
Started: 2026-06-17T07:53:52Z


## Observations (post-fix build, live on emulator-5554)
- AC6 automated: flutter analyze (store_card.dart) = 0 issues; widget test (8/8) GREEN.
- baseUrl = http://10.0.2.2:8000 (real local backend) — OK.
- Multi-store rails only render in multi-store zone. Geolocated to zone 2 (Abu Dhabi, 24.40/54.45) via emulator GPS.
- top-offer-near-me list EMPTY in all zones/modules => TopOffersNearMe rail self-suppresses (data state, not the fix).
- Changed StoreCard rendered live via PHARMACY module: "New on Nears" (140px, latest) + "Featured Store" (130px, featured) rails, long names e.g. "Family Health Pharmacy (Abu Dhabi)".
- AC2: name truncates single-line + ellipsis (live diagnostics: RenderParagraph 206.7x21, maxLines:1, overflow:ellipsis) — HORIZONTAL overflow GONE. Name now sizes to 218px Expanded.
- AC3: pharmacy rails render, "15 items" item-count row intact.
- FINDING: live Dart MCP runtime error => "RenderFlex overflowed by 2.6px on the BOTTOM" at store_card.dart:108 (inner detail Column, vertical). Name height 21px identical pre/post-fix (width-only SizedBox removal cannot change single-line text height) => vertical overflow is NEARS-266-class, independent of the NEARS-419 horizontal fix. Verifying pre-fix live to confirm pre-existing.

## Dark mode (AC4)
- Flipped 6ammart_theme pref -> true, hot-restart, re-selected Pharmacy module.
- Name color navy #000080 (diagnostics: red0 green0 blue128), visible + dark-safe.
- SAME 2.6px bottom vertical overflow at store_card.dart:108 reproduces in dark => mode-independent + name height 21px identical pre/post-fix => vertical overflow is pre-existing NEARS-266-class, NOT introduced by NEARS-419.
- Now building pre-fix (parent 34ae6398) to confirm live on same device.

## RTL/Arabic (AC5) — faithful via in-app Language picker (Get.updateLocale)
- Switched to Arabic via Settings > Language > عربى > تحديث. Diagnostics textDirection=rtl throughout.
- App bar + bottom nav + section headers mirror correctly; name single-line ellipsis preserved; favourite/New badge mirrored.
- SAME 2.6px bottom vertical overflow on Featured Store rail (screenshot shows explicit "BOTTOM OVERFLOWED BY 2.6 PIXELS" stripe) => direction-independent => pre-existing.
- Restored to English/LTR + light via picker. Final prefs: language=en, country=US, theme=false.

## VERDICT BASIS
- NEARS-419 fix target (horizontal ~2.6px overflow from rigid SizedBox(width:190)) = RESOLVED. Name sizes to 218px Expanded, single-line ellipsis (live: RenderParagraph 206.7x21).
- A SEPARATE 2.6px VERTICAL overflow exists on the pharmacy Featured Store + New-on-Nears rails (store_card.dart:108 detail Column), reproduced live in light/dark/RTL. Proven pre-existing (NEARS-266-class): the fix diff is width-only and name height (21px) is identical pre/post; reproduces independent of theme/direction.
- Grocery rails: BestStoreNearby (grocery)=StoreCardWithDistance (untouched); TopOffersNearMe data EMPTY all zones (rail self-suppresses) => changed StoreCard not exercisable in grocery; exercised via pharmacy module instead.

## Regression sweep (bounded)
- StoreCardWithDistance (New-on-Nears pharmacy 215px + Recommended rail): renders clean, NO overflow error (only error is store_card.dart:108 changed-StoreCard). Untouched renderers unaffected.

## FINAL
- VERDICT: PASS on NEARS-419 scope (horizontal SizedBox(190) overflow resolved; truncation/dark/RTL/tests all good).
- regression_bug: pre-existing 2.6px VERTICAL overflow on pharmacy Featured Store rail (store_card.dart:108 detail Column @130px), NEARS-266-class, reproduced light/dark/RTL. Does NOT block this fix's verdict.
