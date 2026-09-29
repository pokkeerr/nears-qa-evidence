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
