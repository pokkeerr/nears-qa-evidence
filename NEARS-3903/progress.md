# NEARS-3903 QA [8] — fix cycle 0 — progress

Build: HEAD a1a066ffa (fix/NEARS-3903-row-add-slot-price-overlap), UserApp debug, pkg com.izzes.nears.nears_nears_3903_row_add_slot_price_over
Base control: f4281b5c3 debug APK, pkg com.izzes.nears.qa3903base (same device, same server, same settings)
Device: emulator-5584, wm size 960x2138 @ 480dpi = 320x712dp (reset after), font_scale 1.3 / 1.0 (reset to 1.0), light mode
Backend: /Users/Apple/Projects/nears-NEARS-3903-row-add-slot-price-overlap/Admin @ a1a066ffa, :8101, DB multi_food_db_qa3903 (private copy)

| AC / scope | status | evidence | logs |
|---|---|---|---|
| AC1 item_view (row) 320dp 1.3x EN/AR plain+disc, '+' and stepper | PASS | montage-iv_en13/iv_ar13 (+ 1.0x iv_en10/iv_ar10) | clean (no overflow on item_view rows) |
| AC1 cart_suggestion_rail 320dp 1.3x EN/AR plain+disc '+' (brand-only rows) | PASS | montage-rail_en13, montage-rail_ar13, rail-ar10-disc | clean for brand-only rows; brand+unit / brand+rating rows overflow = pre-existing (base same px) |
| AC1 cart rail stepper / Rx pill | n/a live (host filters in-cart + Rx items: cart_controller.suggestedItemsFrom) — widget test | n_item_card_row_add_slot_test 1170/1170 | - |
| AC1 staple_card_widget 320dp 1.3x EN/AR qty 0/1/9/10/12 | PASS | montage-staple, montage-staple2, montage-staple_en | clean |
| AC1 store_screen row site (desktop >=1300dp) | widget test | n_item_card_row_add_slot_test.dart 1170/1170 (210dp fixtures) | - |
| AC1 cross_store_search_screen (enableCrossStoreSearch=false) | widget test | same file (300dp fixtures) | - |
| AC2 goldens | PASS | test/golden 185/185; 9 n_item_card* goldens byte-identical vs f4281b5c3 | - |
| AC3 flag OFF stepper-vs-price live | PASS | base-iv-en13-incart (defect at base) vs iv-en13-incart / iv-ar13-incart (fixed) | clean |
| T3/J2 transition item_view | PASS | EN 1.3x: Rice [1399..1765] next 1810 -> in cart pitch 411 unchanged; 1.0x remove: strike back; AR same | clean |
| Rx pill flag ON (copy only) EN/AR 1.3x | PASS | montage-rx, montage-rx_en | clean |
| Closed/OOS discounted row | PASS | montage-so: 1.0x strike beside price + disabled '+'; 1.3x strike dropped, no room (W2 clause 2, measured ~27dp free vs ~39dp needed) | clean |
| Tap add/stepper never opens sheet; name opens sheet | PASS | 11+12 stepper taps stayed on list; name tap opened sheet | clean |
| Semantics (bare-number price) | PASS | AR 1.0x rail strike drawn "43.17" (no currency), a11y label "د.إ. 43.17"; staple qty0 only 1 add node | clean |

Regression candidates (pre-existing, reproduced on BASE):
- cart rail 1.3x brand+unit row overflows 110 box by 15px (base RenderFlex 15px) -> price clipped
- cart rail 1.3x brand+rating row overflows by 20px (base RenderFlex 20px) -> price clipped
- search results screen: RenderTable.assembleSemanticsNode assertion, a11y tree collapses (base same)

Fixtures in the PRIVATE copy only (shared untouched, verified): items 541/542 rating_count 1->0; customer_staple_items +1 (sched 2, item 222); pharmacy_item_details +2 (631, 633 Rx); items 632 stock->0; business_settings 228 flipped 0->1->0 (ends 0).
Shared DB: bs228=0 before and after; max(orders.id)=91415 before and after.
