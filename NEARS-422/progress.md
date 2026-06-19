# NEARS-422 DELTA re-QA progress (fix-cycle 1)
Device: emulator-5554 | Branch feat/NEARS-422-item-detail-modal @ 0e8fc4788 | backend http://10.0.2.2:8000 (UP)
Automated backstop: 5/5 PASS (item_detail_modal_nav_test + item_bottom_sheet_initstate_guard_test)

## Test data
- Module1 grocery z1: item 1 (Sample Product) / 97 (Rice 5kg) store 1 (demo-store)
- Module2 food z1: item 16 (Classic Cheeseburger) store 4 (burger-palace)
- Module3 pharmacy z2: item 598 (Multivitamin Daily) store 53 (careplus-pharmacy-abu-dhabi)
- Invalid id: 9999999 (max item id = 61534)

## Live verdicts (appended as observed)

### [1] AC4 not-on-store — PASS
Grocery module home (non-store) -> tapped "Seedless Grapes" card -> sheet opened over module home (store-name "Abu Dhabi Fresh Market" visible). Tapped store name. t+1s: sheet dismissed, store-profile shown. t+4s: STILL on store-profile (header "Abu Dhabi Fresh Market", addr "Al Wahda Mall, Abu Dhabi", category tabs) — STUCK, no bounce to home. No runtime errors.
shots: ac4-sheet-nonstore-entry.png, ac4-store-profile-stuck.png

### [6] Back-stack check (post AC4) — PASS
From stuck store-profile, 1x system-back -> landed on module grid home (multi-store item grid), NOT a stray duplicate store-profile. offNamed replaced the orphan entry cleanly.

### [2] AC4 on-store regression — PASS
Entered store-profile (Abu Dhabi Fresh Market) -> opened in-store sheet ("Breakfast Cereal") -> tapped store name in sheet. Sheet dismissed, STAYED on same store page (header+category tabs intact), no extra/duplicate nav. 1x back -> module grid home (no duplicate store entry). No runtime errors.
shots: ac4-sheet-instore-entry.png, ac4-instore-stayed.png

### [3] AC5 same-module deep-link — PASS
App in Grocery(module1)/zone2. Fired https://6ammart-web.6amtech.com/item-details/almond-milk-1l-8?id=151&page=item&module=grocery via am start -n com.izzes.nears/.MainActivity. Item RESOLVED -> sheet "Almond Milk 1L" opened over store backdrop (Abu Dhabi Fresh Market). Dismissed -> landed on STORE-PROFILE (header+addr+category tabs), NOT home-no-sheet. No runtime errors.
shots: ac5-samemodule-sheet-over-store.png, ac5-samemodule-dismiss-store.png

### [4] AC5 cross-module deep-link — FAIL
App in Grocery(module1)/zone2. Fired cross-module deep link to pharmacy(module3) item 598 (module=pharmacy in query, confirmed delivered intact via logcat). API returned [404] /api/v1/items/details/598 -> item NOT resolved -> fail-safe snackbar, nothing pushed, stayed on prior grocery store. Backend proof: item 598 resolves 200 with moduleId:3, 404 with moduleId:1. Root cause: openItemDeepLink does int.tryParse(moduleId) but module param is a NAME ("pharmacy") -> null -> set-module-before-fetch SKIPPED -> fetch hits stale grocery module. THIS IS THE EXACT AC5 FIX TARGET; FIX INEFFECTIVE for real (name-carrying) deep links.
shots: bug-crossmodule-404.png  log: bug-crossmodule-404.log

### [5] AC6 fail-safe (invalid id) — PASS
Fired deep link id=9999999 (max item id 61534). API [404] -> brief "Not Found" snackbar shown, NOTHING pushed (no orphan store-profile, no sheet); underlying prior store-profile unchanged. No runtime errors. Cross-module 404 also exercised the same fail-safe correctly.
shot: ac6-invalid-snackbar.png
