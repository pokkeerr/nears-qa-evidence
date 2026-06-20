# NEARS-493 QA progress — locale-aware currency (EN `5.00 AED` / AR glyph)

Device: emulator-5554 (sdk gphone16k arm64). Build: worktree feat/NEARS-493-currency-locale @cdaa44ce.
Backend: worktree Admin served on :8000 (swapped in for the live demo) returning currency_code:AED.

- AC5 LIVE: GET /api/v1/config -> currency_code:"AED" (worktree backend, stable x3). PASS.
- AC1 LIVE: EN store item cards -> `14 AED`,`17 AED`,`12 AED`,`18 AED`,`10 AED` (ISO suffix, one space). shot 03. PASS.
- AC3 LIVE EN: item detail (04), cart (05), checkout summary subtotal/delivery/discount/total (06), payment-method sheet (07), order details/summary (08), wallet balance (09, header 0 AED), search results (12). All EN-AED, no glyph. PASS.
- AC2 LIVE AR: store prices `د.إ.‏ 14/17/12/18/10` glyph prefix unchanged (10); AR search `د.إ.‏ 18/21` (11). PASS.
- AC6 LIVE: AR dates/numbers/percent (`17% OFF`,`30-60 دقيقة`) render fine, no regression. PASS.
- F1: animated counters use ` AED` suffix (one leading space, no trailing) — live ` AED` suffix node + unit test. PASS.
- F2: discount-amount label `10.0 AED off` — unit test backstop (no live amount-discount badge in seed). PASS via backstop.
- Runtime errors: ui_errors clean across full EN+AR session. No crash on fallback path (primary :8000 null) nor on AED path.
- Backstop: price_converter_test 43/43 PASS; ConfigContractTest 4 tests/147 assertions PASS.

DATA FINDING (regression, pre-existing): business_settings has TWO key='currency' rows (id17=AED, id151=USD); Helpers::currency_code() -> get_business_settings('currency') firstWhere is unordered -> currency_code could flip to USD if cache reorders. Returned AED today (stable). DB read-only; reported, not fixed.
