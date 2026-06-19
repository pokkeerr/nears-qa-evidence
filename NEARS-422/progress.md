# NEARS-422 QA progress (live, append-only)
Device: emulator-5554 (sdk_gphone16k_arm64) | build: worktree @9740b758 | branch feat/NEARS-422-item-detail-modal
Backend: http://10.0.2.2:8000 (config HTTP 200)

## Automated backstop
- flutter test item_detail_modal_nav_test.dart + item_bottom_sheet_initstate_guard_test.dart => 5/5 PASS

## Live AC checkpoints
- Boot OK: worktree APK installed+running, signed in customer@nears.com, Abu Dhabi zone-2 home. No runtime errors on boot. (shot: signin)
- AC1 PASS: non-food grocery item (Salted Pretzels) opened as BOTTOM SHEET (grab-handle pill, rounded top, X close) — not full-screen. shot ac1-ac2-nonfood-sheet-light.png
- AC2 PASS: scrim ~20% dim — grocery home (Categories/Organic Shop banner) clearly visible behind light veil, not 54% wall. same shot.
- AC4 inStorePage PASS: store-name tap on store-page dismisses sheet, stays on store-profile (shot ac4-instore-sheet.png).
- AC4 NOT-on-store FAIL: store-name tap from grocery-module-home dismisses sheet but lands BACK on module home, store-profile NEVER appears (sampled 0.4-3.2s, store-profile=0 throughout). shot ac4-notonstore-landed.png. ROOT CAUSE: removed Get.offNamed (line 235 original) was load-bearing — Get.toNamed alone after Get.back()+async forcefullySetModule does not land on store-profile.
- AC3 PASS: food item (Smash Burger) opens proper sheet (grab handle, rounded top, 20% scrim, food home visible) shot ac3-food-sheet.png. Cart-edit modal (tap Margherita Pizza in basket) opens proper modal over basket shot ac3-cart-edit-modal.png. No runtime errors. Both unchanged/working.
- AC5 FAIL: valid item deep-link (id 108 grocery) does NOT open sheet over store-profile — lands on all-modules HOME, no sheet, no store-profile (sampled 6s: sheet=0/store=0/home=1). Trace shows item 200 + store_screen initDataCall fired but forcefullySetModule's full home/all reload cascade clobbers the store push + sheet. shot bug-deeplink-no-sheet.png + bug-deeplink-no-sheet.log. Also: cross-module deep-link 404s (fetch before module set).
- AC6 PASS: invalid item deep-link (id 99999999) -> 404 -> 'Item not found' snackbar rendered (confirmed via a11y tree at t=0.6s) + NOTHING pushed (store-pushed=0 throughout). Visual screencap raced the ambient order-status toast; snackbar text verified in a11y tree + 404 trace. shot ac6-item-not-found-snackbar.png (pixel obscured by ambient toast), log via trace.
- AC7 PASS: dark-mode grocery item sheet (Sparkling Water) — grab-handle pill is mid-grey (theme outlineVariant, not white/navy frozen); 20% scrim dim works (dark grocery home visible behind veil); content (item/store/price/description/qty) legible on dark surface. shot ac7-sheet-dark.png
- AC8 PASS: Arabic/RTL grocery item sheet (Sparkling Water) — layout fully mirrored (image right / heart left, X top-left, Description right-aligned, qty stepper bottom-left, Total Amount right-aligned), grab-handle pill centered, 20% scrim shows RTL grocery home behind, no overflow, no runtime errors. Add-to-cart/qty controls reachable. shot ac8-sheet-arabic-rtl.png
- AC9 PASS: opening item sheet captured the ItemBottomSheetShimmer safe-state (sheet slid up w/ rounded top + grab-handle, skeleton placeholder bars while item==null during fetch) — NO crash, no runtime errors. Plus deep-link 404 null-item path (item==null) did not crash. Plus automated guard test passes. shot ac9-initstate-shimmer-safe.png

## Regression sweep (bounded, 5 surfaces — item-detail entry points)
- Search -> item tap (Mixed Nuts): sheet opens correctly, no crash. shot reg-search-item-sheet.png
- Store-page item tap (inStorePage=true): sheet opens, store-name tap stays on store. PASS (AC4 inStore).
- Cart-edit (basket line tap): modal opens over basket. PASS (AC3).
- Food + grocery item taps: sheet opens. PASS (AC1/AC3).
- Direct Add To Cart (itemDirectlyAddToCart branch B): cross-store reset ConfirmationDialog fires correctly (dismissed WITHOUT confirming — cart NOT mutated). PASS, no runtime errors.
- No runtime errors / red-screens / overflows observed across the whole session (get_runtime_errors clean at every checkpoint; ui_errors clean).
