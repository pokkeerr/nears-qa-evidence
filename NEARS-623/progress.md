# NEARS-623 QA progress — voice_search listenOptions deprecation chore

Device: emulator-5556 (Android 17 / API 37). Worktree: /Users/Apple/Projects/nears-wt/NEARS-623
Branch: feat/NEARS-623-voice-listen-options. Backend: local php artisan serve :8000 (zone 2, Abu Dhabi).

- AC1 (analyze clean + search tests green): PASS — conductor-verified; re-ran search suite from worktree = 86/86 green.
- AC2 (builds & launches, no crash): PASS — clean boot splash->home, all config/home APIs 200, zero runtime errors.
- AC3 (voice mic renders+enabled, listen fires cleanly, engages+stops): PASS via live search-screen voice path.
  - Mic = SearchFieldWidget suffix (keyboard_voice_sharp), clickable+enabled.
  - listen() native lifecycle clean x2: onStartListening->onMicrophoneOpened->onStartOfSpeech->onStopListening->NO_SPEECH_DETECTED (expected emulator no-mic). Listening UI "Listening..."/"Volume Level" engaged. No exception/[FAIL]/[ERR].
  - CAVEAT: changed file voice_search_widget.dart is ORPHAN (no import/route/test). Live mic uses search_controller.dart listen (already listenOptions) — functionally identical API shape. Demonstrated equivalent path.
- AC4 (search idle + typed query): PASS — idle (Your Last Search + Popular Categories) renders; "milk" -> Items(13), /search/unified 200, search analytics fired PII-safe. Zero errors.

Verdict: PASS. No task_bugs. Followups: orphan widget (code hygiene), stale payment-parse WARN from prior sessions.
