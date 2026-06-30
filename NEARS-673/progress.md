# NEARS-673 QA progress (live, append-as-observed)
Device: emulator-5556 | worktree: nears-NEARS-673-logout-pii | branch feat/NEARS-673-clear-on-logout-pii @413874b0
User A = Customer Nears id6 +971565811199 (44 orders, 2 addr) | User B = QA SingleStore id409 +971500000263 (1 addr, 0 orders)

## A-state SEEDED (before logout) — all observed live:
- Login A: greeting "Good morning, Customer" + "Buy It Again" rail. prefs: user_number=565811199, user_country_code=+971 (remember-me ON).
- AC1 Checkout: _address = A "R989+PPW, Dhaka 1216" (Others). [AC1-userA-checkout.png]
- AC2 Address: A 2 addresses Abu Dhabi + Demo Zone Dhaka, "2 delivery spots". [AC2-userA-addresses.png]
- AC3 Wallet: token NOT minted on plain open (needs Gateways add-funds redirect = absent). pref absent both before+after. End-state + unit-test + flag.
- AC4 Remember-me: user_number/country_code stored. [AC4-baseline-signin-fresh.png]
- AC5 Location: 6ammart_user_address pref present (A coords) + map picker opened. [AC5-userA-map-picker.png]
- SEC-1 Orders: A 44 orders (#160,#159,#154,#153). Order #160 detail shows +971565811199 + Customer Nears + Abu Dhabi. [SEC1-userA-orders.png, SEC1-userA-order160-detail-PII.png]
- SEC-3 Search: searchHistory=["MilkRiceCola","MilkRice","Milk"], shown as suggestions. [SEC3-userA-search-history-suggestions.png]
- No runtime errors during A seeding (ui_errors clean).

## B-state VERIFIED (after menu/Profile-tab logout of A, login as B) — ZERO A residue:
- SEC-2 profile/greeting: B menu = "QA SingleStore", Orders "0", Joined 07 Jun (A's Customer Nears/44 GONE). [SEC2-userB-profile-no-A-identity.png]
- SEC-1 Orders: "No orders yet" — no A #160/#159/#154. [SEC1-userB-orders-empty.png]
- AC2 Address: only "Tower A, Single Store QA Zone" (1 spot) — A Abu Dhabi/Dhaka GONE. [AC2-userB-addresses-only-B.png]
- AC3 Wallet: 0 AED, "No transactions yet", wallet-token pref absent. [AC3-userB-wallet-fresh.png]
- SEC-3 Search: only Popular suggestions, no Milk/Rice/Cola, pref=empty-list[]. [SEC3-userB-search-no-history.png]
- AC4 sign-in field EMPTY post-logout (no 565811199 pre-fill). [AC4-signin-empty-after-logout.png]
- AC5 Location: 6ammart_user_address cleared; B re-prompted "Select Your Location" (not A coords); B context = B Tower A / fresh GPS.
- AC1 Checkout: B cart EMPTY (A Mango/Cola/Rice gone); _address/contact cleared (code+unit test); B's checkout FORM not renderable live (all stores CLOSED ~1am, no addable item) — FLAGGED.

## Regressions:
- Guest-after-logout: registration renders (NOT blank) [REG-guest-after-logout-registration-renders.png] + guest home + guest basket "Your cart is empty" render, no errors. SmartManagement.onlyBuilder blank-screen mode does NOT occur. PASS.
- Re-login restores data: login A again -> "Customer Nears" + 44 orders + 2 addresses re-fetch [REG-userA-relogin-data-restored.png]. Clear is session-scoped, not permanent. PASS.
- Drawer logout (endDrawer MenuDrawer, menu_drawer.dart:138) + 401 (api_checker.dart:43) + account-delete (profile_controller.dart:146) all call SAME clearSharedData seam -> clear identically (orchestration unit test + code).

## Logs: ui_errors clean, no [FAIL]/[ERR]/exception, no Dart runtime errors, NO PII (phone/name/token) in logs across whole session.
## Automated: flutter test (6 NEARS-673 files) = 15/15 PASS.
## VERDICT: PASS (AC1 + SEC-2 live caveats flagged; covered by shared-seam ran live + 15/15 unit tests).
