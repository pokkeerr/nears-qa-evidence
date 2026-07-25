# NEARS-1350 NBadge — QA (build cc13c292, emulator-5554 light/LTR Dhaka + emulator-5556 light Abu Dhabi)
## Live UserApp (in-context)
- AC1 CLOSED=error-red (stacked home + row list), ETA=mint(speed), NO row overflow (NEARS-507). logs clean.
- AC3 priceOff=red (-10/-14/-29%, 10% OFF). logs clean.
- AC4 discount/LIVE=navy, banner=navy+white+mint btn, LIMITED TIME OFFER=mint, LIMITED OFFER=navy. logs clean.
- App boots clean; no Flutter/NBadge exceptions in logcat or ui_errors. (ANRs seen were emulator-perf on 5554, not app.)
## Component render (golden PASS + AC8 unit token-matrix 143/143 + code review) — live surfaces env-gated
- AC2 delivery=navy bg + MINT fg + bolt (navyMint). Unit: "delivery paints navy fill + MINT label + bolt" bg==navy fg==mint. Golden delivery+rtl-delivery pass. Live order_tracking/your_tower gated (all stores CLOSED @4am, clock un-rootable; no active order); PDP delivery_eta_pill orphaned (pre-existing, 0 call sites).
- AC5 group_tracking: open->success(green open hue), closed->error(red), inflight->mint. Mapping+golden. Needs active order group (gated).
- AC6 RTL golden passes (bolt mirrors, textDirection threaded). Live in-context RTL not reached (locale non-settable non-root; bottom-nav a11y-unlabeled -> Profile/language toggle unreachable). Dark DEFERRED (reskin light-first) -> non-gating; dark golden passes as supplementary.
## Automated
- packages/nears_dls flutter test 143/143. flutter analyze nears_dls 0. UserApp badge tests 41/41 (incl NEARS-507 overflow). analyze UserApp lib: 1 PRE-EXISTING info lint cart_screen.dart:292 (untouched file).
