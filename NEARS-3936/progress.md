# NEARS-3936 QA progress (cycle 0) - emulator-5558, UserApp @ fce1bb09c, backend :8136 on nears_qa_3936, proxy :8137

| # | Check | Result | Evidence |
|---|---|---|---|
| C1 | Control: no surge (200 price 0) | PASS - 2x1.00, Delivery Fees 2.00, Place enabled | c1-checkout-nosurge-*.xml |
| 1 | Surge fail all stores (RENAME surge_price_dates) | PASS - bill warn+msg+Retry per store, combined "Delivery Fees, Something went wrong" (—), orientation fee — with real ETA, cart "Delivery Fee, Something went wrong" + real ETA, Place disabled | s1-*.xml, c3-cart-3store-surgefail.xml, ac1-surge-fail-bill-en.png |
| 2 | Retry re-fail + double tap | PASS - 1 dispatch (2 surge calls for 2 stores), no Retry node + Place disabled in flight, no single-store fallback, back to failure rows | r1-t1/t2/t3.xml, proxy log |
| 2b | Retry success, 3-store | PASS - 3 skeleton rows (gap 255px vs 189px for 2 = +1 x 66px row), Place disabled in flight, resolves 3x1.00=3.00, Place enabled | r2-*.xml |
| C2 | Control: surge configured (2.00) | PASS - 3x3.00, 9.00, no failure row | k1-surge-configured.xml |
| C3 | Control: free-delivery store + self-delivery store (sub_self_delivery=1, fee 8.26) under surge fail | PASS - both resolved; only normal store blocks. (Store 21 has self_delivery_system=1 but subscription self_delivery=0 -> effective 0 -> correctly blocks; parity) | k2-*.xml, k3-*.xml |
| 3 | Exit by edit (surge instrument) | PASS - remove Fresh local -> Place enabled, no retry | e1-*.xml |
| A | Store detail 500 (s==null) | PASS - row unresolved, 1 log per pipeline run | d1-*.xml |
| B | Per-store delivery-quote 500 | PASS - 'delivery-quote fetch failed' x1, ETA kept | q1-*.xml |
| S1 | Fee compute threw (free_delivery null) | PASS - 'group delivery-fee compute threw' x1, no input-missing dup | S1-compute-threw.xml |
| S2 | Zone missing | PASS - 'group fee input missing zone/module store_id=13' x1 | S2-input-missing.xml |
| S3 | Surge parse threw x3 | PASS - 'group per-store surge fetch threw' x3 | S3-surge-threw.xml |
| - | Pipeline-level throw | UNVERIFIABLE live (all network paths caught locally); unit-covered | - |
| 3' | Exit by edit (permanent 403) | PASS | e2-after-remove-403-*.xml |
| 4 | Permanent 403: reason / way to remove | FINDING - only a never-working Retry on checkout | bug-permanent-unresolvable-store-retry-only.log |
| 5 | No toast in failure flows | PASS - toast px 341 / 733 / 303 (toast ~16-20k) | ac1/ac2/ac3 png scans |
| 6 | Logs 1:1, no repeat on rebuild, no PII | PASS | flutter run log |
| 7 | AC5 no new event | PASS - diff adds 0 analytics calls; place_order_tapped fired (existing) | - |
| 8 | Layout cell 320dp x 1.3x EN+AR | FAIL - store name mid-word break "Fresh su/permar..." EN and AR; rest of cell OK (no overflow in row, Retry own run, 130x44dp, RTL end, icon unmirrored) | bug-unresolved-row-storename-midword-break.log |
| 9 | Free-delivery threshold (11.78) | PASS parity (client Free; server eligibleAmount 12.40-0.62=11.78 >= 11.78 -> 0, code-derived, 0 orders) | f1-threshold-*.xml |
| 10 | Regressions 3771 / 3691 / 3687 / 3934 / 3894 | PASS all | e1/e2, n3691, r1/r2, n3934, n3894 |
| R | Pre-existing overflow at 320dp/1.3x: sticky Total row (checkout_screen.dart:1090, 23px) + loading shimmer (checkout_screen_shimmer_view.dart:53, 63px, AR) | regression_bug | bug-total-amount-row-overflow-320dp-1_3x.log |

Automated: flutter test test/features/checkout test/features/cart -> 1543 passed.
Orders placed: 0 (proxy safety-net 500 on /order/place + /order/group/place; 0 place calls observed).

