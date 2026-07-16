# NEARS-802 QA progress (fix-cycle 1, express lane) — PASS

Device: emulator-5556 (reclaimed stale NEARS-1137/pid73104-dead lock)
Worktree: /Users/Apple/Projects/nears-NEARS-802-chat-fcm-null-guard (feat/NEARS-802-chat-fcm-null-guard)
Build: Android debug, baseUrl http://10.0.2.2:8000 (real local backend, config 200)

## Automated backstop (authoritative for AC1/AC2/AC4 race logic)
- targeted `flutter test test/notification_chat_null_guard_test.dart` -> 6/6 PASS
  (mutation-verified pin on shipped `NotificationHelper.shouldRefreshOpenChat`)
- full VendorApp `flutter test` -> All tests passed (131 tests, 0 failures)
- `flutter analyze` changed files -> No issues found

## AC4 (both branches) — code-confirmed
notification_helper.dart calls shouldRefreshOpenChat on BOTH FCM listener branches:
- line 97: rental TaxiChatController (null-safe messageModel?.conversation?.id)
- line 116: store ChatController (null-safe messageModel?.conversation?.id)
Null loaded id -> false -> existing `else { showNotification(...) }` fallback.

## Live smoke (AC3 happy-path + no-crash-on-chat-entry) — emulator-5556
- VendorApp booted, logged in as store owner, Dashboard renders (Arabic/RTL), no crash
- Menu -> Conversation: GET /api/v1/vendor/message/list -> 200 (getConversationList)
- Opened "Customer Nears" conversation: GET /api/v1/vendor/message/details -> 200
  (getMessages -> populates messageModel.conversation.id) -> message bubble renders
- ui_errors clean; no [FAIL]/[ERR]/EXCEPTION/TypeError across the whole session

## Live mid-load FCM race
NOT hand-reproducible (static FirebaseMessaging.onMessage closure; sub-second
firstLoad race). Per spawn contract, the mutation-verified unit pin is the accepted
evidence for AC1/AC2/AC4. No fabricated push.

## ENV note (NOT a NEARS-802 defect)
Fresh worktree lacked android/app/google-services.json (gitignored) -> app red-screened
at boot with `[core/no-app] No Firebase App '[DEFAULT]'`. Resolved for QA by copying the
gitignored Firebase config from the primary tree (stays gitignored, never committed).
Worktree-bootstrap gap -> followup (mirror the image-bootstrap for google-services.json).

VERDICT: PASS
