# NEARS-2783 QA progress (cycle 0)

- AC1 [ui] null-module clear-cart, no error, cart emptied -> FAIL (DELETE 400, DB row never deleted, false-empty basket)
- AC2 [api] DELETE returns 200 -> FAIL (400 observed, correlation_id=3c3e0481-e55b-43af-b114-5067125d4963)
- AC3 [ui] no raw backend string -> FAIL (showCustomSnackBar(response.statusText) unconditional on this path; backend string = "Module id required")
- AC4 [ui] regression, normal already-has-module state -> FAIL, confirmed in 3 independent variants (cold-boot resume, chained switch, fresh pm-clear + explicit tile tap), all DELETE 400
- Regression sweep: _getCartDataOnline/_addToCartOnline/_updateCartOnline/_updateCartQuantityOnline live-clean (200s, no [FAIL]); _removeCartItemOnline unmodified by source read
- Automated backstop: flutter test cart_repository_clear_cart_module_identity_test.dart 3/3 PASS (mock/live divergence -- test never round-trips the real backend)
- Verdict: FAIL. Comment posted to NEARS-2783. Evidence gallery published.
