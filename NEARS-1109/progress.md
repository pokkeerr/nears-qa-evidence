# NEARS-1109 — LIVE QA (fix-cycle 5, cycle 1 of 2)
Device: emulator-5554 (Android). Build: worktree `feat/NEARS-1109-store-loadmore-silent` @ b83fc029.
Suite: `flutter test` = **2292 passed / 0 failed**. `flutter analyze` = 5 info lints (pre-existing test-file style).

Instrument: QA reverse proxy :8099 -> :8000. Asymmetric fault: 500 **iff** path==target AND offset==2
(offset=1 and offset=3 pass through), so a page-skip is visible. Every request+returned ids logged.

Data note: switched the delivery address to the user's saved **zone-2 (Abu Dhabi)** address. The default
zone (364) has only 3 stores x 15 items and NOTHING there paginates. Zone 2 holds the paginable fixtures.

| AC | status | evidence |
|----|--------|----------|
| AC1 store grid offset>1 -> inline row | PASS | store 12, offset=1 200 (13 items), offset=2 INJECTED 500 -> compact inline "Couldn't load more"+Retry at grid bottom (635,2590). NOT a toast, NOT full-screen; grid intact. `cycle5-ac1-inline-row-store-grid.png` |
| AC2 offer-category + store-wide offers paths | PASS | store 4117. store-wide `/categories/items/offers` offset=2 -> 500 -> inline row+Retry (635,2590). offer sub-category `/categories/items/144?offers=1` offset=2 -> 500 -> inline row+Retry. |
| AC3 Retry re-fires SAME offset, no hole | PASS | offset=2 x3 (initial + 2 retries), **offset=3 = 0**. Healed retry -> 200 n=8 ids=[86,87,88,90,91,92,93,94] == healthy baseline exactly. Rendered: "4X4 Rubiks Cube","Latus","Fresh Organic Tomato". `cycle5-ac3-no-page-skip.log` |
| AC4 offset==1 -> full-screen NearsErrorRetry | PASS | offset=1 INJECTED 500 -> "Something went wrong" + "Please check your connection and try again" + Retry (672,2243). Inline row absent. |
| AC5 AppLogger.failure + PII | PASS | `[FAIL] endpoint=/api/v1/items/latest http_status=500 type=ApiFailure` (+ items/search, categories/items/offers, categories/items/). ApiFailure sentinel, path-only endpoint. PII gate: 0 '?' query strings; 0 hits for latitude/longitude/token/phone/password/store_id=/offset=/name=/Bearer. `cycle5-ac5-applogger-pii-safe.log` |
| AC6(a) category tab | PASS | seal -> switch category -> row gone -> back to All -> offset=2 200 n=8 ids=[86..94] appended |
| AC6(b) open in-store search | PASS | seal -> open search -> row gone on new surface |
| AC6(c) new query | PASS | seal on 'a' -> type 'e' -> row gone -> offset=2 200 n=10 ids=[62,64,88,93,94,91,90,87,201,92] |
| AC6(d) close search | PASS | seal -> close search -> row gone; the failed page re-fires at the **same** offset=2 -> 200 n=10 (no skip) |
| AC6(e) veg/organic filter | PASS (equivalent) | No veg/organic control exists on the store screen in this build (grocery: Discounted/Price/Ratings; food adds "Currently Available"). Ran the type-filter equivalent on food store 49: seal -> filter -> row gone -> **offset=2 200 n=2 ids=[551,552]** on the NEW list |
| AC6(f) price/discounted chip | PASS | seal -> "Discounted Items" -> row gone, new list total=6 -> clear filter -> offset=2 200 n=8 ids=[86..94] |
| AC6(g) Offers chip | PASS | seal All grid (4117) -> enter Offers -> row gone -> offset=2 200 n=2 ids=[61545,61546] |
| AC6(h) offer sub-category chip | PASS | seal store-wide offers -> tap "NEARS600 Deals" -> row gone -> offset=2 200 n=2 ids=[61545,61546] appended |
| AC7 seal holds inside one list | PASS | after failed page 2, ~26 scroll gestures -> **0** requests, row persists, grid intact. Same on StoreItemSearchScreen (16+ gestures -> 0). `cycle5-ac7-seal-holds.log` |
| AC8 store app-bar Search screen | PASS | query 'a': offset=1 200 n=10, offset=2 INJECTED -> inline row. New query 'e': row gone, offset=2 200 n=10 -> page 2 loads |
| AC9 N1 cross-axis interleave | NOT_RUN | **CategoryItemScreen is unreachable on mobile.** Both entry points are desktop-only: `category_view.dart:192` (`isMobile ? SizedBox : CategoryPopUp`) and `category_screen.dart:132` (`if (isDesktop)` branch holds the grid whose onTap -> getCategoryItemRoute). |
| AC10 N5 pre-existing store page-skip | NOT_RUN | same surface (CategoryItemScreen, mobile-unreachable). Also unreachable by data: no category exceeds 5 items in any seeded zone (needs >=21 for page 3). |
| AC11-1 Home store list | PASS | offset=1 total=20 n=12 ids=[8,9,12,13,14,16,17,18,19,20,21,22]; **offset=2 n=8** ids=[35,3168,3380,4004,4006,4009,4117,4118]. No error row. |
| AC11-2 My Orders | PASS | paged **offset=2,3,4,5** all 200 (51 seeded orders). No error row, no stuck spinner. |
| AC11-3/4 Chat lists | NOT_RUN (data) | `/customer/message/list?limit=10&offset=1` 200, renders clean, no error row / no stuck spinner. Only **3 conversations** seeded -> offset=2 can never fire (limit 10). |
| AC11-5 Conversation (reverse:true) | NOT_RUN (data) | `/customer/message/details?offset=1&limit=10` 200, renders clean, no error row. Max **1 message** per conversation -> offset=2 can never fire. |
| AC11-6 Flash-sale details grid | NOT_RUN (data) | Flash sale renders (live countdown). Only **6 items** per flash sale -> single page, offset=2 can never fire. |

## Coverage gap (reported, not a defect)
The **CategoryController / CategoryScreen half of the diff (~140 lines) has NO live-demonstrable path**
on seeded data: every category item list returns <=5 items and the CategoryScreen Offers rail returns 5
(limit is 10), so offset=2 can never fire; and CategoryItemScreen is mobile-unreachable. That half is
covered by unit tests only. Given this ticket's history (13 green pins over a broken app), flagging it.
