# AC4 spot-check: 18 own mutants, scratch copy (rsync of UserApp+packages, own .dart_tool; the live worktree never touched: git status clean), landed by diff -U0 (diffs below), restored by cp from the live file and cmp (restored_cmp=true every row), tests per mutant in order owner_test (46) -> facade_wiring_test (30) -> characterization (92) -> scan_test, stopping at the first RED

| id | target | what | hunk | killed by |
|---|---|---|---|---|
| M01 | store_catalog_owner.dart | browse request: rating -1 sentinel no longer mapped to null (arg list) | @@ -163 +163 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M02 | store_catalog_owner.dart | browse request: lowerValue reads upper (arg swap) | @@ -164 +164 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M03 | store_catalog_owner.dart | getStoreItemList page-1 reset no longer bumps the session id | @@ -142 +141,0 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M04 | store_catalog_owner.dart | initSearchData no longer bumps the session id | @@ -321 +320,0 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M05 | store_catalog_owner.dart | setCategoryIndex: offers-selection clear moved AFTER the loader call (order) | @@ -348 +347,0 @@ @@ -355,0 +355 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M06 | store_catalog_owner.dart | retry closure re-fires with notify=false | @@ -143 +143 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M07 | store_catalog_owner.dart | retry closure captures the live offset instead of 1 | @@ -143 +143 @@ | store_catalog_family_characterization_baseline_test.dart (KILLED, restored cmp=True) |
| M08 | store_catalog_owner.dart | stale page-2 guard inverted | @@ -170 +170 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M09 | store_catalog_owner.dart | search failure path loses the superseded-request session guard | @@ -297 +297 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M10 | store_controller.dart | _StoreCatalogPort.notify bridge becomes a no-op (last class in file) | @@ -2035 +2035 @@ | store_catalog_facade_wiring_test.dart (KILLED, restored cmp=True) |
| M11 | store_controller.dart | port: registeredStoreType reads this controller instead of the registered one | @@ -2021 +2021 @@ | store_catalog_facade_wiring_test.dart (KILLED, restored cmp=True) |
| M12 | store_controller.dart | grid port (offers family): session id write no longer reaches the catalog owner | @@ -1975 +1975 @@ | store_catalog_facade_wiring_test.dart (KILLED, restored cmp=True) |
| M13 | store_controller.dart | grid port: offers page-2 dedupe/partition forward dropped | @@ -1980,2 +1980 @@ | store_catalog_facade_wiring_test.dart (KILLED, restored cmp=True) |
| M14 | store_controller.dart | getStoreDetails no longer resets the grid-failed flag on a new store | @@ -844 +843,0 @@ | store_catalog_facade_wiring_test.dart (KILLED, restored cmp=True) |
| M15 | store_controller.dart | grid port (offers family): retry slot write no longer reaches the catalog owner | @@ -1978 +1978 @@ | store_catalog_facade_wiring_test.dart (KILLED, restored cmp=True) |
| M16 | store_catalog_owner.dart | getStoreItemList: page>1 with a null model no longer takes the reset branch | @@ -138 +138 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M17 | store_catalog_owner.dart | empty-query search returns false instead of true | @@ -259 +259 @@ | store_catalog_owner_test.dart (KILLED, restored cmp=True) |
| M18 | store_controller.dart | facade setCategoryIndex drops the itemSearching argument | @@ -1215 +1215 @@ | store_catalog_facade_wiring_test.dart (KILLED, restored cmp=True) |

Verdicts: 18 KILLED, 0 survived, 0 equivalent. Every RED is an assertion failure (Expected/Actual blocks in the per-mutant logs), none a compile failure. Areas: arg lists (M01 M02), session bumps (M03 M04), notify/order (M05 M10), retry arming (M06 M07), stale guards (M08 M09 M16), empty-query return (M17), port bridge (M10 M11), grid re-bind forwards to the offers family (M12 M13 M15), getStoreDetails reset (M14), facade delegate arg (M18).

## landed diffs (diff -U0)
### M01
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -163 +163 @@
-      rating: _rating == -1 ? null : _rating,
+      rating: _rating,
### M02
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -164 +164 @@
-      lowerValue: _lowerValue == 0 ? null : _lowerValue,
+      lowerValue: _upperValue == 0 ? null : _upperValue,
### M03
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -142 +141,0 @@
-      _itemListSessionId++; // NEARS-1109
### M04
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -321 +320,0 @@
-    _itemListSessionId++; // NEARS-1109
### M05
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -348 +347,0 @@
-    _port.clearOffersSelection();
@@ -355,0 +355 @@
+    _port.clearOffersSelection();
### M06
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -143 +143 @@
-      _retryLastGridLoad = () => getStoreItemList(storeID, 1, type, true);
+      _retryLastGridLoad = () => getStoreItemList(storeID, 1, type, false);
### M07
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -143 +143 @@
-      _retryLastGridLoad = () => getStoreItemList(storeID, 1, type, true);
+      _retryLastGridLoad = () => getStoreItemList(storeID, offset, type, true);
### M08
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -170 +170 @@
-    if (offset > 1 && requestSessionId != _itemListSessionId) {
+    if (offset > 1 && requestSessionId == _itemListSessionId) {
### M09
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -297 +297 @@
-      } else if (offset == 1 && requestSessionId == _itemListSessionId) {
+      } else if (offset == 1) {
### M10
--- live/lib/features/store/controllers/store_controller.dart
+++ mut/lib/features/store/controllers/store_controller.dart
@@ -2035 +2035 @@
-  void notify() => _controller.update();
+  void notify() {}
### M11
--- live/lib/features/store/controllers/store_controller.dart
+++ mut/lib/features/store/controllers/store_controller.dart
@@ -2021 +2021 @@
-  String get registeredStoreType => Get.find<StoreController>().type;
+  String get registeredStoreType => _controller.type;
### M12
--- live/lib/features/store/controllers/store_controller.dart
+++ mut/lib/features/store/controllers/store_controller.dart
@@ -1975 +1975 @@
-      _controller._catalog.itemListSessionId = value;
+      value;
### M13
--- live/lib/features/store/controllers/store_controller.dart
+++ mut/lib/features/store/controllers/store_controller.dart
@@ -1980,2 +1980 @@
-  void dedupeAndPartitionStoreItems() =>
-      _controller._catalog.dedupeAndPartitionStoreItems();
+  void dedupeAndPartitionStoreItems() => null;
### M14
--- live/lib/features/store/controllers/store_controller.dart
+++ mut/lib/features/store/controllers/store_controller.dart
@@ -844 +843,0 @@
-    _catalog.resetItemsFailed(); // NEARS-1088: never carry a grid error into a new store
### M15
--- live/lib/features/store/controllers/store_controller.dart
+++ mut/lib/features/store/controllers/store_controller.dart
@@ -1978 +1978 @@
-      _controller._catalog.setRetryLastGridLoad(value);
+      value;
### M16
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -138 +138 @@
-    if (offset == 1 || _storeItemModel == null) {
+    if (offset == 1) {
### M17
--- live/lib/features/store/controllers/store_catalog_owner.dart
+++ mut/lib/features/store/controllers/store_catalog_owner.dart
@@ -259 +259 @@
-      return true;
+      return false;
### M18
--- live/lib/features/store/controllers/store_controller.dart
+++ mut/lib/features/store/controllers/store_controller.dart
@@ -1215 +1215 @@
-      _catalog.setCategoryIndex(index, itemSearching: itemSearching);
+      _catalog.setCategoryIndex(index);
