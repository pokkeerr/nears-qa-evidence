# AC6 flutter analyze --no-fatal-infos (pinned SDK)

## tip: store_controller.dart, store_discovery_owner.dart + 6 new test/support files -> 13 issues (all infos)
device_info_plus 12.4.0 (13.3.0 available)
device_info_plus_platform_interface 7.0.3 (8.1.0 available)
package_info_plus 8.3.1 (10.2.2 available)
package_info_plus_platform_interface 3.2.1 (4.1.0 available)
Try `flutter pub outdated` for more information.
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
13 issues found. (ran in 3.1s)

## base: store_controller.dart -> 13 issues (all infos)
device_info_plus 12.4.0 (13.3.0 available)
device_info_plus_platform_interface 7.0.3 (8.1.0 available)
package_info_plus 8.3.1 (10.2.2 available)
package_info_plus_platform_interface 3.2.1 (4.1.0 available)
Try `flutter pub outdated` for more information.
info • An 'async' function should have a 'Future' return type when it doesn't return a value • lib/features/store/controllers/store_controller.dart:478:8 • avoid_void_async
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:634:7 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:883:9 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:937:9 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:971:7 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1018:7 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1191:19 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1210:76 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1222:52 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1231:42 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1299:17 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1385:36 • unawaited_futures
info • Missing an 'await' for the 'Future' computed by this expression • lib/features/store/controllers/store_controller.dart:1446:7 • unawaited_futures
13 issues found. (ran in 3.7s)

Tip: 9 in store_controller.dart (avoid_void_async x1 + unawaited_futures x8) + 4 in store_discovery_owner.dart (the 4 recursion calls that moved, lines 136/248/302/336) + 0 in the 6 new test/support files; base 13 in store_controller.dart. 13 -> 9 + 4, no new issue.
