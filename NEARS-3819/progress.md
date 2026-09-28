# NEARS-3819 QA [8] cycle 0 — progress
Device: emulator-5574 (AVD Pixel_10_Pro_2, spare booted for this run), UserApp debug from worktree @ 5c89fdf6a, pkg com.izzes.nears.nears_nears_3819_logo_stack, --dart-define API_HOST=10.0.2.2:8819
Backend: /Users/Apple/Projects/nears-NEARS-3819-logo-stack @ 5c89fdf6a (:8819; later :8820 behind a module-only delay proxy on :8819 for AC8)
- AC7 PASS api-module-before-after.log
- AC12 PASS api-module-before-after.log (15/14/21 == enumerated opened() lists; base 17/15/22)
- AC13 PASS parcel module preview_stores [] + phpunit
- AC1 PASS ac1-home-module-grid-en.png (+17/+11/+18, ecommerce no +N)
- AC6 PASS uiautomator content-desc "Grocery, 20 stores near you, Dama baqala, Noor Al Ward grocery, Mussafha gate baqala"
- AC5 PASS ac5-home-grid-en-1_3x.png / ac5-...-narrow360dp.png (logo band 50px@1x == 51px@1.3x)
- AC4 PASS ac4-home-grid-ar-rtl.png (first logo right-most, 53px visible vs 31/31; pixel runs)
- AC9 PASS ac9-notifications-en(-row91391).png / ac9-notifications-ar-rtl.png
- AC8 PASS ac8-stale-cache-pill-only.png -> ac8-after-refresh-logos.png
- AC2/AC3 PASS (widget tests) + live stock-placeholder stores render "N" initials
- AC11 PASS, AC14 PASS, AC10 DEFERRED

# NEARS-3819 QA [8] cycle 1 (delta) — progress
Device: emulator-5574, UserApp debug @ 6588a1ffc, pkg com.izzes.nears.nears_nears_3819_logo_stack, --dart-define API_HOST=10.0.2.2:8819
Backend: /Users/Apple/Projects/nears-NEARS-3819-logo-stack @ 6588a1ffc (:8819, backend-freshness-check PASS)
- UX-F1 / AC9(+AC4 RTL) PASS fix1-ac9-notifications-ar-rtl.png (+ -rows crop): AR #91391/#91394 badge reads "+1", "+" left of digit, badge on the stack's trailing (left) side; EN fix1-ac9-notifications-en.png unchanged "+1"
- UX-F2 / AC6 PASS fix1-ac6-module-grid-ar-a11y.xml: 4 AR tiles joined with "، " (0 ASCII ", "); EN fix1-ac6-module-grid-en-a11y.xml byte-identical to cycle 0 Grocery label
- Sweep: AR grid tiles 0 changed px vs ac4-home-grid-ar-rtl.png; EN grid tiles 0 changed px vs ac1-home-module-grid-en.png
- Sweep: order status cards (AR) no +N badge present; store card (NStoreCard preview) AR shows "11+" -> pre-existing regression (base n_store_card.dart overflowTile, no LTR isolate) bug-store-card-overflow-tile-ar-reversed.png
