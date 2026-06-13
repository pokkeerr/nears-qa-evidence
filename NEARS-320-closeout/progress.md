# NEARS-320 closeout — QA progress checkpoint

Device: emulator-5554 (Android 17 / API 37), branch fix/NEARS-320-closeout (working tree on feat/userapp-mvvm-v2 tip 871afe0b; fixes are uncommitted working-tree changes).
Backend: php artisan serve :8000 (HTTP 302 admin, config API 200), queue:work running. baseUrl resolves http://10.0.2.2:8000 (real local backend, NOT demo).

## Observed verdicts (as demonstrated)
- NEARS-343 (dead code) PASS — app builds+launches; home renders all rails; Profile tab (menu_screen) renders fully (Edit Profile/My Orders/Settings/etc.), no missing-widget error. No runtime errors. Shots 01,02.
- NEARS-352 (ScrollController removal) PASS — home rails (Recommended/store rails) render + scroll horizontally; vertical+horizontal swipes clean, zero runtime errors. Shots 03,04. (Named rails Popular/NewOnMart/TopOffers are zone-2 data-dependent; PopularStoreView confirmed present in widget tree.)
- NEARS-347 (a11y) PASS — a11y tree (uiautomator, reflects Flutter Semantics):
    * Search field: accessible name "Search" (non-empty); degenerate unlabeled node gone. Shot 01.
    * CartCountView: "+"=Add (Button), "-"=Remove (Button), both clickable/non-silent; initial=Add To Cart (Button). Shot 06.
    * Sign-in email+password: NO doubled announce — zero "X X" patterns on screen; fields clean single label. Wrapper bug reverted. Shot 07.
    * Store header: Back/Search/Share = Button role + name; Favourite = Switch role + selected state (toggled). Add To Cart = Button. Shot 05.
- NEARS-348 (i18n) PASS — in-app Language switch (LocalizationController, .tr):
    * Bengali: cart bottom-nav tab a11y desc = "ঝুড়ি" (not raw 'basket'). Shots 10,10b.
    * Spanish: cart bottom-nav tab a11y desc = "Cesta". Shot 12.
    * English (initial boot): "Basket" (unchanged). Shot 01.
    * clear key: search clear (X) tooltip localized "পরিষ্কার করুন" in bn, NO raw 'clear' leak. Shot 11.
- NEARS-353 (RTL + shimmer + dark) PASS:
    * RTL (Arabic): home rails mirror — leading padding on right, RTL card flow, headers right-aligned, bottom nav mirrored (shot 13). Store-detail expanded hero padding mirrors (EdgeInsetsDirectional.fromSTEB) — shot 15.
    * Dark-mode shimmer: categories + grocery-module banner/category/popular shimmer render in dark grey (theme cardColor/disabledColor), NO bright white flash (shots 19,21). Rounded corners (radiusDefault) match loaded card.

## RE-VERIFY (3 already-fixed)
- NEARS-350 (grocery zone-2 no flash-sale crash) PASS — Grocery & Food module home loaded in zone 2 (Abu Dhabi); Daily Essentials + store rails render; no flash-sale section, no red screen/NPE, zero runtime errors. Shot 22.
- NEARS-349 (checkout validation snackbar) PASS — logged in (james.wilson@demo.com), went to Checkout, tapped Place Order with no payment selected / store closed → error snackbar "Store is closed" (X icon) rendered above the button (NOT silent). App logs show "===> Place Order BUTTON CLICKED" handler fires. Shots 28,29.
- NEARS-344 (logout does NOT delete account) PASS — logged in as James Wilson (user id=1, DB confirmed pre-test). Profile > Logout > "Are you sure you want to log out?" Yes -> returns to "Guest User / Log in/ Sign up". DB AFTER logout: row james.wilson@demo.com STILL EXISTS (id=1, same phone); user_count unchanged (7). Re-login with same creds -> "James Wilson, Joined 01 Mar 2026". Account intact. Shots 30-33.

## Automated backstop
- flutter test (UserApp): All tests passed! (796 tests green). No regressions.

## Regression sweep
- Home loads all rails (clean). Cart add/remove works (+ -> 2, - -> 1). Normal login works (james.wilson). Module switch (Food/Grocery) clean. Zero runtime errors throughout.

## Drift noted
- Splash screen still shows unrebranded "6amMart" logo (pre-existing rebrand gap, out of scope). Frame 20.
- DeliveryApp (com.izzes.nearsdelivery) was installed on the pool device and briefly grabbed foreground after a launcher tap; UserApp is com.izzes.nears. No impact on QA.
