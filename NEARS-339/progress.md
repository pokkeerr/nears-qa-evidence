# NEARS-339 QA progress (live checkpoints)
Device: emulator-5554 | branch feat/NEARS-339-food-home-semantics @ 85855730 | fix_cycle 0

## Pre-flight
- baseUrl -> http://10.0.2.2:8000 (local backend, useHttps=false) — OK
- backend :8000 responding 200 — OK
- device lock acquired $HOME/.nears/qa-locks/emulator-5554 — OK
- AC6 (vacuous): docs/userapp-navigation-guide.md has sections 5.1-5.7 only; no 5.9, no food-home hazard text. CONFIRMED N/A-AT-BASE.

## Logged-in phase (customer@nears.com, zone 1, address "Others/Mirpur-11 House 21 Road 3 Section 11")
- AC1: 3 consecutive Food & Restaurant home entries in ONE session; uiautomator dump (a11y flush) after each. crash-sig grep (Null check operator|parentDataDirty|visitChildrenForSemantics|infinite width) = 0; ui_errors empty; DTD runtime errors: none. PASS (logged-in)
- AC2: food home dump = 39 non-empty labels per entry. PASS (logged-in)
- AC4: ui_find/ui_tap "Garlic Bread" (Most Popular card) -> item-detail sheet (Add To Cart/qty controls) -> Dismiss -> back on food home. PASS
- Rail renders: "Most Popular Items" header + >=3 cards (French Fries Large, Classic Cheeseburger, Garlic Bread); card node 525phys/dpr3 = 175 = 160 card + 15 pad — fix bound live. Shots 10/11/12.
- '+': CartCountView icon-only (no a11y label — PRE-EXISTING gap on all ItemCard rails). Tapped via live-bounds-derived point -> "Start a new basket?" dialog -> Yes -> stepper qty "1" exposed in card label group. WORKS.

## Resumed session 2026-06-12 (device emulator-5556 — 5554 locked by NEARS-336; fresh install from worktree @ 85855730)
- Pre-flight (5556): baseUrl -> http://10.0.2.2:8000, backend :8000 = 200, lock $HOME/.nears/qa-locks/emulator-5556 acquired. OK
- AC5 (logged-in): Grocery & Food home = 44 labels, crash-grep 0, ui_errors empty, DTD clean. Shot 14. PASS
- AC5 (logged-in): Pharmacy home = 61 labels, crash-grep 0, ui_errors empty. Shot 15. PASS
- AC5: shop/ecommerce home N/A — module list in seed = Food & Restaurant / Grocery & Food / Pharmacy only (no ecommerce module).
- Module-switch rapid (Jira c10387): 6 quick module entries (food/grocery/food/pharmacy/food/food, ~2s apart, uiautomator flush mid-transition) -> parentDataDirty grep = 0, broader sig grep = 0, DTD clean. PASS
- AC3 (logged-in re-confirm): Profile/menu screen fully labeled after food visits + module switches (37 labels). Shot 16. PASS (Search leg = prior shot 13 on 5554)
- Dark mode: rail "Most Popular Items" renders at scroll 7, crash-grep 0. Shot 17. OK
- Arabic/RTL (+dark): rail "العناصر الأكثر شعبية" renders, 69-label food home, crash-grep 0. KNOWN polish observed: first rail card flush to trailing edge (no leading inset) in RTL. Shimmer not re-observed (load-time only). Shot 18. OK (not failing — known)
- Settings reverted: English + light restored.
- GUEST phase (logged out via Profile->Logout; zone-1 via Change Location -> Set From Map -> Pick Location @ House 21 Road 3 Section 11 Dhaka / Mirpur-11):
  - AC1 guest: 2 consecutive food-home entries, uiautomator flush each: crash-grep 0, ui_errors empty, DTD clean. PASS
  - AC2 guest: 37 non-empty labels per entry; VisitAgainView absent (expected when logged out). Shot 19. PASS
  - AC3 guest: after food visits -> Search tab (10 labels) + Profile tab (19 labels) alive, crash-grep 0. Shot 20. PASS
- NOTE/drift: bottom-nav tab labels (Home/Categories/Search/Basket/Profile) now LIVE in a11y tree on this branch — NEARS-334 §5.1 "aspirational" note is stale. Running-order banner still replaces the nav bar (dashboard_screen.dart:212) but is a Dismissible (swipe restores nav).
- GMS LocationSettingsChecker dialog loop on fresh 5556 boot — resolved via settings location_mode=3 + "Turn on" (device-level, not app data).
