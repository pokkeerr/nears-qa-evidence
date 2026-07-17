AC log start 2026-07-17T17:16:18Z

## AC1 (Android) — PASS
- Store: Eco Market (id 19, zone 2), rating pill shows 3.4 (avg of 5 reviews)
- Rating pill node: content-desc="تقييمات المتجر\n3.4" (Store reviews) clickable=true bounds[1119,879][1299,1011]
- Tap (label-resolved "تقييمات المتجر") -> navigated to ReviewScreen for Eco Market (3.4/5, 5 ratings/reviews, "NEARS-1038 QA rating-spread fixture" review by James Wilson)
- Logs: 0 [FAIL]/[ERR], 0 exceptions/overflow. CLEAN
- Evidence: ac1-01-before-store-header.png, ac1-02-after-reviews-screen.png

## AC3 (Android) — regression checks
- Back from Reviews -> returns to Eco Market store detail: PASS
- Meta node "Eco Market\n2-5 days\n9.1 كم" clickable=FALSE (name/ETA/distance NOT tappable): PASS
- Only rating pill clickable=true: PASS (scope guard)
- Circle buttons all clickable in a11y tree + functional:
  - Back: works (returns from Reviews/search)
  - Search (يبحث): opened in-store search screen
  - Share (يشارك): opened Android share chooser w/ store deep-link
  - Favourite (مفضل, header [45,333][177,465]): toggled, "view list" snackbar
- Logs: 0 [FAIL]/[ERR]
- NOTE (non-blocking): share URL uses old demo host 6ammart-web.6amtech.com — pre-existing config, unrelated to this ticket

## AC3 unrated store — PASS
- Morning Mart (id 20, NULL rating): pill shows "جديد" (New), clickable=true, bounds[1108,879][1299,1011]
- Tap New pill -> ReviewScreen for Morning Mart, empty state "لم يتم العثور على أي مراجعة" (No review found). No crash/blank. (empty state = NEARS-1115 domain)
- Evidence: ac3-01-new-store-header.png, ac3-02-new-store-reviews-empty.png

## Blast radius — PASS
- Header renders: cover/gradient, logo, name, rating pill, ETA pill, distance sub-line all present (Eco Market + Morning Mart)
- Collapse-on-scroll: header collapses, store name persists in appbar, no RenderFlex/overflow, no new [ERR]

## AC2 (iOS) — BEST-EFFORT / platform-parity by shared code
- iOS build BLOCKED by CocoaPods env issue (specs repo out-of-date + unbuilt ffi gem) — toolchain, NOT ticket code
- Nav code is platform-agnostic Flutter/GetX (Get.toNamed + RouteHelper); widget test (platform-agnostic) passes 11/11
- Demonstrated live on Android; iOS parity by shared code
- Evidence: ios-build-blocked-cocoapods.log

## Pre-existing regression (NON-BLOCKING)
- [ERR] checkout: distance parse failed — CheckoutController.getDistanceInKM (checkout_controller.dart:707): "type 'String' is not a subtype of type 'int'", straight-line fallback. Unrelated to store-header change. Properly logged (not silent).
- Evidence: bug-checkout-distance-parse.log

## Automated backstop — PASS 11/11
flutter test test/features/store/nears_store_header_sliver_test.dart
