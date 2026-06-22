# NEARS-494 v2 — delta re-QA (fix-cycle 1, cycle 2 of 2) — emulator-5556

Started: 2026-06-22. Worktree: nears-NEARS-494-cart-authoritative-v2.
Backend: local 127.0.0.1:8000 (HTTP 200), queue worker up. baseUrl OK (10.0.2.2:8000).

## Checkpoints

### CYCLE 2 (fix re-verify) — emulator-5556, 2026-06-22
- AC1 grid card: Banana +10 burst → 1→11, HELD (no snap-back). One `cart/update`, no `cart/list` mid-burst. PASS
- AC2: burst = exactly one debounced outward `cart/update` per burst, no per-tap, no `getCartDataOnline`. PASS
- TB1 (LIVE ItemBottomSheet, simple in-cart): sheet shows live cartQuantity (11, not reset-to-1).
    in-sheet + burst 11→21→22 instant, HELD; sheet Total 33 AED + card badge 22 in lock-step; CTA "Update In Cart" no spinner. PASS
    Confirmed driving the REAL bottom sheet (item_bottom_sheet.dart) not dead item_details_screen.dart.
- Observed PRE-EXISTING crash on variation-item REMOVE (item 84 Dove): ItemService.prepareVariationType NPE.
    Verified present on pre-494 parent 6c04b65f^. regression_bug, does not gate. See bug-variation-remove-npe.log
- TB2 (optimistic-row no-crash): raced basket open 3 ways; Red Apple optimistic line renders w/ correct
    discounted price, NO Null-check NPE. PASS. See v2-tb2-fix-verified.log
- Observed PRE-EXISTING cosmetic RenderFlex 19px overflow item_widget.dart:822 (recommendation card price row),
    NOT in v2 diff (NEARS-397). regression_bug, does not gate. See bug-recommendation-card-overflow.log
- AC3 basket line +/- : no full-page spinner, only line+summary repaint; one debounced cart/update, no cart/list. PASS
- AC6a cross-store: "Your basket has items from another store..." dialog fired; Yes cleared+added. PASS
- AC4 cap (Sample Product cap=2): climbed 1->2, blocked past 2, HELD at 2 (no overshoot/snap-back),
    "Maximum quantity limit 2" Option-A message shown. PASS
- CRITICAL-1 (discounted price -> checkout): added discounted Rice 5kg (12 from 15) optimistically;
    checkout review shows Rice 1×12 AED (discounted, NOT 15), Sample 2×10=20, Total 32 AED. PASS.
    Did NOT Place Order (read-only QA, no DB mutation).
- AC8 (no green-then-red): every card add (Banana item 3) fired NO green "added to cart" snackbar;
    item_controller diff confirms showCartSnackBar() removed on the optimistic return. PASS
- AC9 (add_to_cart single-fire): each optimistic card add fired exactly ONE `add_to_cart {item_id..}`
    in stdout (observed per add); no duplicate/per-tap analytics. PASS
- The pre-existing item_widget.dart:822 RenderFlex overflow recurs on discounted recommendation cards
    (19px Red Apple / 31px Cola) — cosmetic, not in v2 diff. regression_bug.
- AC6c OOS block: QA OOS Fixture (stock 0) add blocked, "Out of Stock", cart unchanged. PASS
- RTL cap (Arabic): basket RTL-mirrored; Sample + at cap -> "الحد الأقصى للكمية 2", HELD at 2. PASS
    ar.json `only_quantity_available`="المتوفر فقط @quantity" added in v2 diff; maximum_quantity_limit present.
- Dark mode toggle confirmed OFF (light mode) per deferral; no dark-mode checks performed.
- Cold-load persistence: hot restart -> basket reloaded from server with Rice 5kg (12/15, qty1) +
    Sample Product (10, qty2) intact + discounted pricing. PASS
