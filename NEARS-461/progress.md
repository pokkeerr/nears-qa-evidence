# NEARS-461 + NEARS-462 live QA progress (emulator-5554, branch @3ee7aaa5)

## NEARS-461 (dark text refactor) — observed
- AC-1 dark sweep: Home PASS (dark-01), Store detail PASS prices mint (dark-02), Basket/Checkout PASS prices mint (dark-03), Profile/Menu PASS (dark-04), Orders PASS prices mint (dark-06), Settings PASS (dark-05), Order tracking PASS (dark-07). No dark-on-dark NearsText.
- 521 error salmon: PASS — login empty submit -> "Please enter password" + border in salmon-pink errorDark (dark-08).
- 458-F2 elevated white card shadow: PASS — guest-track elevated NearsSurfaceCard visibly lifts on dark scaffold (462 ar-08).
- 458-F3 settings icons mint: PASS — moon/globe/bell icons mint on dark (dark-05).
- AC-3 light no-regression: light-01 home, light-04 profile, light-05 settings captured.
- Backstop: theme + golden tests +11 PASS.

## NEARS-462 (AR content + guest no-match routing) — observed
- AR strings: ar.json back=رجوع, no_order_found contains طلب (not أمر), back_to_home=العودة للرئيسية. Count ar=en=1911. PASS (source).
- es/bn subtitle: native values confirmed in es.json/bn.json (not English/raw key). PASS (source); live empty-state unreachable due to bug below.
- VALID id (156)+phone -> 200 -> populated track screen PASS (ar-08).
- Network error (airplane) -> snackbar, stays on input, NO empty-state. PASS (ar-09).
- INVALID id (999999) -> 404 -> **FAIL**: transient "Not found" toast, stays on input form, NearsEmptyState NEVER renders. Routing AC BROKEN. (bug-guest-404-no-empty-state.{png,log})
- Backstop: order_controller + guest_track_screen tests +65 PASS (mock layer bypasses the real handleError path that causes the live bug).
