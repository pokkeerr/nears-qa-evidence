# NEARS-1068 QA progress (emulator-5556, worktree @7fd0ed23)
- AC1 in-zone deep-link store 59: PASS — store screen rendered (products/categories), /stores/details/nears-257-fixture-store=200 in ~1s, view_store{store_id:59}, 0 NPE, 0 exceptions. shot ac1-inzone-store59-rendered.png
- AC2 out-of-zone deep-link store 3168 (slug grocery-food): PASS(fail-soft) — relocation to zone 400 proceeded, /stores/details/dama-baqala-baqala-3=200 ~1s, view_store{store_id:3168}, home-for-new-zone rendered (not blank, not crash), 0 NPE. Pre-existing checkModuleId no_module_found snackbar→home + stale /stores/details/59=403 [FAIL] (both properly logged, untouched by diff). shot ac2-outofzone-store3168-relocated.png
- AC3 no NPE: PASS — 0 "Null check operator used on a null value" across all 3 deep-links (store59 in-zone, store3168 & store59 out-of-zone relocation).
- AC4 latency: PASS — store details 200 in ~1s each; no multi-second/40s spinner hang; reverted client-await not reintroduced.
- AC5 regression home-tap (empty-slug): PASS — store screen rendered (products/Add To Cart/Filter), /stores/details/59=200, view_store{store_id:59}, 0 NPE. shot ac5-regression-home-tap-store.png
