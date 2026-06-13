# NEARS-320 Regression Sweep — Live QA Progress

- Branch: feat/userapp-mvvm-v2 @ f4a7a3b7
- Device: emulator-5554 (Android)
- Backend: http://10.0.2.2:8000 (artisan serve, local multi_food_db)
- Started: 2026-06-13

## Pre-flight
- baseUrl resolves to http://10.0.2.2:8000 (real local backend) — OK, not demo
- Backend up (config 200), persistent pid 42314
- NEARS-351 seed DB-verified (read-only SELECT):
  - store 2 (zone1): items 81,82,83,85,89 present — OK
  - store 12 (zone2): items 87,88,90,92 present — OK

## Checklist verdicts (append as observed)

- Automated backstop: `flutter test` -> 796 passed, exit 0 (matches expected 796). PASS
- Item 1 (cold launch -> splash -> home): PASS. Welcome-back location sheet -> Use current location -> multi-module home (zone 1 Dhaka), module grid (Grocery/Food/Pharmacy/Parcel), 2/3 banner dots, bottom nav 5 tabs, no red screen, ui_errors empty. evidence: 01-home-multimodule.png
- Grocery module home: rails present (banners, category chips, store rails Nears Mart/Organic Paradise, Buy It Again, See All). "Good afternoon, James" = a session is already active (cached). ui_errors empty. evidence: 01-home-multimodule.png
- Item 5 (Profile/menu + logout/re-login): PASS. Profile menu renders all items (Edit Profile, My Orders, My Address, My Staples, Coupon, Settings, Earnings, Join as Delivery Partner, Open Vendor, Help & Support, Talk to Nears!, Terms/Privacy/Refund, Logout) — NO missing-widget error (NEARS-343 dead-code OK). Logout -> confirm "Yes" -> "Guest User" + "Log in/Sign up" (clean). Re-login customer@nears.com -> /api/v1/auth/login 200, user id:6 restored (order_count 39 preserved -> account NOT deleted, NEARS-344). analytics login{method:phone} PII-safe. ui_errors empty. evidence: 03-profile-menu.png, 04-after-logout.png, 05-signin.png, 07-after-login.png
- Item 7 (a11y sign-in fields): sign-in email/password EditTexts present; semantics tree shows NO duplicated field label entries (no double-announce) — consistent w/ NEARS-347. (further a11y spot-checks below)
- Item 2 (module + zone switch): PASS. grocery (08) -> food (08-food-module, restaurant items+Fresh Finds) -> pharmacy (09, Basic Medicine Nearby, no cast error this load) all load clean. Zone switch z1(Dhaka)->z2(Abu Dhabi) via saved address -> header "Deliver To: Home / Abu Dhabi", zone-2 stores (Abu Dhabi Fresh Market, Organic Shop, Stores in Marina Heights). ui_errors empty throughout. Running-order banner (#152 Pending) renders above nav (NEARS-340). evidence: 08/09/10
- Pharmacy known pre-existing basic_medicine cast error did NOT fire this load (clean).
- Item 10 (zone2 store12 re-homed items 87,88,90,92): PASS. DB SELECT confirms store_id=12 for all 4. API items/latest?store_id=12 returns 21 items incl all 4 (87 Latus, 88 Fresh Organic Tomato, 90 Premium Aromatice Atop Rice, 92 Lay's Classic Chips). Live: Search "Latus" -> result "Latus (kg) / Fresh local / 150" (store 12). evidence: 14-search-latus.png
- Item 4 (Search tab): PASS. Search tab renders Popular Categories + Suggestions + Your Last Search + Clear/Clear All. Query "Latus" -> /api/v1/items/item-or-store-search 200, results render (Item tab 1 of 2), analytics search{search_term} PII-safe. ui_errors empty. evidence: 13-search-tab.png, 14-search-latus.png
- Item 8 (i18n - partial): search Clear/Clear All render as localized English text, not raw "clear" key. (Bengali/Spanish basket check below.)
- Item 3 (store->item->add to cart->cart, qty +/-): PASS. Opened Latus item detail (Add To Cart, qty controls, Frequently Bought Together). Cross-store guard "Start a new basket?/Yes" fired correctly. Cart "Your Basket" shows Latus 1kg د.إ.150 qty 1 + Substitution Preferences + Proceed to Checkout. Increase->qty2/300, Decrease->qty1/150. Did NOT checkout. ui_errors empty. evidence: 15/16/17
- Item 7 (a11y store/item header + cart qty): PASS. Back/Share/Favourite/Cart expose content-desc + role (Button/View) + clickable; Increase/Decrease quantity = named Buttons w/ tap action. Search field content-desc="Search". Sign-in fields no double-announce. Consistent w/ NEARS-347.
- Item 9 (zone1 store2 Fresh Mart Grocery re-homed items 81,82,83,85,89): PASS. DB SELECT store_id=2 for all 5. API items/latest?store_id=2 returns 22 items incl all 5. Live: Search "Marie Frozen Meal" -> "Marie Frozen Meal / Fresh Mart Grocery / 19" (store2). Opened item, Add To Cart -> cross-store guard -> Yes -> in cart "Your Basket". Did NOT checkout. ui_errors empty. evidence: 21/22/23
- Item 6 horizontal scroll (NEARS-352): PASS. "Best Stores Nearby" rail swiped left: before=Fresh Mart Grocery/Tower Mart, after=Organic Paradise revealed. Horizontal rails scroll fine post-ScrollController removal. ui_errors empty. evidence: 26/27
- Item 6 dark mode (NEARS-353): PASS (visual). Settings->Dark Mode ON (6ammart_theme=true, switch checked=true). Home + module picker render with dark body surface (no white flash), navy header + mint accents preserved, dark category tiles/nav/order banner. Multiple load frames all dark-bodied (no white flash during load). Shimmer window sub-frame on local backend. evidence: 34/35/36
- Item 6 Arabic RTL (NEARS-353): PASS (visual). Language->Arabic. Home fully mirrored: bell left/switcher right, search icon right + Arabic placeholder right-aligned, "Fresh Finds" right-aligned w/ Sort on left, Arabic prices د.إ., product cards + badges mirrored. Bottom nav mirrored RTL: Profile(حساب) far-left -> Home(بيت) far-right (Home selected). No overflow, ui_errors empty. evidence: 40-arabic-grocery-home.png
- Item 8 Arabic basket tab: سلة التسوق (Basket) localized correctly in nav.
- Item 8 (i18n basket tab + clear tooltip): PASS. Basket bottom-nav tab: Bengali=ঝুড়ি, Spanish=Cesta, English=Basket (all match checklist), Arabic=سلة التسوق. All 5 nav tabs localized cleanly per language. Search clear (X) control = "Clear" (localized text, no raw 'clear'/'basket' key leak). Language switching via Settings->Language->Update works in all 4 langs. ui_errors empty. evidence: 42-bengali-home, 43-spanish-home, 44-english-search-clear
