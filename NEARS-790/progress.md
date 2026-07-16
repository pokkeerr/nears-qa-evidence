# NEARS-790 QA progress — VendorApp splash push/profile race
device: emulator-5556 (reclaimed stale NEARS-791 dead-pid lock) | build: worktree feat/NEARS-790-splash-push-profile-race

- ENV: fresh worktree missing gitignored VendorApp/android/app/google-services.json -> Firebase.initializeApp() red-screen; copied from primary tree, rebuilt. (bootstrap gap, not a product defect)
- AC4 PASS: unit test splash_store_module_config_test.dart green (null profile -> Module(newVariation:false), no throw). No null-check exception in logcat across nav.
- AC5 PASS (live): cold-start-from-killed logged-in -> /vendor/profile 200 -> dashboard, clean; logged-out -> Sign In, clean. _handleDefaultRouting both branches.
- AC1 partial-live: not-logged-in cold start -> Sign In, no crash, clean. Fix adds isLoggedIn() guard (skips profile load when logged out). Full killed-state FCM tap not deliverable to emulator.
- AC2 partial-live: PendingItemScreen opened (loaded profile) -> NO getStoreModuleConfig null-crash. Populated list not shown: zero seeded pending items + pre-existing offset int/String? parse bug (regression).
- AC3 partial-live: food vendor (Burger Palace) + grocery vendor login -> profile loaded -> dashboard, no crash (food & non-food getStoreModuleConfig branches). Order-details push destination not reproduced: no seeded food-store orders + no deep-link.
- REGRESSION (pre-existing, unrelated): offset int-vs-String? in ItemModel.fromJson:32 + PendingItemModel.fromJson:12 -> blanks All Items / Pending Item lists.
- automated: flutter test 116/116 pass; flutter analyze 16 pre-existing lint (0 errors, none in touched files).
