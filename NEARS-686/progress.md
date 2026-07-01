# NEARS-686 + NEARS-687 QA progress (device emulator-5558, worktree feat/NEARS-686-hygiene-batch @8ec2a845)

VERDICT: PASS (both tickets). Light mode only (dark deferred per light-first policy).

## NEARS-686 (cached-location boot-log hygiene)
- AC1 (no-cache boot): PASS. 4 fresh (pm clear) boots -> onboarding -> guest home. featuredHeader() executed
  (banners?featured=1 + stores/get-stores/all?featured=1 both 200) and getAddressFormSharedPref() ran at init;
  ZERO "cached location parse failed" warns, zero [WARN] of any kind from app. See ac1-no-cache-boot.log.
- AC2 (happy path + relaunch): PASS. Saved Abu Dhabi address (zone 400). Relaunch applies cached lat/lng
  (get-zone-id?lat=24.4538817&lng=54.3773417, inZone=true), sectors_shown zone_id:400, home renders, featured
  200s, no parse warns, get_runtime_errors clean. alreadyInApp:true branch = pure refactor; in-app login trigger
  blocked by icon-only nav (tooling gap). See ac2-saved-address-relaunch.log.
- AC3 (corrupt cache): UNTESTED (optional). run-as/SELinux sandbox on the Android-16 emulator blocked seeding a
  corrupt userAddress (write denied via cat> and cp). Behavior preserved by inspection: the try/catch+AppLogger.warn
  is unchanged, now gated behind `cached != null && cached.isNotEmpty`.

## NEARS-687 (WebNewOnShimmerView RTL)
- AC4 (RTL shimmer mirror): PASS via authoritative widget test (3/3, incl. rtlLeft>ltrLeft) + code
  (PositionedDirectional start:15, EdgeInsetsDirectional start:95) + live Arabic RTL home renders correctly
  (title right, See-All/chevron left, cards RTL, no RTL crash). LTR home unchanged (EN reference + directional==physical
  in LTR + test LTR case). NOTE: the transient WebNewOnShimmerView null-window could NOT be caught on-device (rails
  prefetch during splash; pull-to-refresh retains data; See-All uses a different vertical shimmer) — capture-timing
  limitation, not a defect. See ac4-rtl-widget-test.log + ac4-arabic-rtl-*.png.
- AC5 (heart top-trailing untouched, NEARS-672 parity): PASS. WebNewOnShimmerView heart = Positioned(top:15,right:15)
  UNCHANGED by diff; byte-identical to NEARS-672 non-web NewOnShimmerView (lib/common/widgets/item_view.dart:135).
  Light mode verified; dark deferred per light-first policy.

## Automated backstop
- flutter test web_new_on_shimmer_rtl_test.dart -> 3/3 PASS.
- Full UserApp suite -> 1730/1730 PASS.

## Regression (bounded): CLEAN
- featuredHeader consumers store_repository + banner_repository -> featured requests 200 with correct zone 400
  (guest/no-cache boot AND saved-address boot). Home rails render EN + AR. No boot crash on either cache state.
- Pre-existing (NOT this change): guest-boot 401/403 on cart/info/coupon/notifications/running-orders + cm-firebase-token
  302, each with paired [FAIL] log (logging contract honored). just_the_tooltip unmounted-State exception on fast nav.
