# NEARS-3940 QA [8] cycle 0 — evidence index
Build: worktree nears-NEARS-3940-cod-full-amount @ cfd6b9341 (HEAD); BASE: f04c3a21b (scratch worktree). Device emulator-5554 (AVD NEARS_2424_QA), 1080x2400, font_scale 1.0, light mode.
DB: private copy nears_qa_3940 (mysqldump of multi_food_db, read-only on source). Backend: php -S 127.0.0.1:8342 from worktree Admin/ (cwd @ cfd6b9341), fronted by a logging/fault-injecting proxy on :8340 (proxy-harness.py.txt). App built with API_HOST=10.0.2.2:8340.
Serverside figures (copy, Rice 5kg x2, store 1): items 27.05 after 10% discount, tax 1.3525, free delivery ON -> server order_amount 28.40 (orders 91416/91417/91422). Free delivery OFF -> 29.40 (delivery_charge 1.00, order 91419). Tax-included -> 27.05 (order 91418).
Files: proxy-*.log.txt = backend-side delivery-quote/get-Tax/place request log (amt=, resp=, status); app-head-*.log.txt / app-head-all-flutter-lines-part*.txt = AppLogger/analytics lines; *.png/*.xml = screenshots + accessibility dumps.

# Cycle 1 (delta) — 2026-10-01, build 6542b4daf (UserApp code identical to merge b53ec7217)
Device emulator-5554 (NEARS_2424_QA, 1080x2400, light, font_scale 1.0). DB copy nears_qa_3940 (guest_checkout_status=1 on COPY only; shared 0). Backend php -S :8342 (pid 91718, cwd worktree, @6542b4daf, freshness PASS), harness proxy :8340 (proxy-harness-cycle1.py.txt adds tax_strip / store_null_zone / quote_body_200 knobs). App API_HOST=10.0.2.2:8340. Cart Rice 5kg x2 store 1, items 27.05, server full 28.40.
- A1 guest cap 27.50: verdict amt=28.4 -> cod_eligible=false, cash hidden, cod_limit_exceeded row, [WARN] reason=cod_cap x1 (c1-A1)
- A2 guest cap 28.39: amt=28.4 false, hidden (c1-A2). A3 cap 28.41: amt=28.4 true, cash offered (c1-A3). A4 placed guest order 91424 (is_guest=1 user 1971) order_amount 28.40 cash_on_delivery (c1-A4). A5 cap 27.50 + injected 500 on amt>=28: cash kept, exactly 1 [FAIL] delivery-quote status=500 correlation_id 3fc7c100 == proxy rid (c1-A5)
- B1 get-Tax 200 with product_price/total_addon_price/total_discount stripped: cash offered, exactly 1 [FAIL] endpoint=/api/v1/customer/order/get-Tax "cod cap verdict not scheduled (tax components missing)", no amounts, no verdict request; 3 tip taps -> still 1 (c1-B1)
- B2 store zone_id nulled (stores/details proxy): only the NEARS-3937 fee line "delivery quote not scheduled (no zone/module)" x1; verdict line NOT emitted and no verdict request (shadowed by isTotalUnresolved) (c1-B2)
- B3 200 malformed body {"delivery_charge":[1],"cod_eligible":"yes"}: no throw, no [FAIL]; cod_eligible=='yes' parsed as false -> cash hidden reason=cod_cap (c1-B3)
- C take_away: git grep proof reproduced at b53ec7217 (see QA comment).
Files: c1-*.png/xml, c1-app-flutter-lines.log.txt, c1-proxy-all.log.txt, shared-db-untouched-cycle1.txt
