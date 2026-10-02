# NEARS-3981 QA progress (fix-cycle 0), UserApp 8c1ae8818, emulator-5662, private DB copy nears3981_qa, own server :8981 (app via logging proxy :8982)
Store 4 min=10.00 unless noted. Bar text read from the on-screen "Minimum order ..." node; Proceed state from its enabled flag.
- C1 item16 Regular x1: "Add 1.01 AED more to reach minimum", Proceed disabled. PASS (C1-regular-below-min.png)
- C2 item16 Large x1: "Minimum order met (11.49 / 10.00)", Proceed enabled; COD order 91416 placed HTTP 200, stored line price 11.49 Large optionPrice 2.50, order_amount 12.06. PASS (C2-large-met.png, C2-confirm-sheet.png)
- C3 Regular+Tomato: "Add 0.51 more", Proceed disabled. PASS (C3-...png). Pre-fix would show 1.01 (10.00-8.99).
- C4 Regular+Fried Egg: met 10.24/10.00, Proceed enabled. PASS
- C6 Regular+Extra Cheese add-on: met 10.49/10.00. PASS
- C7 Regular+Jalapenos add-on: "Add 0.01 more", Proceed disabled. PASS
- C8 item16 Large x2: met 22.98/10.00 (option x qty). PASS
- C12 item16 Regular + 9003981 Large: met 10.49/10.00. PASS
- A3 forced: curl (own token) 406 {"errors":[{"code":"order_time","message":"You need to order at least 10 AED"}]}, BE log reason=minimum_order http_status=406 correlation_id==X-Request-Id; in-app the checkout local guard blocked first with [FAIL] PlaceOrderBlocked reason=minimum_order_amount_is store_id=4; positive control Large basket placed 200 (order 91418).
- A4a Veggie Burger + Extra Cheese (no priced option): met 11.49/10.00 (=9.99+1.50). PASS
- A4b store 2 item 84: 250ml (200) "Add 50.00 more", Proceed disabled; 500ml (300) met 300.00/250.00. PASS
- A4c item16 10% discount + min 11.00: Large bar "met 11.49/11.00" (gross, discount 1.15 not entering), Proceed enabled; local checkout rejected (PlaceOrderBlocked minimum_order_amount_is) on post-discount 10.34 < 11.00; server accepts same basket (curl, order 91419). Finding candidate (separate from this ticket).
- A5 local pair (Regular then Large, item 16): Basket screen reloads from server on open, so rows read hybrid: both rows "Size (Large)", bar "met 22.98/10.00" (true 20.48). KNOWN LIMIT NEARS-4024. Relaunch: identical. COD order 91417: SENT variations both Large (cart_id 989 and 990), SENT order_amount 24.0; STORED lines Regular 8.99 + Large 11.49, order_amount 21.50.
