# NEARS-3541 QA progress
- Device: emulator-5556 (locked, NEARS-3541)
- Backend: local php artisan serve :8000, queue:work running
- Fresh-worktree gap: android/app/google-services.json absent (gitignored) -> copied from primary tree per NEARS-3534 known pattern (this is an environment bootstrap step, not a code change)
- open_ai_status = 0 on this backend -> AI-generator FAB (add_item_screen.dart) NOT reachable in this test env

## AC1 - PASS (3 of 4 tooltips demonstrated live; 4th confirmed unreachable in this env)
- Dashboard Store FAB: content-desc="Store" in a11y tree; visual long-press popup "Store" screenshot ac1-dashboard-store-fab-tooltip.png. Regression: tap -> Store tab (My Shop). PASS.
- Store screen (My Shop) add-item FAB: content-desc="Add Item"; visual popup ac1-storescreen-additem-fab-tooltip.png. Regression: tap -> Add Item screen. PASS.
- All Items screen add-item FAB: content-desc="Add Item"; visual popup ac1-allitems-additem-fab-tooltip.png. Regression: tap -> Add Item screen. PASS.
- Add/Edit Item AI-generator FAB: open_ai_status=0 via GET /api/v1/config on this backend -> configModel.openAiStatus false -> FAB not rendered. Confirmed absent from a11y dump (ac1-add-item-screen-ai-fab-absent-dump.xml), positive-control node in same dump = content-desc="Add Item" (the add-item screen's own top-level Button, proving the a11y instrument was live, not empty). UNVERIFIABLE-BUT-EXPECTED (flag not on) -- not a defect.

## AC2 - FAIL (reproduced, real defect, filed as task_bug for engineer)
Reproduced live TWICE on the exact profile-save -> back-navigation path, from BOTH required
starting Dashboard tab states (Home tab active, Store tab active). FlutterError:
"There are multiple heroes that share the same tag within a subtree." Colliding tag:
"<default FloatingActionButton tag>" (Flutter's own sentinel for FABs with no explicit
heroTag) -- this is a DIFFERENT collision than the already-flagged regression-candidate
(store_screen.dart/all_items_screen.dart literal 'nothing' tag), so this is filed as a NEW
AC2 task-bug, not a confirmation of the existing regression-candidate. See
bug-ac2-hero-collision-default-fab-tag.log for full assertion text + both repro timestamps.
App does not visibly crash (no red screen in debug); "Profile updated successfully" shows and
navigation completes, but a real uncaught FlutterError fires each time -- Hero collisions are
not gated by kDebugMode/assert, so this would also throw in profile/release builds.
Test-account cleanup: ahmed.khan@demo.com last name reverted to "Khan" after testing; phone
was originally blank (no phone on file) and could not be restored to blank (Phone is a
required field for Update to succeed) -- left as +971 509991234, noting this as a data
hygiene side-effect of the investigation, not a code defect.

## Regression sweep (bounded) - clean
Dashboard Home/Orders/Wallet tabs, Store screen, All Items screen, Add Item screen: no new
[ERR]/[FAIL] beyond the AC2 finding above (ui_errors confirms only the 9 AC2-related lines
match across the whole session). All 3 demonstrable FAB taps still navigate correctly
(regression pass).

## Automated backstop
flutter test test/features/dashboard/fab_a11y_tooltip_test.dart -> 8/8 passed.
