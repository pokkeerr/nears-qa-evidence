# NEARS-1708 — live Arabic QA (on-device), 2026-08-11

Device: **emulator-5562** (AVD `nears_qa_delivery`, booted for this run — the whole documented
pool was held by live peer lanes: 5556→NEARS-1601, 5558→NEARS-1756, 5560→NEARS-1877, and 5554
was running a peer's UserApp with **no lock file**). Geometry overridden to the pool standard
**1344x2992 @ 480dpi (448x997dp)**. Lock key NEARS-1708, released on exit.
SDK: `/Users/Apple/Tools/flutter/bin/flutter` **3.41.9**; `pubspec.lock` meta = **1.17.0** (unpolluted).
Backend: `127.0.0.1:8000` live; app `baseUrl` → `http://10.0.2.2:8000`. Light mode only (dark deferred).

## Cache-trap controls (this run's evidence is not a picture of the cache)
- `pm clear com.izzes.nears` + full reinstall **between** the pre-fix and fixed builds.
- APK md5 differ: PRE `851e1d7ddd8b438d8d8bbb5ff45d3dfe` vs FIX `bef24720afe0e37d542dab3c7c3d9914`;
  `lastUpdateTime=2026-08-11 14:22` > `firstInstallTime=05:51` confirms the swap.
- **Positive control on every capture**: backend request activity bracketing the capture window
  (3–63 distinct `correlation_id`s per window). No capture was taken in a zero-request window.
- uiautomator used for **navigation only** — it reports logical text, so every AC1/AC2 verdict
  below is read off a **screenshot**.

## PRE-FIX — `/Users/Apple/Projects/nears-NEARS-1708-BASE` @ dde904f1
| Surface | Logical text | Visual render | Defect |
|---|---|---|---|
| Order card | `10 Jul 2026,  10:19 PM  •  #176` | `Jul 2026,  10:19 PM  •  #176 10` | day `10` displaced to end |
| Chat bubble | `07:33 PM \| 16-Jul-2026` | `PM \| 16-Jul-2026 07:33` | time `07:33` displaced to end |
| Review row | `10 Jul 2026` | `Jul 2026 10` | day `10` displaced to end |

Reproduced on all three named surfaces.

## FIXED — `/Users/Apple/Projects/nears-NEARS-1708-date-bidi` @ 1442d28e
Logical text now carries the LRE/PDF pair (`‪…‬`); visual order matches the format string.

| AC | Surface | Result |
|---|---|---|
| AC1/AC2 | Order card | **PASS** — `10 Jul 2026,  10:19 PM  •  #176`, row still mirrors, digits not reversed |
| AC1/AC2 | Chat bubble | **PASS** — `07:33 PM \| 16-Jul-2026` |
| AC1/AC2 | Review row | **PASS** — `10 Jul 2026` |
| AC3 | English, order card | **PASS** — unchanged, no visible glyph from LRE/PDF |
| AC3 | English, chat bubble | **PASS** — unchanged, no visible glyph |
| AC4 | Today/Yesterday | **NOT DEMONSTRABLE** — see below |

### AC4 — why it is not demonstrable (not a pass, not a fail)
`ar.json` carries both keys (`today`→`اليوم`, `yesterday`→`أمس`), and **`'today'.tr` was observed
rendering `اليوم` live in Arabic** on the checkout time-slot sheet (`time_slot_bottom_sheet.dart`
uses `'today'.tr`) — captured in `post-timeslot-range-ar.png`. But the two AC4 date-branch call
sites — `convertTodayYesterdayFormat` (chat bubble) and `convertTodayYesterdayDate` (notification
screen) — have **zero** qualifying records: reviews today/yesterday = 0, orders = 0, messages = 0,
notifications today = 0. The one reachable chat thread is **read-only** (no composer), so no
today-dated message could be created through the app either. DB writes are forbidden.
`أمس` was never rendered. Reported `unverifiable`, not passed.

## The two previously-`unverified` claims — BOTH RUN
### 1. THE WIRE CLAIM — **VERIFIED, PASSES**
A **scheduled order was actually placed in Arabic** (slot 06:00 PM–07:00 PM):
order **#91113**, `scheduled=1`, `schedule_at=2026-08-11 19:01:00`, `order_status=pending`.
No 422, no rejection, order count 60 → 61.
Decisive byte-level proof that `dateToDateAndTime` stayed unwrapped:
```
HEX(schedule_at) = 323032362D30382D31312031393A30313A3030   LENGTH = 19
a wrapped value would be  E280AA…E280AC                      LENGTH = 21
```
Zero directional marks reached the wire or the database. The seven-method exclusion is correct,
proven on the wire rather than by static reading.

### 2. THE CHAT ROUND-TRIP — **VERIFIED, PASSES**
Conversation **list** and a **thread** both opened in Arabic on the fixed build. List populated,
all timestamps rendered, **no `FormatException`**, presence dot not dark. Log check scoped to the
live app pid: **0** `[FAIL]`/`[ERR]`/`FormatException`, against a non-vacuous control of 387 lines
for that pid (260 flutter lines).

## Range check (the rejected-isolate regression)
Checkout time-slot sheet in Arabic renders every range **start→end**: `03:00 PM - 04:00 PM`,
`05:00 PM - 06:00 PM` … **not inverted**. The rejected LRI/PDI mechanism would have shown
`04:00 PM - 03:00 PM`. The chosen LRE/PDF mechanism did not reintroduce range inversion.

## Automated backstop
`flutter test test/helper/date_converter_bidi_test.dart test/features/review/review_widget_dls_test.dart
test/features/chat/message_bubble_dls_test.dart` → **All tests passed (63)**, SDK 3.41.9.

## Regression sweep (light mode, Arabic + English)
Order list · order details · order tracking/status hero · conversation list · chat thread ·
store review screen · profile "Joined" (`انضم ‪14 May, 2026‬`) · checkout · time-slot sheet ·
cart · item sheet · store screen — all render dates in format-string order, no crashes,
no red screens, no `FormatException`.

## Findings NOT caused by this ticket (pre-existing — see envelope `regression_bugs`)
1. `bug-unsubstituted-amount-placeholder.png` — checkout minimum-order gate body renders the
   **literal placeholder** `أضف @amount آخر للوصول للحد الأدنى`; `@amount` is never substituted.
2. `bug-min-order-gate-stale.png` — both stores kept failing the `minimum_order` gate with
   subtotals visibly **above** their minimums (Nears Mart 27 ≥ 20, Fresh Mart 8 ≥ 5), and
   place-order stayed disabled; a fresh checkout entry did not clear it. Needs owner confirmation
   of the backend rule before being called a defect outright.
3. `[FAIL] endpoint=/api/v1/customer/cart/update http_status=404 correlation_id=b95aa002-…`
   on cart item removal. Correctly logged (no silent-failure violation), but a 404 on a normal
   cart edit is wrong.
