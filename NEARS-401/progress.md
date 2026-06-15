# NEARS-401 Basket Reskin — QA Progress Checkpoint

Device: emulator-5554 (Android 17 / API 37), QA SHA 013a1de7, build via `flutter run` from worktree.
Backend: http://10.0.2.2:8000 (local Laravel, seeded). Login: customer@nears.com (Customer Nears). Zone: Demo Zone — Dhaka.

## Observed live (shot 01-basket-top.png)
- A1 app bar: navy header, white "Your Basket", white shopping_basket glyph trailing — PASS (F-401-1 resolved)
- B1 ETA banner: mint surface, navy text "⚡ Arriving in ~20 mins" — PASS (solid mint = accepted DLS divergence)
- C1 item cards: per-item white NearsSurfaceCard + soft shadow — PASS
- C2/G4 image 80×80 — PASS
- C3 OOS overlay: Banana shows "Not Available Now" tint — PASS (capability live)
- C4 navy name, C6 grey qty subtitle, C7 NearsBadge unit chips (DOZEN/KG) — PASS
- C8 discounted price mint/navy + strikethrough original (Banana د.إ.1 / د.إ.2) — PASS
- C11 X-remove glyph top-end — PASS
- C12 NearsQtyStepper mint −/+ — PASS
- C13 line totals (د.إ.1, د.إ.24) — PASS
- D1/G1gap Add More Items = navy-outline NearsSecondaryButton + circle icon — PASS
- I1 suggested rail "You May Also Like!" — PASS
- K2 Proceed to Checkout mint pill + trailing arrow — PASS
- K4 fromNav spacer above dashboard nav — PASS
- L3 cross-store dialog (shot 12) — branded navy/mint — PASS

## Observed live (cont.)
- G1 substitution: all 5 options visible, default "Call me ASAP" mint check (shot 02); single-select + reselect to "Please cancel the order" (shot 03) — PASS
- H1 order summary card: boxed NearsSurfaceCard, Subtotal/Discount(mint tag)/large navy Total, no delivery-fee line (shot 02) — PASS
- H1 math: 1 Banana(~1.8)+1 Pretzels(24)=Total 26; Pretzels qty 1→2 → Subtotal/Total 26→50 live (shot 06) — PASS
- Substitution PERSISTS into Checkout: "Please cancel the order" shown on checkout screen (shot 07) — PASS (HARD)
- K3 OOS guard: 1st Proceed stayed on basket (Banana OOS overlay); after removing OOS item, Proceed → checkout — PASS
- C12 dec-at-1 removes: Banana qty1 decrement removed it, badge 2→1 (shot 08) — PASS
- C11 X-remove: removed Pretzels → empty (shot 10) — PASS
- L1 empty cart: "Your cart is empty" + navy app bar/glyph (shot 10) — PASS chrome; ILLUSTRATION still legacy 6amMart clip-art (NOT Nears-branded) → regression/followup, NoDataScreen out of ticket scope per DoR Ruling 7
- C14 swipe-to-delete: code-confirmed Slidable end-action; adb swipe gesture flaky in automation (snaps back) — partial-demo, X-remove proves removal path

- L2 loading skeleton: caught live (shot 11) under throttled net on synced-item qty update — shimmer NearsSurfaceCard row (80×80 block + 2 lines), NO spinner, 1 row = live cart count (dynamic rows cycle-1 fix), no layout jump — PASS
- G1 default reset: after hot restart, substitution reset to "Call me ASAP" (index 0) — PASS

- L7 dark mode: navyContainer cards, mint name/price/Total, mint discount line, mint CTA (shots 13,14) — PASS
- L6 RTL/Arabic: image→right, X-remove+stepper→left, ETA+badge mirrored, substitution radios→start(right), summary labels right/values left, CTA arrow points left, basket glyph→trailing(left), bottom nav mirrored (shots 15,16) — PASS
- D1 add-more nav: → Daily Fresh Market store item page, cart preserved "1 Item", back→cart intact (shot 17) — PASS
- Automated backstop: flutter test test/features/cart → 45/45 PASS (incl cart_skeleton_widget_test)

- L4 guest login-suggestion: logged out → guest; sheet did NOT fire on tab-hosted cart. Code (cart_screen.dart:124-129): gated by `isGuestLoggedIn()` + `Get.currentRoute == RouteHelper.cart` — tab-hosted cart route ≠ RouteHelper.cart, so guard suppresses it on the nav-shell path (pre-existing, NOT changed by this ticket; shared-widget concern out of DoR scope). Marked unverifiable-via-this-path.
- Runtime errors: NONE across full session (Dart MCP + ui_errors clean, no cart overflows/exceptions)
- Automated backstop: flutter test test/features/cart → 45/45 PASS

## Regression/findings
- L1 empty-cart illustration is LEGACY 6amMart clip-art (person+cart), not Nears-branded navy/mint. Chrome (app bar/glyph/text) IS branded. NoDataScreen is a SHARED component, explicitly out of this ticket's scope per DoR Ruling 7 → regression_bug/followup, NOT a task_bug.
- C14 swipe-to-delete: code-confirmed Slidable end-action (error-red); adb swipe gesture snaps back in automation (couldn't capture the revealed action). X-remove + dec-at-1 prove the removal paths. Functional capability present.

## VERDICT: PASS
