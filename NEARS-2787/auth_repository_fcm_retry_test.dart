// NEARS-2787 — saveDeviceToken() retry/backoff + log-gating pins.
//
// Two behaviors under test, both in the same function
// (auth_repository.dart `saveDeviceToken()`):
//  1. getToken() failing transiently (the documented cold-launch Play
//     Services race) must retry with bounded backoff and log [FAIL] exactly
//     ONCE, after retries are exhausted — never once per attempt.
//  2. Regression pin for the pre-existing bug: the trailing null-check
//     gating the [INFO] "obtained" log checked a variable that was never
//     left null even on total failure, so [INFO] could fire after a [FAIL]
//     for the SAME fetch. Success logs INFO only; total failure logs FAIL
//     only — never both for one saveDeviceToken() call.
//
// getToken() is scripted via a mutable FirebaseMessagingPlatform stub
// (mirrors test/helpers/firebase_mocks.dart's approach) rather than that
// shared helper directly, because the shared stub hardcodes a single
// always-succeeding token and these pins need per-test failure/success
// sequences.
// ignore_for_file: depend_on_referenced_packages
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_core_platform_interface/firebase_core_platform_interface.dart';
import 'package:firebase_messaging_platform_interface/firebase_messaging_platform_interface.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sixam_mart/api/api_client.dart';
import 'package:sixam_mart/features/auth/domain/repositories/auth_repository.dart';
import 'package:sixam_mart/helper/app_logger.dart';

class _StubFirebaseApp extends FirebaseAppPlatform {
  _StubFirebaseApp()
    : super(
        defaultFirebaseAppName,
        const FirebaseOptions(
          apiKey: 'test',
          appId: 'test',
          messagingSenderId: 'test',
          projectId: 'test',
        ),
      );
}

class _StubFirebasePlatform extends Mock
    with MockPlatformInterfaceMixin
    implements FirebasePlatform {
  @override
  FirebaseAppPlatform app([String name = defaultFirebaseAppName]) =>
      _StubFirebaseApp();
}

const String _throwMarker = '__throw__';

/// getToken() outcomes are consumed in FIFO order per test; a queue drained
/// past its scripted outcomes means the test under-scripted attempts.
class _ScriptedMessagingPlatform extends Mock
    with MockPlatformInterfaceMixin
    implements FirebaseMessagingPlatform {
  final List<String?> script = [];

  @override
  FirebaseMessagingPlatform delegateFor({required FirebaseApp app}) => this;

  @override
  FirebaseMessagingPlatform setInitialValues({bool? isAutoInitEnabled}) =>
      this;

  @override
  Future<String?> getToken({
    String? vapidKey,
    String? serviceWorkerScriptPath,
  }) async {
    final String? next = script.removeAt(0);
    if (next == _throwMarker) {
      throw Exception('transient getToken failure');
    }
    return next;
  }
}

class _FakeRecorder implements CrashRecorder {
  int recordCount = 0;

  @override
  void setCustomKey(String key, Object value) {}

  @override
  void recordError(
    Object error,
    StackTrace? stack, {
    String? reason,
    bool fatal = false,
  }) {
    recordCount++;
  }
}

/// Async counterpart of app_logger_test.dart's `_capturePrints` — this
/// suite's body awaits real (zero-delay-scripted) retry backoff.
Future<List<String>> _capturePrints(Future<void> Function() body) async {
  final lines = <String>[];
  final DebugPrintCallback original = debugPrint;
  debugPrint = (String? message, {int? wrapWidth}) {
    if (message != null) lines.add(message);
  };
  try {
    await body();
  } finally {
    debugPrint = original;
  }
  return lines;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late _ScriptedMessagingPlatform messaging;
  late _FakeRecorder recorder;
  late AuthRepository repo;

  setUpAll(() {
    // FirebaseMessaging.instance/_delegate is a process-wide singleton cache
    // (see firebase_messaging's FirebaseMessaging._firebaseMessagingInstances)
    // resolved on first use, so the platform stub is installed once here and
    // its outcome QUEUE is reset per-test below rather than swapping the
    // platform instance itself.
    FirebasePlatform.instance = _StubFirebasePlatform();
    messaging = _ScriptedMessagingPlatform();
    FirebaseMessagingPlatform.instance = messaging;
  });

  setUp(() async {
    SharedPreferences.setMockInitialValues(<String, Object>{});
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final ApiClient apiClient = ApiClient(
      appBaseUrl: 'https://example.test',
      sharedPreferences: prefs,
    );
    repo = AuthRepository(sharedPreferences: prefs, apiClient: apiClient);
    messaging.script.clear();
    recorder = _FakeRecorder();
    AppLogger.recorder = recorder;
    AuthRepository.fcmTokenRetryDelays = const [Duration.zero, Duration.zero];
  });

  tearDown(() {
    AppLogger.resetRecorder();
  });

  test('AC1: cold-launch success logs INFO once, no FAIL line', () async {
    messaging.script.addAll(['fresh-token']);

    String? result;
    final List<String> lines = await _capturePrints(() async {
      result = await repo.saveDeviceToken();
    });

    expect(result, 'fresh-token');
    expect(
      lines
          .where(
            (l) =>
                l.contains('[INFO]') &&
                l.contains('FCM registration id obtained'),
          )
          .length,
      1,
    );
    expect(lines.any((l) => l.contains('[FAIL]')), isFalse);
    expect(recorder.recordCount, 0);
  });

  test(
    'transient failures retry then succeed: exactly one INFO, no FAIL line',
    () async {
      messaging.script.addAll([_throwMarker, _throwMarker, 'token-after-retries']);

      String? result;
      final List<String> lines = await _capturePrints(() async {
        result = await repo.saveDeviceToken();
      });

      expect(result, 'token-after-retries');
      expect(lines.where((l) => l.contains('[INFO]')).length, 1);
      expect(lines.any((l) => l.contains('[FAIL]')), isFalse);
      expect(recorder.recordCount, 0);
    },
  );

  test(
    'AC2: total failure after retries exhausted — one FAIL (not one per '
    'attempt), sentinel returned, boot not blocked indefinitely',
    () async {
      messaging.script.addAll([_throwMarker, _throwMarker, _throwMarker]);

      String? result;
      final List<String> lines = await _capturePrints(() async {
        result = await repo.saveDeviceToken();
      });

      // '@' sentinel contract: verification_repository.dart:22 force-unwraps
      // this on total failure — must never become null.
      expect(result, '@');
      expect(
        lines
            .where(
              (l) =>
                  l.contains('[FAIL]') &&
                  l.contains('FCM registration id fetch failed'),
            )
            .length,
        1,
      );
      // Regression pin: the old vacuous always-true null-check could still
      // fire [INFO] after a [FAIL] for the same fetch — must not happen now.
      expect(lines.any((l) => l.contains('[INFO]')), isFalse);
      expect(recorder.recordCount, 1);
    },
  );
}
