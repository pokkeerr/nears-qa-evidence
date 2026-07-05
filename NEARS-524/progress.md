# NEARS-524 Buy It Again — QA progress (fix_cycle 1, Option A delta re-QA)

Device: emulator-5554 (nears_qa_wave56, headless swiftshader). Backend: worktree Admin @:8000. NEW code from worktree.
Precondition: sort setting all_stores_sort_by_temp_closed UNSET → temp-closed stores kept. user6 home = store 8 coords.

## RESULTS (all live unless noted)
- AC1 populated rail: PARTIAL/FAIL — rail RENDERS with real purchase history, BUT resolved store 9 "Organic Shop" (4586m) instead of the actual nearest store 8 (4.8m, present+first in list). Rail shows Strawberries(52)+Organic Bananas(58)=store9; expected store8 Orange Juice(145). => "nearest store" not satisfied. shots 11.
- AC2 taps: PASS — card body → items/details/52 (Organic Shop detail); "+" pill → POST cart/add 200 + add_to_cart{item_id:52} analytics, NO nav, qty stepper (Remove|Add) in place. shots 12.
- AC3 guest: code-unchanged (isLoggedIn ? view : SizedBox; resolveBuyItAgain guest→clearBuyItAgain→no call); cycle-0 confirmed live (shot 02). Not re-demoed live cycle-1 (order-card UI overlap on logout).
- AC4 Arabic RTL: PASS — header "اشترِ مجدداً" right-aligned (x1007); rail mirrored (Strawberries x958 right / Organic Bananas x752 left = reverse of LTR). shot 13. zero errors.
- AC5 leak: PASS — rail shows ONLY resolved store's items (52/58); no other-store/cross-zone/campaign leak.
- CR-2 cold-cache self-heal (HIGH bug): PASS — fresh install + cold relaunch → buy-it-again fired 200 on FIRST grocery load (cache-settle + network-settle), rail populated, not stuck hidden. FIXED.
- CR-3 pull-to-refresh: PASS — pull-refresh re-fired store list + buy-it-again (200), rail re-resolves.
- Opt-in scoping: code-verified — onListSettled only passed by the module-home fetch (store_controller getStoreList), not filter/pagination reloads.
- Logs: zero [ERR]/[FAIL] entire session (flutter run + logcat).
- Automated: flutter buy_it_again + nearest_store + cold_cache tests, phpunit BuyItAgain (to run).

## VERDICT: FAIL
Blocking: nearest-store resolution selects a FARTHER store (9) over the actual nearest (8) → AC1 "nearest store" broken for the demo account (rail shows the wrong store's history). Everything else (populate/taps/RTL/CR-2/CR-3/no-leak) works — fix is narrow (nearest-store selection). Root cause TBD by engineer (resolution logic vs distance/location-state); Store model DOES parse API distance (metres), API probe with home coords gives store8=4.8m nearest, so the app used a different origin or list variant. Emulator scroll-fling broken (worked around via wm density 200); AC2/AC4 unblocked by density.
