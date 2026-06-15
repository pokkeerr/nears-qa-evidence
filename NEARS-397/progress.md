# NEARS-397 QA progress (live checkpoint log)

Device: emulator-5554 (Android 17 / API 37) · branch feat/NEARS-397-home-marketplace @ c5cfa556
Backend: http://127.0.0.1:8000 (302 admin) · baseUrl -> 10.0.2.2:8000 (real local). PASS pre-flight.

## Automated backstop
- flutter analyze: exit 0 — 8 info lints only (no errors/warnings). Touched-file info: item_widget.dart:115 underscore-local (cosmetic). PASS.
- flutter test: +876 All tests passed! (matches expected 876). PASS.
- includes new test/features/dashboard/bottom_nav_reskin_test.dart (141 lines).

## Scope 9 — RTL + Dark (verified early in session)
- RTL (Arabic): sector picker + grocery module + bottom nav all MIRROR correctly (notif bell logical-end/left, change-loc chevron mirrored, sector icon tiles logical-start/right, View-All links mirrored). shot 01,02. PASS.
- Dark mode: surfaces flip to dark navy; prices use sky/cyan + legible; mint promo banner + Shop-Now CTA navy-on-mint legible; bottom-nav active=mint pill navy-fill. shot 03 (settings),04 (grocery home dark EN). PASS.
- Session is GUEST (مستخدم ضيف) + zone 2 (Abu Dhabi) — useful for guest-gating.

## Module walkthrough (light, EN, zone 2 Abu Dhabi)
- GROCERY: full rail stack renders restyled (banner mint hero+Shop-Now navy CTA, categories, Buy-It-Again, item cards w/ discount+price+strike, mint ETA, '+' navy-on-mint, fav heart). shot 05. no errors.
- FOOD: Fresh-Finds grid + category strip + multiple item rows + all-stores block; search placeholder = "foods or restaurants" (CAP-B1 config gate). shots 06,07,08. no errors.
- Module switch (CAP-A2): glass tile @[15,195][111,291] -> returns to sector picker (removeModule+resetStoreData), no crash. PASS.
- Filter chips (CAP-E2): tapped Top Rated -> store list refetched/reordered; "All" selected = mint fill+navy text, unselected white+hairline. shot 08. PASS.
- Pull-to-refresh (CAP-F1): mint indicator (src home_screen.dart:206 NearsTokens.mint); fan-out ran clean, feed re-rendered. shot 09. PASS.
- Special-offer grid card (blast-radius ItemWidget): discount badge + price+strike + veg dot + fav heart + '+' navy-on-mint. shot 09. PASS.

## PHARMACY module
- Distinct rails render: New on Nears (new-on-mart, NEW badges, See All), Featured Store, Cold&Flu/First Aid (common-condition), all-stores block. shots 10,11. 
- Search placeholder = "items or stores" (non-restaurant config). 
- Skeleton-shimmer loaders confirmed during refresh (shot 11 — gray banner+circle+card skeletons). PASS scope-8.
- Mint refresh spinner visible (shot 11). Confirms CAP-F1 mint.

## CLOSED STORE TREATMENT (scope 7) — PASS
- CarePlus Pharmacy (Abu Dhabi) all-stores + New-on-Nears cards: grayscale/desaturated cover + RED "CLOSED" chip top-start (NOT black scrim, NOT mint). Card retains navy "Visit" button (tappable). shot 10. PASS.

## REGRESSION BUG (pre-existing, NOT NEARS-397) — store_card.dart 2.6px overflow
- "A RenderFlex overflowed by 2.6 pixels on the bottom" — Column @ lib/common/widgets/card_design/store_card.dart:108 (horizontal store card; pharmacy 4-row variant: name+rating/addr+ETA+address).
- store_card.dart is NOT in NEARS-397 diff (empty diff vs base 8830ac27); last touched by NEARS-266 (commit 1abbe893 "bound store_card ... no overflow" — incomplete). Cosmetic yellow-black stripe on Featured Store + New-on-Nears rails. Does NOT break a NEARS-397 AC. -> regression_bugs[].
## SHOP module — env-gated (no shop module seeded in any zone; DB-confirmed)
- modules table: grocery/food/pharmacy/parcel only (+QA single-store grocery zone 3). No shop-type.
- shop_home_screen.dart rails = same restyled shared widgets already live-verified (Banner/Category/Recommended/MostPopular/FlashSale/MiddleSectionBanner/Highlight/Brands/SpecialOffer/ProductWithCategories/JustForYou/ItemThatYouLove/NewOnMart/Promotional) — each self-hides empty. Source+suite-verified; flutter analyze + 876 tests green. Stated as env-gated.

