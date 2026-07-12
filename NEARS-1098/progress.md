# NEARS-1098 — QA fix-cycle 3 (delta re-QA), emulator-5554

Harness: transparent pass-through proxy on :8001 -> local backend :8000, with an
injectable 500 on `/api/v1/stores/details/<slug|id>` (store 59 / nears-257-fixture-store).
No DB write, no product-code change. App built with --dart-define=API_HOST=10.0.2.2:8001.
Store details are fetched by SLUG when the deep link carries one (store_repository.dart:232).

## PRE-FIX CONTROL (HEAD c90d7d74, delta reverted) — light mode, English/LTR
- Cold deep-link into a failing store -> failure surface renders
  ("This store could not be loaded" / Retry / Back).
- "Back to Home" link: **NOT FOUND** (never mounted) -> bug-ac5-prefix-01-failure-no-home-link.png
- Tap Back -> a11y tree = **0 nodes**, com.izzes.nears/.MainActivity still topResumedActivity
  = blank dead splash. DEAD-END REPRODUCED -> bug-ac5-prefix-02-dead-splash-after-back.png

## FIXED BUILD (cycle-3 delta re-applied) — light mode, emulator-5554
| AC | Result | Evidence |
|---|---|---|
| AC1 error state, not shimmer | PASS | ac1-error-state-not-shimmer.png |
| AC2 no duplicate toast | REUSED (cycle-2 PASS; toast path byte-untouched) | prior gallery |
| AC3 failure audible | PASS (re-observed) | `[FAIL] endpoint=/api/v1/stores/details/ http_status=500 type=ApiFailure` — endpoint PATH only |
| AC4 retry recovers | PASS | disarmed injected 500 -> Retry -> store content loaded (ac4-retry-recovers-store-loaded.png) |
| AC5a cold deep-link LTR (2/2) | PASS | back -> live Home 34 nodes (pre-fix: 0 nodes) — ac5a-01/02 |
| AC5b cold deep-link RTL/AR | PASS | AR link "العودة للرئيسية"; back -> live Home 33 nodes; NO false "no internet" — ac5b-01/02 |
| AC5c anti-over-correction | PASS | pushed from search list: link ABSENT, back popped to the LIST — ac5c-01/02 |
| AC5d hardware back (PopScope) | PASS | from list -> list; cold deep-link -> live Home — ac5d-01/02 |
| AC5 auto-opened fast path | escape PASS / link ABSENT (pre-existing) | back -> live Home (not stranded); link cannot mount because `autoOpened` is nullified by Get.arguments precedence — bug-autoopened-flag-dead-on-hero-path.{png,log} |

Automated: `flutter test` 2255/2255 PASS.
Mutation-check: reverting ONLY the widget to the pre-fix line turns the new pin RED
(`Expected: true / Actual: <false>`) => the unit pin is falsifiable, not green-but-blind.
Regression: healthy store (deep-link + list push) opens and backs out unchanged; logs clean.
