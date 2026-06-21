# NEARS-510 QA progress — distance-based delivery ETA (mins+secs)
Device: emulator-5556 | Build: worktree feat/NEARS-510-eta-distance @ HEAD | Light mode (dark deferred)
Backend: local 8000 vs multi_food_db (HTTP 200)
Automated backstop: flutter test (delivery_eta_helper_test + delivery_eta_banner_test) = 36/36 PASS

## AC checkpoints
- AC-4 (static fallback before address distance) + AC-2 baseline: mobile Checkout banner shows "Arriving in ~30 min 58 sec" with default Demo Zone Dhaka addr (zone1, store1). Distance-based, ~prefix, min+sec format. Shot 01-checkout-eta-near-dhaka.png. NO errors.
- AC-2 (CORE — ETA reacts to distance, MOBILE): near addr46 (0.356km from store1) = "~30 min 58 sec"; far in-zone current-location (2.846km, in zone1, NOT blocked by NEARS-513) = "~35 min 42 sec". ETA LONGER for farther address. min+sec format, ~ prefix. Math: 30min prep + round(2.846/30*3600)=341s=5m42s = 35m42s EXACT. Shots 01 (near) + 02 (far). PASS.
- AC-4 (static fallback): caught live transient — banner shows verbatim "30-40 min" (NO ~) before distance resolves, then "~30 min 58 sec". No 0/null/crash. ui_list captured twice. Shot 03 (timing sub-second, textual evidence authoritative).
- AC-3 (take_away no banner): order-type toggle NOT reachable in delivery-only reskin checkout (no UI control). Covered by widget tests (take_away early-return x2). Faithfully noted UI-unreachable.
- BUG (task, medium, breaks_ac=false): selecting out-of-zone Abu Dhabi addr -> 513 reverts address label to Dhaka + disables Place Order, BUT banner left showing stale "~7323 min 16 sec" + Abu Dhabi map (distance not reset on 513 revert). bug-cross-zone-eta-flash.png/.log. AC-2 core in-zone PASS unaffected.
- 513 interplay regression: zone guard fires correctly (warning + Place Order disabled).
- AC-5 (RTL/Arabic): banner "يصل خلال ~30 دقيقة 58 ثانية" — numerals 30/58 LTR Western digits, units دقيقة/ثانية, ~ prefix, full RTL mirror, NO overflow, NO runtime errors. Shot 05. PASS.
- REGRESSION sweep:
  * Store-card ETA label UNCHANGED: "30-40 MIN"/"30-40 min"/"NEW" on home+store lists, EN+AR (separate etaLabel path). CLEAN.
  * Delivery fee/order summary renders correctly (Subtotal/Discount/Delivery Fee FREE/Total). CLEAN.
  * NEARS-513 zone guard fires correctly on out-of-zone select (warning + Place Order disabled). CLEAN.
  * Order placement: checkout flow reaches Place Order -> order-summary -> button fires (log "Place Order BUTTON CLICKED"). Actual order-API blocked ONLY by pre-existing business-rule config conflict: store min-order 20 AED vs COD max 10 AED (no single total satisfies both; only COD payment seeded). NOT a NEARS-510 issue. Banner unaffected throughout.
- AC item 4 (DESKTOP surfaces — width-gated >=1300): web run NOT FEASIBLE (Playwright not installed in env; uinav_web.sh requires it). Covered by: (a) widget tests delivery_eta_banner_test.dart ("defaults to showMap:true" desktop-banner case) + delivery_eta_helper_test.dart fallback cases (36/36 pass); (b) IDENTICAL DeliveryEtaHelper.resolveEtaText path proven on mobile — desktop checkout banner = same DeliveryEtaBanner widget (showMap default true), desktop basket row = same resolveEtaText(store.hasPlausibleDistance?distanceInKm:null, deliveryTime) with static fallback. NOT live-demonstrated.
- CLEANUP: 3 stray test addresses (49/50/51, created via /address/add during AC-2 exploration) DELETED via app UI (/address/delete 200 x3). DB restored to original 2 seed addresses (45,46). No order residue (Place Order attempts blocked by min-order/COD-cap rules before order API; 2 today's orders are pre-existing).
- Dark mode: DEFERRED (light-first) — not gated, not booted.
