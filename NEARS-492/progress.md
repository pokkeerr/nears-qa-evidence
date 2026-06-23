# NEARS-492 QA progress (cycle 1) — device emulator-5556, build 10728531

Verdict: PASS. Light mode only (dark deferred). Backend up (config 200), baseUrl http://10.0.2.2:8000 (real local).

| AC | verdict | evidence | logs |
|----|---------|----------|------|
| 1 no empty white space (has/lacks matrix) | met | 02/04/05/07 grids + widget test (rated/unrated/OOS variants) | clean |
| 2 store-name slot -> rating/New | met | New pill live across all grids (02,04,05,07); rating row via widget test (live data returns rating_count=0) | clean |
| 3 no ETA badge / no gap | met | no "3-5" on any grid (01,02,04,05,07) + widget test asserts findsNothing | clean |
| 4 image taller 6:4 | met | visual 02/04/05 image ~60% vs detail ~40% | clean |
| 5 balanced 2-col / 1-col-wide / hscroll | met | 2-col store grid 04/05, search 02; hscroll Fresh Finds/Buy It Again 01 | clean |
| 6 non-ASCII/Arabic no mojibake | met | Arabic locale render 09 (جديد/عضوي/AED LTR), em-dash item name intact via API; NEARS-482 utf8.decode present | clean |
| 7 widget-test backstop green | met | 4/4 adaptive card tests pass; 112/112 full common/widgets suite | clean |

Discount card (priceOff RED + strikethrough): verified live 02/05 (12%/19% OFF red badge, strike price). Flat-type "30 AED OFF" also verified (01).
Out-of-stock: verified via widget test (seed has no grocery OOS; food OOS items in a module without stock-tracking). Disabled non-tappable "+", grayscale CLOSED, card tap allowed.
RTL mirroring: heart top-left, "+" bottom-left, badges start-side, price LTR (09). Verified.
Note (out of scope): store-screen "Recommended For You" rail uses WebItemWidget (not ItemWidget) -> still shows "TOWER MART" store-name line. Not one of the 7 grid surfaces; not a NEARS-492 regression. -> followup.
Note (pre-existing backend): item-list APIs return rating_count=0 despite DB rating_count>0 -> every card shows New pill live; rating row only reachable via widget test. -> regression_bug (out of scope).
