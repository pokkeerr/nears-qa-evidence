# NEARS-509 QA progress (restart after API-529 crash)

Device: emulator-5556 (Pixel_10_Pro_2), worktree feat/NEARS-509-basket-ui @8801118a
App pid: 24521 (UserApp). Backend: shared dev :8000 (HTTP 200), baseUrl http://10.0.2.2:8000 (real local).

## Reused evidence (prior crashed run — verified on disk)
- AC-1 EN light: ac1-appbar-en-light.png (title "Basket") — OK
- AC-2 no line-subtotal + aggregate qty1/qty2: ac2-card-qty2-no-subtotal.png, ac2-order-summary-qty1.png, ac2-order-summary-qty2.png, ac2-discounted-card.png — OK
- AC-3 pill/nav + running-order: ac3-pill-vs-nav-fromnav.png, ac3-checkout-gap-fromnav-runningorder.png
  (NOTE: both AC-3 shots have running-order banner covering the pill area; need a clean pill-vs-nav capture)

## Gaps to fill (live)
- [x] G1 AC-1 Arabic appbar = "سلة التسوق" (reuses nav tab term), clean RTL, no overflow; full layout
      mirrored incl. checkout arrow flipped (NEARS-401). Dark-mode appbar legible, mint accents OK.
      Evidence: ac1-appbar-ar-light.png, ac1-appbar-dark.png. PASS. No runtime errors.
- [x] G2 AC-2 expanded addon card (Beef Shawarma, 2 addons) — right col (close+stepper) top-anchored,
      reads intentional; addon detail flows full-width BELOW the row; NO awkward gap, balanced. PASS.
      Evidence: ac2-addon-card-collapsed.png, ac2-addon-card-expanded.png. No overflow/runtime errors.
- [x] G3 AC-3 pill<->nav gap (fromNav=true, gesture-nav): measured pill.bottom=2581, nav-icons.top=2683
      => 102px (~29dp); nav card visual top is higher (8dp+ internal pad) so visual gap ~12-18dp = small/
      flush, intended. Pill NOT pushed high; NO double-inset excess. dashboard SafeArea(bottom:false)
      (NEARS-340) + bottomNavigationBar reserves inset => pill SafeArea(bottom:true) adds ~0 here.
      Evidence: ac3-pill-vs-nav-clean.png. PASS (flush). No task-bug.
- [x] G4 AC-3 fromNav=false (View Cart push from store/search): back-arrow shown, NO bottom nav, pill
      flush at bottom safe-area edge, NO clearance spacer. Correct. Evidence: ac3-fromnav-false-pushed-cart.png. PASS.
- [x] G5 Skeleton: code proof cart_skeleton_widget.dart has 3 lines (name/qty/stepper-pill), NO subtotal
      placeholder row; mirrors post-removal layout. Live qty++ refresh clean, no layout jump, no errors.
      Evidence: ac5-skeleton-refresh.png + code. PASS.
- [x] G6 Empty-cart NoDataScreen unaffected — clean basket icon + "Your cart is empty", nav present.
      Evidence: ac-empty-cart.png. PASS.
