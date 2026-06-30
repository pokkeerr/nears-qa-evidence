# NEARS-668/669/670 QA progress (live, fix-cycle 0)

Device: emulator-5556 (Android 17). Build: worktree feat/NEARS-668-itemcard-batch @ee559de3. Light mode. Zone 1 (Dhaka demo).

## Pre-flight
- baseUrl = http://10.0.2.2:8000 (real local backend) — config 200 OK. PASS.
- Automated backstop: 11/11 widget tests PASS (item_card_dls_alignment, item_card_in_store, most_popular_rail_semantics) incl NEARS-668/662/630 cases.
- Module stock map: grocery(1,4,6)+pharmacy(3)=stock TRUE; food(2)=stock FALSE.
- Fixtures: OOS item 61534 "QA OOS Fixture — Sparkling W" store2 grocery zone1 stock0; food 0-stock items store4/5/6.
- DRIFT: search results render ItemWidget, not ItemCard (task scope said search uses ItemCard).

## AC results
- AC1 OOS overlay (store2 grocery, item 61534 schedule-AVAILABLE so overlay is pure stock-gate): grayscale+red CLOSED badge, NO "Add To Cart" node (disabled +), in-stock siblings DO have Add To Cart. No legacy navy out_of_stock pill anywhere. logs clean. PASS. shot ac1-oos-fixture-store-grid.png
- AC4 visual: grayscale veil + CLOSED top-leading, top corners only, parity w/ ItemWidget (same NotAvailableWidget). PASS (1 shot).
- AC5 schedule path: Red Apple/Banana/Whole Milk (08:00-22:00, closed@23:04) show same CLOSED overlay + active + underneath. "both OOS+sched => one overlay" by code ternary (single NotAvailableWidget) + unit test. PASS.
- AC7 44dp: Salted Pretzels Add-To-Cart hitbox 132px=44dp wide; edge-tap x=1157 (outside 36px circle) fired add_to_cart{item108}. PASS.
- AC8 NEARS-630 decrement: stepper -/1/+ ; "Remove" node clickable=true; tap -> remove_from_cart{108}+cart/remove[200], reverted to +. PASS.
- AC9 no reflow: fixed grid cell + CartCountView reserves 36h both states; addControl end-anchored in Clip.none stack. (confirm bounds). 
- Logs during add/remove: all 200, analytics add_to_cart/remove_from_cart fired, no ERR/FAIL.
- AC2 food module.stock=false: Burger Palace stock=0 items (Double Bacon Burger 17, Chicken Wings 19) have ACTIVE "Add To Cart"; tapped DBB -> cart/add[200] add_to_cart{item17}. NO disabled +, no stock overlay (CLOSED present is schedule-only @23:0x). PASS. shot ac2-food-zero-stock-active.png
- AC3 null stock: NO live endpoint omits stock (all serialize it); guard item.stock!=null short-circuits; covered by code + dls_alignment tests. met-by-code, live-untriggerable (noted).
- AC6 RTL/Arabic: switched to Arabic; store2 cards show مغلق badge at TOP-RIGHT (logical start) on Recommended rail (Whole Milk/Banana/Red Apple) + grayscale OOS fixture in All Products grid; layout mirrored (+ bottom-left). PASS. shots ac6-rtl-closed-badge{,-2}.png
- AC10 isShop: requires moduleType==ecommerce (NOT seeded) + no unit test uses isShop:true. met-by-code only (isShop branch = diff-unchanged bottom:0/end:0 positioning + same 44dp SizedBox proven tappable in AC7; 36px circle in 44dp box = 4dp inset). COVERAGE GAP flagged (non-blocking).
- AC11 Most Popular rail: food home "Most Popular Items" rail renders ItemCards cleanly (Cheeseburger/Bacon Burger/Wings/Fries/Garlic Bread), no missing items, no overflow. NEARS-670 removed-field is unused no-op. PASS. shot ac11-most-popular-rail.png
- AC9 no reflow: addControl = fixed 44h SizedBox both states (w 44<->100), end-anchored in Clip.none stack; CartCountView reserves 36h both; grid fixed-cell; no sibling shift observed on add/remove. PASS (struct+observed+dls test).
- Automated backstop: 3 touched files 11/11 PASS; broader card_design+home dirs 54/54 PASS.
- Regression: NO runtime errors across home rails/store grids/food rail/RTL/cart ops. Search uses ItemWidget (NOT ItemCard) -> out of blast radius (drift noted).
- Device restored to English/zone1. Light mode throughout (dark deferred).
- VERDICT: PASS.
