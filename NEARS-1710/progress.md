# NEARS-1710 QA progress (cycle 4) — DeliveryApp policy/HTML viewer states

Device: emulator-5560 (sdk_gphone16k_arm64), Android, **light mode only** (dark deferred).
Build: worktree /Users/Apple/Projects/nears-NEARS-1710-deliveryapp-html-viewer-states @ 0f5958d0 (clean).
Logged in: Ali Hassan (delivery_man). Verdict: PASS.

## Two backends used
1. **Real dev backend** `http://10.0.2.2:8000` (default Android baseUrl) — returns HTTP 200
   with a 2-byte blank body on both policy endpoints, which drives the empty branch naturally.
2. **QA proxy** on `http://10.0.2.2:8099` (app relaunched with `--dart-define=BASE_URL=`, the
   supported seam in app_constants.dart). Transparent pass-through to :8000, with the two
   policy endpoints switchable to content / blank / HTTP 500 / 6s-delayed. **No DB mutation.**
   Needed for the states the real backend cannot produce (content, non-200, observable skeleton).

## Per QA-scope point

1. **4 states, both routes — PASS.**
   - skeleton: 6s-delayed 200; a11y tree = app-bar title only (11 nodes), shimmer bars present.
     `ac1-terms-skeleton-loading.png`
   - error+retry: HTTP 500 and airplane-mode, both routes. `ac2-terms-http500-error-retry.png`,
     `ac1-terms-error-retry-state.png`
   - empty: real backend blank 200, both routes. `ac1-terms-empty-state.png`,
     `ac1-privacy-empty-state.png`
   - content: proxy HTML; h1 + both paragraphs render. `ac1-terms-content-state.png`
2. **No permanent spinner — PASS.** HTTP 500 held error+Retry at T+3s and T+11s; offline held it
   at T+1s and T+7s. Never a spinner. The `CircularProgressIndicator()` line is deleted from
   the source (it is one of only 3 removed lines in the screen diff).
3. **Retry re-fetches — PASS.** Offline retry emitted a NEW GET with a NEW correlation_id
   (f1c5fe73 != 60403ab9). Retry after restoring the network: `http_status=200`, error cleared,
   state advanced. Retry from HTTP 500 into a delayed 200: content rendered.
   (See finding below — the retry paints no in-flight state; non-AC-breaking.)
4. **Single-controller stale flash — PASS, both directions.** Distinct per-route markers used.
   Terms(content) -> Privacy: skeleton only, zero TERMS-CONTENT-MARKER (`ac4-switch-no-stale-flash.png`).
   Privacy(error) -> Terms: skeleton only, no stale error.
5. **Exactly one [FAIL] per failed fetch — PASS.** Whole-session tally: 3 induced 500s -> 3 [FAIL]s,
   2 induced offline fetches -> 2 [FAIL]s, each with a unique correlation_id. No double-log.
   HTTP path carries status: `[FAIL] endpoint=/api/v1/terms-and-conditions http_status=500
   type=ApiFailure msg="unhandled api response" correlation_id=e3765a59-...`.
   **Correlation join proven end-to-end:** the proxy's captured wire header
   `x-request-id: e3765a59-bbcc-428e-9d05-f04feb5fbf19` is byte-identical to the id in the [FAIL].
6. **Empty vs error distinguishable — PASS (visual + structural).** Empty = document icon in a
   tinted disc + "This page isn't available yet.", NO button (12 a11y nodes). Error = cloud-off
   icon + "Couldn't connect to the server. Please try again." + green Retry (13 nodes).
7. **`policy_content_unavailable` in en/ar/bn/es — PASS, all four live.**
   en "This page isn't available yet." · ar "هذه الصفحة غير متوفرة بعد" ·
   bn "এই পৃষ্ঠা এখনও উপলব্ধ নয়" · es "Esta página no está disponible aún". No raw key anywhere.
8. **Happy path unchanged / no token swap — PASS.** The screen diff removes only 3 lines (the
   spinner ternary); `HtmlWidget` keeps its default textStyle and `onTapUrl`. Content renders
   bold h1 + body paragraphs. NEARS-413 BR-1 boundary respected, not flagged.