## BOTTOM NAV — all 5 tabs (scope 4 / CAP-F5) — PASS
- Home/Categories/Search/Basket/Profile each: active = mint pill + NAVY FILLED Material-Symbols icon + navy label (NOT white-on-mint); inactive muted-white outline. shots 05,12,13,14,15. Nav height/position consistent across tabs.
- Cart badge: guest empty cart -> no badge (correct). _IconWithBadge renders count when cartList non-empty (src verified).
## NEARS-340 (scope 5 / CAP-F6) — PASS
- dashboard_screen.dart diff: persistentContentHeight math BYTE-FOR-BYTE preserved (hasRunningOrderSheet ? (iOS?110:100) : 0); enableToggle unchanged; only nav Container surface+shadow tokenized (explicit comment confirms NEARS-340 geometry untouched).
- Live zero-orders path: full session on dashboard, NO NaN crash, NO runtime errors, no invisible drag strip (persistentContentHeight:0 -> no sheet). PASS.
- Running-order-present path: env-gated (needs placed order = DB mutation, read-only QA). Math preserved + new bottom_nav_reskin_test.dart (4 cases incl. cart-badge) green in 876 suite. Stated.
## SHARED-CARD BLAST RADIUS (scope 6) — PASS
- store-detail (City Care Chemist): restyled grid+row cards, All Products grid/list toggle, filter chips (All=mint), Recommended rail. shot 16. no errors.
- Categories tab: restyled grid item cards (mint ETA, navy-on-mint discount + '+', fav heart). shot 12.
- Search results ("Mask"): restyled row cards, fav heart logical-START (top-left of thumb), navy price+strike, navy-on-mint '+', diagonal mint discount ribbon, Item/Stores toggle. shot 17.
- Cart (empty): clean empty state. shot 14.
- Grid rating star = NearsIcon('star', NearsTokens.warning=#B8530B amber, filled) + NearsText (Inter) — src item_widget.dart:313. PASS scope-6.

## GUEST-GATING + APP BAR (scope 3) — PASS
- Session=GUEST: greeting/visit-again/promo-code correctly ABSENT (src grocery_home_screen.dart:25/42/48 isLoggedIn?...:SizedBox). Logged-in-shows side = source-verified (login text-entry blocked by Flutter/adb friction; auth is NEARS-396 surface, Done). 
- NO LOGIN WALL: "CONTINUE AS GUEST" on login + home fully reachable as guest. PASS.
- Notification bell: navy-glass + NearsIcon('notifications') + MINT unread dot (hasNotification-gated; guest=no dot). src home_screen.dart:462. PASS.
- Location selector state (i) address-set "Deliver To: Your Location" live; tap->location screen wired. State (ii) "select location" = source-gated (session has address).
## Location selector live + flash-sale gate
- Location selector LIVE-INTERACTIVE: changed to "Deliver To: Others" mid-session (deliver-to/address change wired -> zone/feed re-resolve). State(ii) "select_your_location"+CustomToolTip source-verified.
- Flash-sale (CAP-D7): gated activeProducts!=null && duration>1s + FlashSaleTimerView countdown (src). No active flash-sale seeded zone-2 -> correct self-hide.

## FINAL ERROR SWEEP — clean for NEARS-397 surfaces
- DTD runtime errors + logcat across full session: NO Flutter exceptions / subtype / GetX / NaN-Infinity crashes.
- TWO RenderFlex overflows, BOTH in files NOT in NEARS-397 diff (pre-existing/out-of-scope):
  1. store_card.dart:108 — 2.6px bottom (horizontal store card; pharmacy 4-row variant). Last touched NEARS-266. -> regression_bug.
  2. sign_in_screen.dart:212 — 1px bottom, ONLY with keyboard open (auth "Nears" wordmark, NearsText.display w800 fallback). NEARS-396 surface. -> regression_bug (cosmetic).
- ZERO errors attributable to NEARS-397 files (item_widget/store_card_with_distance/bottom_nav/home_screen/banner/item_that_you_love/not_available/dashboard).

## VERDICT: PASS
