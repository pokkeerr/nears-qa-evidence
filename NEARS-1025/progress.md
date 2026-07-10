# NEARS-1025 QA cycle-2 (delta) progress — device emulator-5554, branch @65687870

- AC10 (panel renders): PASS (reused prior + re-observed) — out-of-zone recovery panel shows at checkout. shot c2-10-panel-renders.png
- AC11-a (red-screen GONE gate): FAIL — getModuleData crash gone (prong-1 held), BUT a NEW/moved "Null check operator" _TypeError fires during the pick at PricingService.calculateOriginalDeliveryCharge:672 (`address.zoneData!`, 5th unguarded site the fix missed) via async resolution-window race. shots c2-11a-inzone-pick-checkout.png, c2-11b-pricing-crash.png; log bug-c2-changeloc-pick-pricing-redscreen.log
- AC11-b (in-coverage pick -> normal checkout): FAIL-during-transition — settled checkout renders correctly (COD/pricing/Banana line item) but the pick transition throws (same defect as AC11-a).
- AC11-c (out-of-coverage pick -> panel re-shows): UNVERIFIABLE via saved-address pick — cycle-1 serviceable-filter excludes out-of-coverage addresses from the sheet (only Dhaka offered); would need Add-New-Address out-of-zone pin. Blocked by AC11-a anyway.
- AC11-d (fail-soft on failed resolution): NOT REACHED — the SUCCESSFUL-resolution path already crashes (AC11-a), so fail-soft-on-failure is moot until AC11-a fixed.
- Regression (settled in-zone checkout, fully-stamped zoneData): PASS — re-enter checkout with Dhaka settled = 0 runtime errors, COD/payment/total render. Prong-1 null-guards did not break the happy path. shot c2-regr-settled-inzone-checkout.png

VERDICT: FAIL (AC11-a gate not met). Last allowed cycle -> conductor escalates.