9. **RTL — PASS, verified by pixel not by eye.** Arabic skeleton vs English skeleton:
   160dp header bar LTR x=79..558 (left_inset 39, right_inset 747) mirrors to RTL x=784..1263
   (left_inset 744, right_inset 42); 180dp closing bar 39/687 -> 684/42; full-width lines identical.
   Widths preserved exactly (479px / 539px in both). `ac9-terms-skeleton-arabic-rtl.png`.
   Arabic empty state also correct (`ac7-ac9-terms-empty-arabic-rtl.png`).
10. **No API shape change — PASS.** Wire request captured verbatim by the proxy:
    `GET /api/v1/terms-and-conditions` with content-type/accept/moduleid/x-localization
    (+ transport user-agent/accept-encoding/host/traceparent) and a minted x-request-id;
    body 0 bytes, no auth header. The diff adds only the Dart-side `handleError: false`, which
    is consumed in `ApiClient.handleResponse` and never touches the request.

## Regression sweep (bounded)
Home / Orders / Request / Profile tabs + Language switching (en->ar->bn->es->en) + both policy
entry points on Profile. Zero `EXCEPTION CAUGHT`, zero `RenderFlex overflowed`, zero red screens
across both boot sessions. The only [FAIL] lines in the whole run are the ones QA induced.
Second entry point (registration `condition_check_box_widget` -> same `RouteHelper.getTermsRoute()`)
NOT exercised live (requires logout); its call site is untouched by the diff and it pushes the
identical route/widget.

## Automated backstop
`flutter test test/features/html/html_viewer_states_test.dart --reporter expanded` -> 14/14 passed
(14 declared test cases in the file = 14 run, no load failure).
`flutter test` (full DeliveryApp suite) -> 267/267 passed.

## Findings
- **task_bug (low, breaks_ac: false)** — Retry paints no in-flight state and stacks concurrent
  requests on double-tap. Evidence: `bug-retry-no-inflight-state.log`.
- **followup (non-blocking, pre-existing convention)** — skeleton shimmer bars measure luminance
  244/255 on the white card (~1.09:1, below WCAG 3:1 for non-text UI) because they use
  `Theme.of(context).shadowColor` = `Colors.black.withValues(alpha: 0.03)` (light_theme.dart:11).
  This is the app-wide DeliveryApp shimmer convention — `OrderShimmerWidget` (the widget this
  skeleton documents itself as mirroring) uses the same token on lines 23/27/34/41. Not caused
  by this ticket; the bars are visible, just low-contrast.

---

## Delta re-QA (cycle 5) — task-bug fix verification, HEAD 2780cabd
Device emulator-5572 (AVD nears_qa_delivery, booted for this run; pool 5554/5560/5564/5568 all held).
Scope: the Retry in-flight-state task-bug + the route-scoping fix from review cycle 2 ONLY.
The full 10-point AC table from the cycle-4 PASS was NOT re-run (controller-only change).

| # | Delta check | Result | Evidence |
|---|---|---|---|
| D1 | Retry drops the stale error immediately; skeleton paints; content lands | PASS | delta-03/delta-04; mid-flight sample t+2.0s vs 8s response |
| D2 | Double/triple-tap Retry fires exactly ONE request | PASS | proxy request log: 1 line for 3 taps |
| D2b | Same route re-entered twice while fetch in flight -> ONE request | PASS | non-vacuous exercise of the re-entrancy guard |
| D3a | Terms in flight -> navigate to Privacy: Privacy fetches, shows PRIVACY, late Terms 200 discarded | PASS | delta-05, delta-route-scoping-proof.log |
| D3b | Reverse (Privacy in flight -> Terms): shows TERMS, late Privacy 200 discarded | PASS | delta-route-scoping-proof.log Case B |
| D4 | Cold entry skeleton -> content; empty state still distinct (no Retry) | PASS | delta-01/delta-02; "This page isn't available yet." |
| D5 | flutter test (targeted 18, full suite 271) | PASS | 18/18 and 271/271 visible |

Logs: 3 x [FAIL] http_status=500, all deliberately forced to reach the error state, each
paired with the visible error card. 0 unhandled exceptions / overflows.
