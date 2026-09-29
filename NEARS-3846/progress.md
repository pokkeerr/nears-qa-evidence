# NEARS-3846 QA progress (cycle 0) — FINAL
Device emulator-5580 (NEARS_2424_QA, 411dp; 360dp×1.3 via wm density 480 + font_scale 1.3 for AR shots). Build eb6561bad (worktree APK). Control build d14bba041 (detached worktree, separate package). Backend: own `artisan serve --no-reload` :8146 from the ticket worktree, DB multi_food_db_qa3846 (private), fronted by a logging QA proxy :8147.

- AC1 PASS · AC3 PASS (J2 8=8 / 1=1; placed children 8.00/1.00; control shows 1.00 for the surged store)
- AC2 FAIL (cod_cap leaves the auto-selected cash selected; empty re-opened sheet on stale zone data)
- AC4 PASS · AC5 PASS (reachable states; null-module branch not UI-reachable) · AC6 PASS (reason branch at Place + PUT on both surfaces; validator 403 without reason → generic)
- AC7 PASS (home prompt, payment-screen dialog, DigitalPaymentFailedScreen); order details not reachable for the child (not listed)
- AC8 PASS (debug mirror; FA disabled on suffixed package)
- AC9 PASS · AC10 UNVERIFIABLE · AC11 PASS · AC12 UNVERIFIABLE · K3 UNVERIFIABLE (pre-existing guest multi-store blocker, same on control)
- AC13 FAIL (AR cash copy ellipsized at 360dp×1.3; EN/AR strings exact, app-owned proven via sentinel)
- AC-LOG PASS · AC-REG PASS (A/B identical: flag-OFF single 21.13, flag-OFF same-module 55.80, flag-ON single-module 55.80; 0 validate) · AC-TEST PASS (7480 tests, 25 fails == base set)

# Cycle 1 (delta re-QA) — build 29bc434b4, emulator-5580 at 360dp x font 1.3 throughout, own serve :8146 (cwd = ticket worktree @ 29bc434b4) via proxy :8147, DB multi_food_db_qa3846 (proven: flag ON only in copy; surge id 3 title served)
- TB1 PASS (pending cash auto-select dropped at cod_cap verdict + warning; offline pick dropped at cash_removed:true). Residual Low: cod_cap from the quote not rendered until verdict/Place tap (bug-codcap-pending-display-lag.*), AC2 unknown-branch permits it
- TB3 PASS (stale zone OFF, server ON: Place cash -> 403 -> sheet Paypal/Razor pay; Paypal -> group placed 91457/91458)
- TB5 PASS (cod: partial dropped, online offered; both: partial kept, online remainder)
- TB2/AC13 PASS (3 toasts EN+AR full copy at 360dp x1.3, visible ~6s; ordinary toast 3-line cap + default duration)
- TB4 PASS order-details path (module_id 2 w/ header 1). Residual Low: DigitalPaymentFailedScreen Pay Now still header module (bug-tb4-payfailed-screen-header-module.log)
- RB5 PASS EN+AR (cash offered / no cash / switch refused same dialog)
- AC6/AC7/AC8 spot-checks PASS · AC-REG PASS (21.13 / 55.80 flag OFF, cash default, 0 validate)
- Confirm-only: (a) NOT reproduced (group card expands, child details reachable); (b) reproduced; (c) confirmed by code + live body (pre-existing)
- AC-TEST: UserApp 7501 tests, 25 fails == prior set; nears_dls 2915, 2 pre-existing n_store_card fails
