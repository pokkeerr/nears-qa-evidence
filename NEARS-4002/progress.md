# NEARS-4002 [8] QA - progress / evidence index (worktree tip 3eda9b460, base 9222f9dc8)

Device-free gate walk (all re-measured by QA, scratch exports under the session scratchpad, live tree never mutated):
- lib diff vs base: `git diff 9222f9dc8 --stat -- DeliveryApp/lib packages DeliveryApp/pubspec.yaml` = DeliveryApp/lib/main.dart only, +21/-1; `git diff -w` removes only the foundation show-list import line; ordered await list in main() identical (10 awaits, derived from both trees); no print/debugPrint/AppLogger added. lib touched by two commits only: 3be43ba08 (s4) and 03048fb1e (one-line comment fix).
- Existing suite (58 files, byte-identical at head): base export +542 passed, head export of the 58 files +542 passed, failing-id set empty on both, 0 skipped, 0 load errors; full head suite +1037 passed (542 + 495 new), peak tree RSS 1.54 GB (base) / 1.71 GB (head) under mem-guard 6 GB.
- Goldens: 208 PNG, 14,351,400 B = 13.69 MiB (< 25 MiB guard); golden manifest test 4/4 green (0 missing, 0 extra).
- Determinism: scratch regeneration of chat_golden_compose_test (12 PNG) + order_details_golden_item_heavy_bottom_test (4 PNG), SHA-256 identical 16/16; peak RSS 1.57 / 1.18 GB.
- Mutation spot checks (scratch copy, `diff -r` showed each landed, restored and re-diffed clean): M1 order total uses client sum -> order_details_money_test RED (Expected 25.00 USD / Actual 23.70 USD); M2 getMessages offset>1 replaces -> chat_messages_controller_test RED (Expected <60> / Actual <30>); M3 logout controller-reset order swapped -> session_reset_logout_test RED (ordered timeline mismatch); M4 visual (subtotal label font) -> order_details_golden_item_heavy_bottom_test RED (pixel test failed, 4 cells).
- Fixtures redaction read: baseline_order_fixtures.dart + baseline_feed_fixtures.dart read in full; placeholder names, 000-prefixed phones, no email/URL/token/image URL; secret-pattern scan over all added test/support text files found only example.test hosts and 000 000 000N phones.
- Conversation list deferral (G26): `git diff --name-status 9222f9dc8...HEAD` (286 entries) read in full; no conversation_* file, golden or fixture; ConversationModel import in 2 chat tests + 1 support file is the `Conversation` header object on the MESSAGE page, never ConversationScreen / getConversationList; DC pins (test/features/chat/*) untouched.

Live boot check: see boot-timeline-events.txt, boot-log-scan.log, bug-firebase-absent-unguarded-boot-exceptions.log.
No screenshots and no performance numbers in this evidence set (G42 parked; timeline timestamps deliberately stripped).
