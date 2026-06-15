# NEARS-399 re-QA progress (fix_cycle 2)

Device: emulator-5554 (Android 17 / API 37)
Branch: feat/NEARS-399-store-detail @ 9e0d2bab
Backend: http://127.0.0.1:8000 (api 200, baseUrl=10.0.2.2:8000)

## AC1 cover-photo hero (Organic Paradise, store 3, grocery, unrated)
- 01-hero-cover-organic-paradise.png: cover photo backdrop + navy scrim + floating glass buttons (back/search/share/fav) + bottom-anchored mint-ring logo + name + mint NEW pill + glass 25-35 ETA pill + address subline + Free Delivery pill. MATCHES Stitch store_profile_nears_2 composition. PASS
## AC4 metadata pills (unrated)
- NEW pill shown (not 0.0); glass ETA "25-35" present; address in subordinate line. PASS (rated case + no-ETA case still to verify)
## AC8 preservation
- All Products header has grid/list toggle + filter funnel trigger (right); category chip rail All/Bakery & Bread/Dairy & Eggs/General Items; View Cart bottom bar present. PASS (so far)
## AC3 floating glass buttons + favourite toggle
- 02-hero-fav-toggled.png: favourite heart top-right turns mint-filled on tap (logged in as Customer). Back/search/share/fav are circular glass buttons over photo. PASS
## AC6 search header — veg OFF (grocery, Organic Paradise, veg_non_veg=false)
- 03-search-header-veg-off-grocery.png: back glass circle + full-width search input, NO overflow stripe, keyboard auto-opens (autofocus). ui_errors empty, dart runtime errors none. PASS (veg-OFF half)
## AC6 search header — veg ON (food, The Grill House, veg_non_veg=true)
- 05-search-header-veg-on-food.png: back glass circle + search input + VegFilterWidget(funnel) all fit, NO overflow stripe, keyboard autofocus. Runtime errors none. PASS — carried QA-FAIL regression CONFIRMED FIXED in both veg states.
## AC1/AC3 food hero (The Grill House)
- 04-hero-food-grill-house.png: cover photo + scrim + 4 glass buttons (back/search/share/fav, share present => web url configured) + mint-ring logo + name + NEW pill + 20-40 ETA pill + address subline + Free Delivery. PASS
## AC5 closed store (Abu Dhabi / Organic Shop id 9, active=0)
- 06-closed-store-organic-shop.png: cover photo GRAYSCALED + logo GRAYSCALED (mint ring kept); solid RED "Closed Now" pill, white text, legible over grayscale. PASS for grayscale + red pill.
- 07-closed-store-grid.png + 08-closed-store-addtocart-attempt.png: product grid is FULLY INTERACTIVE — tapping "Canned Beans" opened item sheet, "Add To Cart" reached the cross-store confirm dialog (would have added). NO IgnorePointer.
  => AC5 sub-requirement "product grid non-interactive (IgnorePointer)" NOT met. FAIL on AC5.
  Note: base branch feat/userapp-reskin ALSO has no IgnorePointer (git grep clean) — gap predates this branch, but AC5 explicitly requires it for this ticket. task_bug, breaks_ac=true.
  (cart left at "2 Item" — dismissed dialog with No, no DB/cart mutation persisted.)
## AC7 loading skeleton (Test Store, Abu Dhabi)
- 09-skeleton-2.png: navy->navyDeep gradient hero panel (NOT solid navy) with NearsSkeleton photo block; action row has 4 placeholder circles (1 left + 3 right); logo circle + name + pills placeholders bottom-anchored; All Products + chip + grid skeletons below. PASS
## AC2 no-cover fallback
- All seeded stores HAVE covers; no-cover (hasCover=false) branch unreachable live without DB mutation (forbidden). Verified by code + widget test "no cover photo -> branded navy fallback gradient, no broken image" (passes). Skeleton uses IDENTICAL navy->navyDeep gradient as no-cover hero => no color flash/jump on skeleton->loaded transition (confirmed in 09-skeleton-2.png + code). PASS (no-cover gradient via test backstop; transition-no-flash via live skeleton + identical gradient).
## Automated backstop
- Focused: test/features/store/nears_store_header_sliver_test.dart + store_details_shimmer_test.dart => +8 All tests passed. Full suite running.
## AC4 rated store + Dark mode
- 12-hero-darkmode.png (Test Store, Abu Dhabi, RATED): mint "5.0" rating pill (value, not New) + glass "1-15 min" ETA pill. Distance not shown (guarded); tower "Marina Heights" + address in subordinate lines. Confirms rated-store mint pill case. Dark page bg, scrim legible, glass buttons legible. Dark mode PASS, AC4 rated case PASS.
- 10-hero-open-test-store.png: open Test Store light mode (Share button present).
## RTL/Arabic states (dark mode)
- 13-hero-rtl-arabic.png: back arrow MIRRORED to top-right; fav/share/search glass buttons to top-left; logo+name bottom-RIGHT; pills right-aligned (5.0 mint + 1-15 glass ETA); tower+address subordinate lines right-aligned w/ trailing pins; scrim legible. PASS
- 14-search-header-rtl.png: back arrow mirrored top-right, RTL search input (icon right, Arabic hint), chips right-to-left, NO overflow stripe, autofocus keyboard, dark navy body. Runtime errors none. PASS (veg-OFF/grocery RTL).
## REGRESSION SWEEP + DEFECT FOUND
- 15-regression-addtocart-bottomcart.png: item grid renders (Carrots/Croissants/Milk), item detail + Add To Cart works, cross-store guard fires, "Item added to cart" + bottom View Cart bar. Regression PASS for grid/cards/cart.
- DEFECT (task_bug, breaks AC): RenderFlex overflow in rebuilt store hero. DTD Flutter.Error reproduced TWICE on Test Store (rich meta: rated 5.0 + ETA + tower + wrapping 2-line address + free delivery) during SliverAppBar collapse scroll: "A RenderFlex overflowed by 5.7 / 3.3 pixels on the bottom" at Column nears_store_header_sliver.dart:184 (expanded-content Column, MainAxisSize.max, action-row 44dp + Spacer + logo/name 56dp + _MetaBlock). At collapse fractions the Column content exceeds the shrinking Positioned box (constraints h=180.3 / 182.7) before expandedOpacity fades it out. 16-hero-collapse-overflow.png attempted (stripe transient).
  Base branch feat/userapp-reskin hero used contentHeight=224 and a different action-row placement; this rebuild (280 + action row inside the Column) owns the overflow => defect IN this change. SAME class as the reopened-ticket target (overflow stripe).
