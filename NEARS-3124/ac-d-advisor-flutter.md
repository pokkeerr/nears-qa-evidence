# AC (d) spot-check — advisor-flutter.md (189 lines, H2 set = template) — 3 rules + 1 claim check

## Rule 1 — GetX SmartManagement.onlyBuilder
**Brief (## Rules and standards, "Layering and wiring", bullet 2):**
> All three apps use GetX (`get: ^4.7.3`) exclusively; every controller is registered in `get_di.dart`. UserApp and DeliveryApp set `Get.smartManagement = SmartManagement.onlyBuilder` as the first statement of `di.init()`, mirrored on `GetMaterialApp` — the default `full` disposes globally-registered singletons on route teardown, causing blank/red screens. (nears-reference.md §16, NEARS-870)

**Source nears-reference.md:558 (§16):**
> All three apps use **GetX** (`get: ^4.7.3`) exclusively. Pattern: `Controller → Service → Repository → ApiClient`. All controllers are registered in `get_di.dart`. UserApp and DeliveryApp (NEARS-870) both set `Get.smartManagement = SmartManagement.onlyBuilder` (first statement of `di.init()` + mirrored on `GetMaterialApp`) — the default `full` disposes globally-registered singletons on route teardown, causing blank/red screens; why → Confluence page 20774915.

Verdict: traceable — near-verbatim.

## Rule 2 — paired AppLogger.failure for every generic error toast
**Brief (## Rules and standards, "Logging", bullet 3):**
> Every generic error toast/error state needs a paired `AppLogger.failure(...)`; a silent toast is a violation. (CLAUDE.md §Conventions; docs/platform/logging-contract.md)

**Source CLAUDE.md:103:**
> - **Logging:** every generic error toast/error state needs a paired `AppLogger.failure(...)` — a silent toast is a violation; full rule → `docs/platform/logging-contract.md`.

Verdict: traceable — verbatim.

## Rule 3 — Known trap `stale-async-writeback-seals-new-session`
**Brief (## Known traps, bullet 6):**
> **stale-async-writeback-seals-new-session** (high, NEARS-1109) — any error/seal/retry flag written AFTER an await is epoch-guarded against the session it started in; drop the ENTIRE write-back (flag + retry closure + spinner) on mismatch; the epoch is keyed to the LIST it protects (NEARS-1840).

**Source docs/workflow/review-lessons.json:** status=active · severity=high · first_seen=NEARS-1109
> rule: Any error/seal/retry flag written AFTER an await must be epoch-guarded against the session it started in. … on the continuation, drop the ENTIRE write-back (flag + retry closure + spinner) when it no longer matches.

Verdict: traceable — the two operative sentences are reproduced; severity + origin match.

## Claim check — brief asserts CLAUDE.md's Crashlytics line is stale
**Brief (## Rules and standards, "Logging", bullet 8):** "Crashlytics is wired (NEARS-296) and debug-no-op … CLAUDE.md's \"`firebase_crashlytics` is disabled in UserApp\" is the stale statement — `UserApp/pubspec.yaml` carries `firebase_crashlytics: ^5.2.3`."
- UserApp/pubspec.yaml:26 → `firebase_crashlytics: ^5.2.3` (OBSERVED)
- CLAUDE.md:100 → "`firebase_crashlytics` is disabled in UserApp." (OBSERVED — the stale line the brief names)
- profile grep NEARS-296: 72:## Logging & observability — MANDATORY (NEARS-415 / NEARS-296 / NEARS-267)
78:- **Crashlytics is debug-no-op** (collection `!kDebugMode`, wired NEARS-296); release upload deferred — verify via the `[FAIL]` console line + the unit seam.

Verdict: the brief's claim is correct against the tree; CLAUDE.md:100 is the stale statement (pre-existing doc drift, not this ticket's defect → followups[]).

Never-do list: all four mandatory items present (see ac-d-structural.txt).
