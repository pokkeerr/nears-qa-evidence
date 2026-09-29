# NEARS-3843 QA progress (phase 8, cycle 0)

Build: fix `98a12e2de` vs base `dae75e9ec` (detached worktree), emulator-5570, debug, light mode.
Backend: own `php artisan serve --no-reload` on :8043 from the fix worktree, DB `nears_qa_3843` (private copy; proven via /api/v1/config toggle_veg_non_veg=true while multi_food_db=0).
Active module in every state read live through the VM service (`ModuleController.module?.moduleType`).

| AC | Verdict | Evidence |
|---|---|---|
| AC1 [ui] | PASS | Fix: grocery / food / no module -> Ghee (and Red Apples) no icon + "N kg", Veggie Burger green veg icon in all 3 (`ac1-fix-*.png`, pixel classifier). Base control: food active -> Ghee red non-veg + Red Apples veg (wrong); grocery active and no module -> Veggie Burger no icon (wrong) (`ac1-base-*.png`). RTL AR and 1.3x OK (`ac1-fix-rtl-ar-*`, `ac1-fix-textscale-1.3-*`). No module reached by VM `Get.toNamed(cart)` (no UI path). |
| AC2a [behav] | PASS (fixture substituted) | Item 42's stock=2 is masked by running flash sale 1 (available_stock 50), so the test used item 105 Red Apples (Nears Mart, grocery, effective stock 9). Fix: food active and no module -> "Only 9 available", row stays 9. Base control: food active -> 9 to 10. |
| AC2b [behav] | PASS | Fix: grocery active and no module -> Veggie Burger 1 to 2. Base control: grocery active and no module -> "Only 0 available", stays 1. |
| AC3 [behav] | FAIL | Grocery row, food active: sheet shows qty 9, + capped, Update -> no duplicate (PASS; base control lets it go past the cap to 11). Food row, grocery active: sheet shows disabled "Out of Stock", with no stepper and no cart quantity (fix == base). Cause: `item_bottom_sheet.dart:450-461` isOos reads the ambient module stock. |
| AC4 [unit] | PASS | staples_add_all_row_module_test 5/5. Device: add-all on schedule 2 (store 37) -> no stores/details before POST cart/add; the post-navigation stores/details sequence (1, 37, 37) is identical to base. |
| AC-LOG | PASS | Stock blocks: no [FAIL] (only the generic `[ERR] error snackbar shown`, same as base). Staples miss: exactly one `[FAIL] CartStoreModuleFailure ... store_id=37`. Null/unknown row type not reachable with seeded data -> unit-proven (module_helper_row_module_config_test 7/7). |
| AC-REG | PASS | Flag OFF (fix): grocery cart = 41,105, no icons, + capped at 9; food cart = 18, veg icon, + allowed. Flag ON rows whose module == active module render identical to base. Mixed wrong-icon state is not reachable with the flag OFF (server cart is module-scoped). |
| Backstop | PASS | Full UserApp suite +7371 -25; 25 failures identical to the base list. |
