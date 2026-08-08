# NEARS-1586 — live QA (emulator-5558, worktree HEAD `77dbec19`, SDK 3.41.9)

**Verdict: FAIL** — 7 ACs PASS, AC5 NOT_VERIFIED (its deliverable is unreachable on
any runnable target), AC3 descoped. Nothing observed is broken; the block is an
undemonstrated AC plus a missing specced region.

## Freshness proof (both isolates)
| When | Isolate / pid | Symbol evaluated | Result |
|---|---|---|---|
| Before driving | `isolates/6975423775210819` pid 21005 | `ItemController.presentItemDetailSheet` signature | carries `cart: CartModel?`, `cartIndex: int?` |
| " | " | compiled `item_bottom_sheet.dart` (len 97199) | `NBottomSheet(`x2, `ItemImageViewWidget(`x1, `brSheetTop`x1, `GestureDetector(onVerticalDrag` **x0** |
| After reconnect | `isolates/8099720177763367` pid 28805 | same three | identical, source len 97199 unchanged |
| " | " | `item_bottom_sheet_shimmer.dart` | `NSkeleton(`x12, `shimmer_animation`x0 |

## Measured checks
| Check | Measurement | Verdict |
|---|---|---|
| QA-1 height | card top y=227px -> sheet 897.7dp; `0.9 x 997.33 = 897.6` | PASS (0.8 default excluded) |
| QA-1 radius | corner arc fits r=96px = **32.0dp**; verified at 2 rows (y+3 -> x=72, y+43 -> x=16) | PASS (15dp excluded) |
| QA-2 barrier parity | browse median alpha **0.2000** (n=6774) vs cart **0.2031** (n=2304); sheet top y=227 both | PASS (black54=0.54 excluded) |
| QA-4 slow drag 30% | 808px / 1500ms ~= 180dp/s -> **SPRING BACK**, Close bounds unchanged | expected narrowing |
| QA-4 fast flick | 808px / 100ms ~= 2693dp/s -> **DISMISSED** | native threshold works |
| QA-9 tap targets | Close 44x44, Favourite 44x44, Decrease 44x44, Increase 44x44 dp | PASS |
| QA-5 1.3x scale | scale proven live (Total Amount: 269x54px @1.0 -> 348x69px @1.3); range item 200-300 AED: name right edge 775 < price left 811; footer 396 -> 1001 gap; **0 overflow** | PASS |
| Small screen 360x640dp | 0 new overflow, all footer controls present, 44dp | PASS |
| Small screen 180x320dp (literal instruction) | 5 RenderFlex overflows in DLS `NRating`; footer controls absent | see bug log |
| QA-3 speed banner | `delivery_time: "20-30"` populated, but `NSpeedBanner` absent from the build | region not built |

## Per-AC
| AC | Verdict | Evidence |
|---|---|---|
| AC1 Grocery simple | PASS | Banana: hero 1/4, 1 AED + strike 2 AED, `DOZEN` chip, NQtyStepper, add -> cart |
| AC1 C3 (choice_options must survive) | PASS for item 84 | Size 250ml/500ml render; total 200 -> 300 AED on change; adds to cart. Items 86/91 are zone-2 only -> gap |
| AC2 Food modifiers + live price | PASS | item 16: Size REQUIRED->COMPLETED, Toppings x5; totals 9/11/12/24 = 8.99/11.49/11.99/23.98 |
| AC3 Pharmacy | DESCOPED | not demoed |
| AC4 mobile browse + mobile cart-line | PASS | both open the sheet, top edge y=227 identical; qty 1->2 UPDATES the row (2 items, 18 AED), still 2 rows |
| AC4 desktop x2 | NOT_VERIFIED | UserApp has only `android/` + `ios/`; no web/desktop scaffold |
| AC5 deep link | NOT_VERIFIED | link works (4/4 launches open the sheet) but the rebuilt loader route never builds - see bug log |
| AC6 three error branches | PASS | outOfZone: Change Location, **no Retry**; notFound: Back only, terminal; loadFailed: Retry that **recovered** live |
| AC7 multi-store basket | PASS | store 4 then store 5 -> "2 Item", **no reset dialog**, Burger Palace row survived |
| AC8 RTL/Arabic | PASS | Close-X 1188..1320 -> **24..156**; handle centre 671 vs 672; hero 1/4->2/4->3/4 on RTL-next; prices carry U+2066/U+2069 LTR isolates (live **and** strike) |
| AC9 capability parity | PASS w/ gaps | store link navigates, rating, favourite, unit chip, NON-VEG, description, closed-store notice, not-available panel, modifiers; **discount tag exactly once** (1 a11y node, only source = hero NBadge:107) |

## Logs
1571 app-log lines. Every `[FAIL]` maps to an error state I deliberately provoked
(403 out-of-zone x3, 404 notFound x2, network-off x2). **Zero unexplained
`[FAIL]`/`[ERR]`/exception on any happy path.** Correlation join verified
end-to-end: app `f27cfbe9-...` == backend `X-Request-Id` in `laravel.log`.

## Automated backstop
`flutter test` (SDK 3.41.9, worktree) -> **+3002 ~2 -6**. Base was +2989 ~2 -6.
Failure and skip counts identical to base; the 6 failures are
`category_screen_back_button`, `coupon_controller` x3, `dls_golden` light+dark
(the known `ink_sparkle.frag` shader artifact). None touches the changed surface.
