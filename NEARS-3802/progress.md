# NEARS-3802 (#15) + NEARS-3788 #16 live QA — emulator-5554, com.izzes.nears.live, 2026-09-28 02:24-02:35 GST
- #15a PASS — EN snackbar "Test Store: Store is closed now" (15-after-confirm-en.xml)
- #15b PASS — sheet closed; gate card "Store is closed now" + "Edit Cart" under Test Store; Place Order enabled=false; re-tap fired no validate (15b-*.xml)
- #15c PASS — one [FAIL] per Confirm tap (15c-fail-lines.log)
- #15d PASS — AR snackbar "متجر الاختبار: المتجر مغلق الآن" (15d-*)
- #16 PASS — 0 "null" in EN+AR checkout dumps; positive control = address node present (16-*.xml/png)
- Cart restored to Organic Bananas x2 (99-cart-restored.png)
