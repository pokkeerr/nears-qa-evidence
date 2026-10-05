# AC6 analyze (flutter analyze --no-fatal-infos, pinned SDK by absolute path)
## tip: lib/features/store/controllers + 3 new tests + stage-A characterization + store_catalog_support
Analyzing 6 items...                                            

   info • An 'async' function should have a 'Future' return type when it doesn't return a value • lib/features/store/controllers/store_controller.dart:437:8 • avoid_void_async
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:742:7 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:915:19 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:934:76 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:946:52 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:955:42 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1023:17 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1109:36 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1170:7 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:136:7 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:248:9 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:302:9 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:336:7 • unawaited_futures

13 issues found. (ran in 3.7s)
mem-guard[s5qa-an]: done rc=0 peak_tree_rss=0.66 GB (cap 6.0)

## base: lib/features/store/controllers (qabase worktree)
Analyzing controllers...                                        

   info • An 'async' function should have a 'Future' return type when it doesn't return a value • lib/features/store/controllers/store_controller.dart:465:8 • avoid_void_async
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:770:7 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:943:19 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:962:76 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:974:52 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:983:42 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1051:17 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1137:36 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1198:7 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:136:7 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:248:9 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:302:9 • unawaited_futures
   info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_discovery_owner.dart:336:7 • unawaited_futures

13 issues found. (ran in 4.2s)
mem-guard[s5qa-an]: done rc=0 peak_tree_rss=0.81 GB (cap 6.0)

RESULT: 13 infos at tip (store_controller 9 + store_discovery_owner 4 + store_catalog_owner 0 + 0 in the new/stage-A tests) == 13 infos at base (same 9 + 4, line numbers shifted only). 0 errors, 0 warnings.
golden_manifest_check_test +5 rc=0, golden/baseline_home_golden_test +15 rc=0 (nets rows 23, 45); git status of the tested worktree clean after all runs (no golden regenerated); git diff --name-only base..tested | grep -ciE 'golden|png' = 0
