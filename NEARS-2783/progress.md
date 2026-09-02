# NEARS-2783 QA progress (cycle 0)

- AC1 [ui] null-module clear-cart, no error, cart emptied -> FAIL (DELETE 400, DB row never deleted, false-empty basket)
- AC2 [api] DELETE returns 200 -> FAIL (400 observed, correlation_id=3c3e0481-e55b-43af-b114-5067125d4963)
- AC3 [ui] no raw backend string -> FAIL (showCustomSnackBar(response.statusText) unconditional on this path; backend string = "Module id required")
- AC4 [ui] regression, normal already-has-module state -> FAIL, confirmed in 3 independent variants (cold-boot resume, chained switch, fresh pm-clear + explicit tile tap), all DELETE 400
- Regression sweep: _getCartDataOnline/_addToCartOnline/_updateCartOnline/_updateCartQuantityOnline live-clean (200s, no [FAIL]); _removeCartItemOnline unmodified by source read
- Automated backstop: flutter test cart_repository_clear_cart_module_identity_test.dart 3/3 PASS (mock/live divergence -- test never round-trips the real backend)
- Verdict: FAIL. Comment posted to NEARS-2783. Evidence gallery published.

# Cycle 1 (delta re-QA, HEAD 2b3e2d0d1)

- AC1 [ui] null-module clear-cart -> PASS: DELETE 200, DB row deleted (zero rows for guest 1350), Basket genuinely empty. correlation not needed (no [FAIL]).
- AC2 [api] DELETE returns 200 -> PASS (confirmed above)
- AC3 [ui] no raw backend string -> PASS (success path never reaches ApiChecker's error branch)
- AC4 regression (3 variants: cold-boot resume, chained guard-switch, fresh pm-clear+explicit tile tap) -> ALL PASS, all DELETE 200
- Forced-failure check (airplane mode during DELETE): exactly ONE "[ERR] msg=\"error snackbar shown\"" log line (not 0, not 2); [FAIL] correctly tagged endpoint=/api/v1/customer/cart/remove (not /api/v1/module); module switch correctly ABORTED; cart row DB-verified UNTOUCHED (id=701, never deleted) -- confirms both review-cycle-2 fixes live.
- Regression sweep: _getCartDataOnline/_addToCartOnline/_updateCartOnline/_updateCartQuantityOnline/_removeCartItemOnline all live-clean (200s, no [FAIL]) this cycle too. reorder_helper.dart/_openStore + item_controller.dart/clearAndAddToCart confirmed UNCHANGED by diff; new clearCartOnline() signature is backward-compatible (auto-derives fallback from _cartList when no arg passed) -- verified by source read, not separately live-driven (order-history reorder repro would need a delivered order + cross-module state; out of proportion given the mechanism is already verified 4x live in this cycle).
- Automated backstop: 113/113 PASS (re-ran live).
- Verdict: PASS. Comment posted to NEARS-2783.
