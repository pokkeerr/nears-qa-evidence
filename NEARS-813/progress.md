# NEARS-813 QA progress

Device: emulator-5556 (Pixel_10_Pro_3 AVD, spare booted — 5554 was occupied-without-lock)
App: VendorApp, worktree /Users/Apple/Projects/nears-NEARS-813-vendorapp-smartmanagement
Backend: local php artisan serve :8000 (already running), config endpoint 200 OK

## AC1 - SmartManagement.onlyBuilder set
PASS (code spot-check) - get_di.dart line ~172 `Get.smartManagement = SmartManagement.onlyBuilder;` before any registration; main.dart GetMaterialApp `smartManagement: SmartManagement.onlyBuilder`. Confirmed via `git show d0c0810f6`.

## AC2 - Order details -> back -> home round-trip
Logged in as ahmed.khan@demo.com. Home showed orders #91175, #91176. Tapped #91175 -> Order Details screen loaded (Customer Nears, Tomato item, 5.67 AED, Pending). Back button -> Home screen restored intact, same 2 orders, no stale flash, no crash. logcat clean (no [FAIL]/[ERR]/Exception/FATAL).
PASS

## AC3 - Cross-nav controller-persistence sweep
Path: Home -> My Orders (bottom nav) -> Menu -> Store Config -> back -> Menu -> Edit Profile -> back -> Menu -> Conversation (chat) -> back -> Home.
- My Orders: full order list (#157, #91111, #91172, #91175, #91176) loaded via OrderController, correct.
- Store Config: StoreController loaded correct store settings (Halal Tag, Home Delivery, Take Away, Schedule Order toggles).
- Edit Profile: ProfileController showed correct data for logged-in vendor (Ahmed / Khan / ahmed.khan@demo.com).
- Conversation: chat list loaded (Customer Nears thread).
- Back to Home: correct orders restored, no stale flash.
No crash anywhere, no frozen/broken screen state, logcat clean throughout (no [FAIL]/[ERR]/Exception/not found).
PASS

## AC4 - Core-flow regression
Cold start (fresh flutter run install) -> notification permission dialog -> language chooser (English) -> Sign In screen -> login as ahmed.khan@demo.com -> Home (splash/init completed cleanly, home shows orders). Repeat profile visits (Edit Profile viewed twice across two different accounts) both showed correct, non-stale data each time. Orders list (My Orders tab) and order detail both loaded correctly.
PASS

## AC5 - flutter analyze clean of NEW issues
Ran `~/Tools/flutter/bin/flutter analyze VendorApp` (pinned SDK). Result: 16 issues found (5 unused_local_variable/unused_field warnings, 2 dead_code warnings, 8 avoid_print info, 1 deprecated_member_use info) - matches engineer's claim of 16 pre-existing issues, 0 new. Spot-checked file list: custom_text_field_widget.dart, home_screen.dart, invoice_dialog_widget.dart, running_order_body_widget.dart, profile_repository.dart, customer_review_screen.dart, store_repository.dart, all_items_screen.dart, store_screen.dart, store_settings_screen.dart - none touched by the NEARS-813 diff (get_di.dart, main.dart only).
PASS

## Logout/account-switch check (flagged regression-candidate, not a numbered AC)
Method: logged out from ahmed.khan@demo.com (grocery store, store_id ~ Store A) via Menu -> Logout -> Yes, in the SAME app session (no kill/restart). Signed in as a second, DIFFERENT vendor account, demo.store@gmail.com (store_id 1, different module/store) - note: countryfair@demo.com (originally selected 2nd account) turned out to be a SUSPENDED account server-side (auth-002, confirmed via direct curl to /api/v1/auth/vendor/login), unrelated to this ticket - substituted with demo.store@gmail.com after confirming it's active via curl.
- Home screen after switch: correct NEW account orders (#91179, #91182, 13 total orders) - not ahmed.khan's #91175/#91176.
- Edit Profile after switch: correct NEW account data ("Demo" / "Store" / demo.store@gmail.com) - not "Ahmed"/"Khan"/ahmed.khan@demo.com.
- Repeated the switch in reverse (demo.store -> logout -> ahmed.khan) with 5x rapid-fire back-to-back accessibility-tree dumps captured immediately after the Sign In tap and again immediately after landing on Home/Edit Profile (no settle delay) specifically to try to catch a transient stale-data flash. All captures showed either the in-flight "Loading..." button state or already-correct ahmed.khan data (#91175/#91176 orders; "Ahmed"/"Khan"/ahmed.khan@demo.com profile fields) - never demo.store's leftover data.
- Root-cause read of the code explains why: `_login()` in sign_in_screen.dart awaits `ProfileController.getProfile()` (or TaxiProfileController for rental) BEFORE calling `Get.offAllNamed(RouteHelper.getInitialRoute())` - so by the time Home/Menu mounts, `_profileModel` has already been overwritten with the new account's fetched data. Home's own initState also re-calls `ProfileController.getProfile()` and OrderController's list-fetch on mount, refreshing further.
- Caveat: this test cannot rule out a sub-frame (<~100-200ms, faster than one uiautomator dump cycle) flicker with absolute certainty - accessibility-tree dumps sample discrete points in time, they do not record every rendered frame. But across 2 directions and ~8 total capture points (including deliberately-early ones), no stale flash was observed, and the code path explains why none should occur.
VERDICT: PASS (no observable stale-data flash; latent-bug concern investigated live and not confirmed as a defect under this test methodology).
