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

# Cycle 2 (delta re-QA after rebase onto 3cc7d2489 incl. NEARS-3887) — build 1912013b2 (clean tree), emulator-5580 360dp x font 1.3, own serve --no-reload :8146 (cwd ticket worktree @ 1912013b2, freshness PASS) via proxy :8147; DB multi_food_db_qa3846c2 (fresh dump of multi_food_db + Nears3858 seeder; flag ON, FCM push file NULL, mail status 0, free-delivery 0, dated surge "QA3846c2 Rain" +7 zone1/module1 — copy-only, proven served via get-surge-price). 3887 proven served: digital validate with zone1 digital_payment=0 -> 200 rows digital_unavailable_in_zone.
- A PASS: 1 group/validate payment_method=digital_payment -> 200 cash_removed:true; sheet Paypal/Razor pay only (cash+offline hidden); [INFO] probe cash_removed=true; checkout_cash_removed_shown{mixed_basket_cash_unavailable} once. RB4 overflows only (pre-existing).
- AC3 J2 PASS: Grocery (surged) 8.00 == validate dc 8; Kitchen 1.00 == dc 1.
- E PASS (digital-first): store 91158 minimum_order=100 -> ONE digital validate, row minimum_order, no second call.
- B1 PASS (server zone1 digital OFF, cached zone rows ON): digital validate -> 200 rows digital_unavailable_in_zone -> [INFO] "probe method refused reason=digital_unavailable_in_zone" -> cash validate -> 200 cash_removed:false. Section: Cash on Delivery auto-selected; sheet Cash + Pay Offline, Paypal/Razor pay hidden.
- NEARS-3912 confirm-only: REPRODUCED. Offline offered on group basket; pick -> Place -> group/validate 403 {code:payment_method, message:"The selected payment method is invalid."} no reason; [FAIL] reason=none; no order (max id 91415 unchanged), no group/place. Generic 'something_went_wrong' snackbar is NOT visible: confirm sheet stays open, frames 1.2-5.0s pixel-identical to pre-tap.
- B1 digital-pick reset PASS: probe delayed 15s/call; Paypal picked (index=2) between the digital refusal and the cash reply -> verdict -> "payment method selected index=-1"; sheet then Cash + Pay Offline only.
- B2 PASS (zone rows refreshed via address re-select: zone1 digital_payment=false): ONE cash validate -> 200 cash_removed:false; cash auto-selected (index=0); sheet Cash + Pay Offline, no digital.
- AC6 spot PASS: cash selected, server zone1 digital flipped ON after probe -> Place -> 403 reason=mixed_basket_cash_unavailable (server msg = proxy sentinel) -> index=-1, reopened sheet Paypal/Razor pay only, app copy toast; [FAIL] reason=mixed_basket_cash_unavailable corr 215c4eb5 == proxy rid; checkout_cash_removed_shown once.
- AC13 spot PASS: EN toast full copy (6 lines, no ellipsis) at 360dp x1.3, visible 1.4s..>=6.8s. c2-AC6-AC13-* shot.
- Extra (2): NO. Toast [78,1278][1002,1980] covers Paypal row [63,1728][1017,1896]; tap at 5.9s (toast up) swallowed; positive control after toast registers gateway index=0.
- AC6 part 2 PASS: global COD off after probe, cash picked -> Place -> 403 {code:cash_on_delivery, reason:payment_method_unavailable} -> generic path: [FAIL] reason=payment_method_unavailable, NO index reset, NO mixed toast/sheet, NO checkout_cash_removed_shown, no order. (Generic snackbar hidden under confirm sheet: frames identical after 1s = NEARS-3894 Part B shape.)
- D1 (zone1 digital off + zone1 cash off, global on): cash probe -> cash_unavailable_in_zone; digital probe -> digital_unavailable_in_zone; exactly ONE [FAIL] "no payment method passes reason=digital_unavailable_in_zone"; auto-selected cash reset to -1; checkout open; sheet EMPTY (no rows: offline hidden by rule, wallet 15.84<38.66); Place tap -> reopens empty sheet, no validate, no order, NO "no payment method" message (wallet_status=1 so no_payment_method_is_enabled branch not reached).
- E (cash-first) PASS: module_zone(1,1) cod cap 5 -> ONE cash validate, row cod_cap, no digital fallback; checkout_cash_removed_shown{cod_cap}; auto cash dropped index=-1.
- F PASS: probe held 40s; address changed mid-flight -> new probe (cash, new lat) set the verdict; old held digital reply arrived after -> "[INFO] probe reply dropped — basket or address moved"; no stale verdict.
- (relaunch 1: global digital OFF, wallet off) C PASS: ONE validate payment_method=cash_on_delivery -> 200; cash auto-selected; sheet Cash + Pay Offline, digital never shown.
- D2 (global digital off + zone1 cash off, wallet off): ONE cash validate -> cash_unavailable_in_zone; NO digital call; ONE [FAIL] "no payment method passes reason=cash_unavailable_in_zone"; cash reset; Place -> confirm sheet (SELECT PAYMENT METHOD) -> confirm -> [FAIL] PlaceOrderBlocked reason=no_payment_method_is_enabled; the snackbar is NOT visible (frames identical, under confirm sheet). No order. -> 'say so' gap logged (bug-no-method-state-not-said-visibly.log).
- (relaunch 2: settings restored) H flag ON same-module (91158 + Corner Grocer 36): 0 group/validate; 51.24 + 2.00 + 2.56 = 55.80 == base.
- H flag OFF (relaunch 3/4/5): single-store 12.50 + 8.00 + 0.63 = 21.13; same-module 2-store 51.24 + 2.00 + 2.56 = 55.80; cash default; 0 group/validate in all; mixed server cart under flag OFF shows only the module's own store in the Grocery basket, 0 validate. Base numbers unchanged by NEARS-3885.
- I (guest, relaunch 6: guest_checkout_status=1 on copy): 0 group/validate with contact fields empty; after name/phone/email filled still 0 — fees never land (Delivery Fee -1.00, no delivery-quote call) = pre-existing NEARS-3906, so "re-sent once valid" UNVERIFIABLE (same blocker as cycle 0).
- G PASS: 0 PII hits (name/phone/email/address/coords) across every I/flutter line this cycle; refusals are [INFO] "probe method refused reason=<token>"; the only probe [FAIL]s are the two no-method lines (one per D run).
