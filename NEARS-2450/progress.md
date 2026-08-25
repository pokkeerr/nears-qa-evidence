# NEARS-2450 QA progress (express lane, cycle 2)

Device: emulator-5556 (Android). Worktree HEAD 29a7a373. Backend: shared
dev backend at 127.0.0.1:8000, routed through an ad-hoc QA fault/staging
proxy (127.0.0.1:8099, `--dart-define=API_HOST=10.0.2.2:8099`) for the
duration of the demonstration, then the app was rebuilt WITHOUT the
dart-define before releasing the device (clean state for the next session).

## Data DoR gap (partial — reachability solved, data did not exist)
`brands` table has 0 rows and 0 `ecommerce_item_details.brand_id` rows in
the dev DB (confirmed via read-only SELECT) — no real backend response for
ANY brandId can ever contain items. The ticket's suggested deep-link
technique (VM-service `evaluate`, `Get.toNamed(RouteHelper.getBrandsItemScreen(...))`)
DID work once `flutter run` was wrapped in `script -q` to give it a real
tty — a bare non-tty background launch loses the DDS ~seconds in (per the
nav guide's NEARS-1321 warning) and the JSON-RPC-over-HTTP evaluate path
returned "No compilation service available"; the raw VM `/ws` endpoint
(hand-rolled WS client, same technique as `ios_find.py`) worked cleanly.

Reachability itself was NOT a Data DoR gap once the tty issue was solved.
The remaining data gap — no real item ever attached to any brand — was
closed with the SAME "local rewriting proxy" technique the nav guide cites
as NEARS-2287 precedent (staged responses, not just staged failures): the
proxy staged synthetic-but-schema-correct `products` payloads (matching
`ItemModel`/`Item.fromJson`) for specific offsets, and separately injected
real transport failures (503/500) for other offsets — both go through the
REAL app code path (repository -> controller -> screen), never a mock at
the Dart layer, and never touch the DB.

## AC evidence
- AC1 [ui]: offset=1 failed (503, injected) -> `ac1-error-retry-state.png`,
  a11y dump confirms cloud-off icon + "Something went wrong" / "Please try
  again" / "Retry", vertically centered in viewport (not top-pinned). Log:
  `[FAIL] endpoint=/api/v1/brand/items/999002 http_status=503 type=ApiFailure`.
- AC2 [behav]: tapped Retry -> re-fired `GET /api/v1/brand/items/999002`
  (offset=1) -> staged 200 w/ 12 synthetic items -> `ac2-retry-recovery-grid.png`,
  a11y confirms 12-item grid rendered (`QA Synthetic Item 90000..90011`).
  Scroll-to-end fired offset=2 (staged 200, 8 more items) -> items
  90100-90107 appended -> pagination confirmed unaffected.
- AC3 [behav]: fresh nav with a 10s staged delay on offset=1 -> screenshot +
  a11y dump at t+4-8s show ONLY the appbar/back (no item labels, no error
  text) -> shimmer/loading state, unchanged. Resolved cleanly after the
  delay, no `[FAIL]`.
- AC4 [behav]: cleared all proxy rules (true pass-through to the real,
  unmodified backend) -> fresh brandId -> genuine empty response (0 items,
  since 0 real brand-linked items exist) -> "No Brand Item Found" ->
  `ac4-empty-state.png`. Log clean (200, no FAIL).
- Regression (load-more failure, footer row): staged offset=1 success (12
  items, total_size=25) + injected offset=2 failure (500) -> scrolled to
  end -> footer `NearsLoadMoreError` row + "Retry" appeared, full-pane
  state untouched -> `regression-loadmore-footer-error.png`. Log:
  `[FAIL] endpoint=/api/v1/brand/items/999003 http_status=500`.
- RTL: `Get.updateLocale(Locale('ar','SA'))` then fresh nav with offset=1
  failing -> Arabic strings (`حدث خطأ ما` / `يرجى المحاولة مرة أخرى` /
  `أعد المحاولة`) + a11y bounds show Back button mirrored to the right
  edge (`bounds=[912,79][1038,205]`, vs LTR's top-left) -> `rtl-error-retry.png`.

## Automated backstop
`~/Tools/flutter/bin/flutter test test/features/brands/` — 24/24 passed
(brands_first_page_error_retry_test.dart, brands_load_more_failure_test.dart,
brands_load_more_recovery_test.dart, brands_page_limit_coupling_test.dart).

## Regression sweep / unrelated findings
Repeated `E/com.facebook.GraphResponse ... Application has been deleted`
(HTTP 400, errorCode 190) throughout the whole session, from app startup
onward — unrelated to brands/NEARS-2450 (Facebook SDK config issue, present
before any brand-item interaction). Flagged as a followups[] regression
candidate, not a finding against this ticket.