# Fix cycle 1 (delta re-QA) - emulator-5556, UserApp @ d0cc1dcd8 (qa-run.sh, API_HOST=10.0.2.2:8137), backend /Users/Apple/Projects/nears-NEARS-3936-group-fee-failure-row @ d0cc1dcd8 :8136 on nears_qa_3936, proxy :8137 (qaproxy.py)

| # | Check | Result | Evidence |
|---|---|---|---|
| AC1 | Surge 500 all stores, default size EN | PASS - per unresolved store TWO button nodes `<store>, Something went wrong, Retry` (132x132px=44x44dp) + `<store>, Edit Cart` (174x132px=58x44dp), combined `Delivery Fees, Something went wrong`, self-delivery Test Store resolved 0.00, Place Order clickable=false; 3 injected -> 3 [FAIL] get-surge-price | v3-ac1-surge-bill-en.xml/.png |
| AC2 | Retry success (fault cleared) | PASS - 1 dispatch (3 surge calls), 1.00+1.00 -> Delivery Fees 2.00, Place enabled | v3-ac2-retry-success.xml |
| AC2' | Per-store fault: store-detail 403 store 13 | PASS - only store 13 unresolved, Fresh local 1.00, Place disabled; Retry re-dispatches once, stays blocked; 2x403 -> 2x [FAIL] 'group store detail unresolved store_id=13' | v3-c3-403-*.xml |
| C1 | 320dp x1.3 EN+AR, long name (store 13 renamed on copy) | PASS - EN 'Fresh Supermarket Al / Barsha' breaks between words; AR 'سوبرماركت فريش البرشاء' one line; Retry + Edit Cart whole, same line, end-aligned (LTR end x=855 == resolved amount end; RTL Edit Cart left x=105 == resolved amount x=105); tap targets EN 46x44/75x44dp, AR 78x44/64x44dp; no overflow from checkout_group_fee_breakdown.dart | v3-c1-en-ar-320-13x-feebreakdown.png, v3-c1-*-320-13x.xml/.png |
| C2 | Edit Cart -> Basket -> Back, nothing removed | PASS - Basket opened, 0 surge/quote calls after the tap; back on Checkout both stores still unresolved, Place Order clickable=false | v3-c2-*.xml |
| C3 | Permanent 403: Edit Cart -> identify -> remove | PASS - Basket shows 'Fresh Supermarket Al Barsha' with 'Delivery Fee, Something went wrong' + ETA '—'; Remove Sparkling Water -> Back -> Delivery Fees 1.00, Place Order clickable=true | v3-c3-403-basket.xml, v3-c3-403-after-remove.xml |
| AC3 | No toast in these flows | PASS - 0 toast-like nodes in 10 v3 dumps; positive control: 'Removed from cart' snackbar did appear in the tree | v3-*.xml |
| X | Coupon at free-delivery threshold (routed -001 C3) | PRE-EXISTING mismatch (base bb4fc8927): client Free 0.00, server eligibleAmount 20-2=18 < 19 -> charges 1.00 | bug-coupon-at-threshold-group-fee-shown-free-server-charges.log |
| R | DLS n_item_card.dart:1964 bottom overflow 15/19px at 320dp/1.3x | regression_bug (pre-existing, packages untouched) | bug-dls-nitemcard-bottom-overflow-320dp-1_3x.log |

Orders placed: 0 (place endpoints 500 via proxy safety net; none called).

## Guide notes (parked here; do not edit the shared guide from this worktree)
- The copy (and the shared DB) carry `admin_free_delivery_status=1 / free_delivery_to_all_store`: every group fee is 0.00 and a surge failure correctly does NOT block (unresolved needs fee > 0). Set status 0 on the COPY + `DB_DATABASE=<copy> php artisan cache:clear`, then hot-restart the app (config is cached): `kill -USR2 <flutter_tools run pid>` works for a backgrounded `qa-run.sh`.
- After a hot restart user 6 (`customer@nears.com`) gets an old "Your payment was Incomplete" sheet (#91404): tap `Close` only (never `Cancel Order` / `Pay Now` / `Switch to Cash On Delivery`).
- Coupon chips in the checkout coupon sheet apply on tap (no separate `Apply` press needed).
- Store names in Checkout come from the cart load: after switching language, reload via Home -> `Pharmacy` -> `Grocery` -> Basket to see the translated name.
- Settings on Profile sits partly under the bottom bar at 320dp; resolve its live bounds and tap the visible strip.
