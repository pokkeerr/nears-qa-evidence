# NEARS-870 QA progress (DeliveryApp SmartManagement.onlyBuilder)
device: emulator-5554 (debug build), user: Ali Hassan (dm id=1, +971565656656)
backend: local Admin @ 10.0.2.2:8000 (config 200 OK)

- AC1: Get.smartManagement = SmartManagement.onlyBuilder @ get_di.dart:84 (first line of init) — PRESENT
- AC2: smartManagement: SmartManagement.onlyBuilder @ main.dart:209 (GetMaterialApp) — PRESENT, mirrors UserApp
- AC3: debug build launched cleanly, Dart VM Service up — PASS
- AC4: fresh login (phone+pw) -> home dashboard renders normally — PASS
- AC5: Logout (Get.offAllNamed signIn teardown) -> clean sign-in -> re-login -> working home — PASS
- AC6: 401 teardown branch (api_checker.dart:29-35) — code-identical to demonstrated Logout teardown
       (same Get.find<AuthController>.clearSharedData + Get.find<ProfileController>.stopLocationRecord
       + Get.offAllNamed(signIn) on the same GLOBAL route-independent singletons). Genuine network-401
       not fired: requires forbidden DB token-revoke (read-only rule) or breaking GCM secure-storage.
       Storage-tamper attempt threw at startup (main.dart:124), a different path — restored. MET-by-equivalence.
- AC7: post-teardown sweep — Home, Orders list, Order details #166, Profile, Chat/Conversation,
       My Earning, My Account/cash-in-hand, back-nav stress -> all render, ZERO grey/blank/red/not-found — PASS

logs: clean across all live ACs (only GMS/OS noise). One pre-existing background race: update-fcm-token
POST 403 during logout — PROPERLY logged ([FAIL] + ApiFailure sentinel + correlation_id), not silent, unrelated.

automated: flutter test -> All 202 tests passed.
