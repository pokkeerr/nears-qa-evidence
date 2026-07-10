# NEARS-1032 QA progress — emulator-5554, zone 1 (Dhaka demo)
Build: worktree feat/NEARS-1032-tap-through-module-switch @34f6139d
Backend: primary :8000 (no BE change). Locale: English.

## Pre-flight
- Unit backstop: 14/14 PASS (ensure_module_context, module_controller_verified_switch, item_widget_tap_override). AC4 fail-closed paths all emit [FAIL] endpoint=/api/v1/module + snackbar.
- Global search API zone-1 verified cross-module: chicken=grocery1/food6/pharmacy1; oil=grocery3/food1/pharmacy3.

## AC results
- AC6 reworded copy: PASS — "Your basket has items from another module..." (another module, not category). Shot 02.
- AC6 CANCEL: PASS — No → no clearCart, no setModule, results+cart intact.
- AC6 CONFIRM + AC1/AC2: PASS — Yes → cart/remove 200 (clear FIRST) → items/details/393 200 (no 404) → view_item. Backend probe: item393 moduleId=1→404, moduleId=2→200, absent→403 (proves header flip to B). Shot 03.
- AC3 bucket-under-B: PASS — cart shows only Chicken Burger (food/module2), Cream Cheese cleared, food-only recommendations. Shot 04.
- Logs-first: only [FAIL] lines are get-zone-id 404 at startup (17:16-17:17), NONE during any 1032 action. (regression candidate, pre-existing)
- AC4 fail-closed: unit-pinned PASS (14/14) — null/unresolved-list/failed-switch → [FAIL] endpoint=/api/v1/module + snackbar + nav aborted. Not live-forceable.
- AC5 See-all: PASS — route module=food-restaurant → search/unified 200 → existing SearchScreen "Items(6)/Stores(0)/Filter" prefilled 'chicken'. Shot 05.
- AC7 item: PASS — after tap-through, back lands on module home (Search your desired...), no stale global results.
- AC7 see-all: PASS — back → food module home, not global results.
- AC7 store: PASS — Corner Grocer → route module=grocery-food → stores/details/36 200 → view_store; back → grocery home (offNamed). Shot 07.
- Regression: home item card (details/3 200) PASS; module-search item (details/6 200) PASS; module-search Stores-tab store card = code-verified unchanged (onTapOverride?? null = identical). Shot 06.
- AC8 RTL/Arabic: PASS — dialog "...من وحدة أخرى..." (another module), RTL mirrored, no truncation; CANCEL intact. Shot 08. Dark mode DEFERRED (light-first policy).

## FINDINGS
- task_bug#1 (breaks_ac:false, medium): tap-through switches to section.moduleId; item-detail filters by item.module_id. 7 zone-1 items (39,47,60,73,75,76,77) mis-seeded (item.module_id != store.module_id) → 404 on tap (error UI + [FAIL] log, NOT silent). Fix: switch to tapped product's module_id (present in /search/global payload). bug-tapthrough-section-module-404.log
- regression_bug (data, medium): 7 mis-seeded items above (item.module_id != store.module_id) — data + 1027 grouping.
- regression_bug (low, pre-existing): get-zone-id 404 x5 at startup during location resolution.
- note: global search route throttle:30,1 — easy to 429 under rapid use (test artifact here; error handled + logged).

VERDICT: PASS (core feature proven on valid data; failures non-silent + logged; no 1032-caused regressions in shared ItemWidget).
