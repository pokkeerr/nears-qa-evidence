# NEARS-1109 — re-QA (fix-cycle 2), HEAD 2318a4d1, emulator-5556, light mode

Delta scope: AC3 (previously FAILed) + regression smoke. ACs 1,2,4,6,7,8 reused from cycle 1
(store_screen.dart + paginated_list_view.dart unchanged in 2318a4d1). AC5 stays NOT_RUN (NEARS-1122).

## AC3 — in-store search load-more (StoreItemSearchScreen, /search-store-item)
| # | check | result | evidence |
|---|-------|--------|----------|
| 3.1 | page-2 failure -> inline row, grid keeps 10 items, no fullscreen/toast | PASS | ac3-search-inline-error-row.png |
| 3.2 | page-skip gone: offset=3 never fetched (15 gestures) | PASS | 0 offset=3 reqs in proxy log |
| 3.3 | Retry re-fires SAME page: 2nd offset=2, items 11-20 append in order | PASS | ac3-retry-page2-appended.png |
| 3.4 | THE TELL: [WARN] paginated list: onPaginate(2) failed PRESENT | PASS | logcat 09:32:28.411 |
| 3.5 | scroll-jiggle -> no auto-retry (listener sealed) | PASS | only 1 offset=2 req across 15 gestures |
| 3.6 | NEW QUERY while row up -> row clears, grid resets to page 1 | **FAIL** | bug-stale-loadmorefailed-seals-pagination.{png,log} |

AC3 = FAIL (3.6). The fix correctly closed the original silent-drop, but introduced a NEW one.

## The new defect (blocks Done)
Stale `_loadMoreFailed` is never cleared on a new query/category change, because
paginated_list_view.dart didUpdateWidget only clears it when the MODEL offset moves
BACKWARDS -- and after a FAILED page 2 the model never advanced past 1, so the reset is a
1 -> 1 no-op. `_scrollListener` gates on `!_loadMoreFailed` => pagination SEALED.

Proven live on BOTH surfaces with a HEALTHY backend (fault injection OFF):
 - StoreItemSearchScreen: new query -> 0x offset=2, 0 new [WARN], stale row shown.
 - Store GRID (the AC1/AC2 surface that PASSED in cycle 1): after a failed page 2,
   switching category back to 'All' (21 items, page 2 exists) -> 12 scroll gestures,
   ZERO offset=2 requests, ZERO [WARN], stale row. 8 of 21 items unreachable for the session.

## Regression smoke
| surface | result |
|---|---|
| store grid: row + rollback under injection (cycle-1 surface) | PASS (row + [FAIL] + [WARN]) |
| store grid: normal pagination, fault off (control) | PASS (offset 1 -> 2, all 21) |
| store grid: pagination AFTER a failure, fault off | **FAIL** (sealed - see above) |
| home store list (non-store consumer), fault off | PASS (offset 1 -> 2, no row, no WARN) |
| other 5 non-store consumers (orders, chat x2, conversations, flash-sale) | PASS by mechanism: only the 2 store files call throwIfPageFailed, so _loadMoreFailed can never be raised there |

## Automated backstop
flutter test (UserApp): 2269 passed, incl. the 13-test NEARS-1109 pin suite (P7e green).
The pins are GREEN BUT BLIND: every pin covers fail -> retry -> same page. None covers
fail -> NEW QUERY / category change (the model 1 -> 1 no-op), which is where it breaks.
