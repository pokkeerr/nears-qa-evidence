# NEARS-3879 QA progress
- 02:05 backend: worktree :8115 pid 42688 (artisan 42584), DB multi_food_db_qa_bug3879, /config reads guest_checkout_status=1 cross_module_basket=true (shared DB has 0/0) -> server hits the copy.
- device emulator-5590 (spare AVD nears_qa_wave56, ppid1), lock acquired, app com.izzes.nears.nears_nears_3879_guest_tax_verify, API_HOST=10.0.2.2:8115.
- AC2 flagON guest 2 stores (Grill House 39 Chef Salad 43.75 + Kitchen 91159 Chicken Shawarma 15.75): Subtotal 59.50, VAT +2.98, Delivery 0.00, Total 62.48. get-Tax x2 = 200 in app log.
- AC1 curl: (a) 200 tax 2.1875/0.7875; (b) omitted 401; (c) wrong token 401 (BE log join by X-Request-Id).
- 02:11 AC4: ONE guest group order placed (COD): #91418 (Grill House, tax 2.19, amount 45.94) + #91419 (Kitchen, tax 0.79, amount 16.54); sum tax 2.98 == VAT shown 2.98; total 62.48 == shown 62.48. order_taxes 2.1875 + 0.7875 (5% x 43.75 / 15.75).
- K3 flag OFF (config False) guest: VAT +2.98 total 62.48. AC3 logged-in flag OFF and ON: VAT +2.98 total 62.48; bearer curl 200 same tax.
- extra: flag ON guest cross-module (grocery+restaurant): VAT +2.82 (0.625+2.1875), 2 get-Tax 200.
