# NEARS-3927 QA [8] — fix cycle 0 — progress

Build: HEAD 6013e4e40 (fix/NEARS-3927-row-host-text-scale-sizing), UserApp debug, pkg com.izzes.nears.nears_nears_3927_row_host_text_scale_siz, built 07:00 from the worktree (qa-run.sh --root <worktree>)
Device: emulator-5554, 1344x2992 @480dpi (448dp wide), light mode; font_scale 1.0 / 1.3
Backend: primary Admin tree (/Users/Apple/Projects/nears @ e98917575) on :8127, DB_DATABASE=nears_qa_3927 (--no-reload), proven via copy-only marker (item 1 name "Sample Product QA3927COPY" returned by :8127 API; shared DB unchanged)

| AC / scope | status | evidence | logs |
|---|---|---|---|
| AC1 rail EN 1.3x brand+unit (Green Cross Pharmacy, unit kg) | PASS | rail-en13-brandunit(-crop).png: cards 1620..2151px = 177dp (1.0x = 130dp), price "9.62 AED" fully drawn, '+' 44dp beside, uniform height both cards; bottom whitespace = accepted trade-off | clean (0 overflowed / [ERR] in window) |
| Scope 1 rail EN 1.3x swipe to end | PASS | 18 horizontal swipes to last card (Ibuprofen 400mg); all cards one height 531px/177dp; HorizontalScrollView full width [0..1344]; rail-en13-end.png | clean |
| Scope 3 stable card EN 1.3x | PASS | tap '+' Hand Sanitizer: stepper state (a11y "...\n1") card [1636..2167] = 531px; after re-filter [1636..2167] = 531px; same after Ibuprofen left the rail (rail-en13-stepper-transient.png) | clean |
| AC2 rail AR 1.3x brand+unit (Nasal Spray / Sunscreen, unit kg) | PASS | rail-ar13-brandunit(-crop).png: cards [1225..1774] = 549px/183dp, price "د.إ. 9.62" fully drawn, RTL mirrored (header right, image right, '+' at left), uniform height | clean |
| Scope 1 rail AR 1.3x swipe to end (pharmacy) | PASS | 18 LTR swipes (RTL forward) to last card; cards one height 549px/183dp | clean |
| AC3 rail AR 1.3x brand+rating+discounted '+' state (Chicago Style Cheese 12% OFF, Spice Route Kitchen, food module = rating meta) | FAIL | rail-ar13-brandrating-disc(-crop).png + bug-rail-13x-discount-strike-dropped.png (1.0x vs 1.3x): zero overflow, current price "د.إ. 37.99" whole, BUT strike NOT drawn at 1.3x (a11y label lacks 43.17; at 1.0x same card label + paint carry "43.17"). Only the 12% OFF image pill carries the discount. Card has visible bottom whitespace -> not height-starved; width-driven DLS W2 drop (decisionWidth=infoWidth says beside, inline width beside the 44dp '+' leaves < strike floor) | clean (no overflow, no [ERR]) |
| AC4 item_view asSliver — store_screen.dart:2179 (Green Cross Pharmacy, non-food, list view) AR 1.3x | PASS (no-brand rows: inStore hides brand) | iv-store-ar13.png: SliverList rows 324px/108dp content-sized, separator 45px/15dp, discounted rows draw BOTH prices (Throat Lozenges 37.49 + strike 42.12; Omega-3 28.98 + 36.22; Adhesive Bandages 24.61 + 26.18), in-cart stepper rows same 324px; pagination: 2nd GET /api/v1/items/latest 200 fired on scroll | clean |
| Analytics view_item_list basket_suggestions | PASS | fires once per mount/distinct list: item_count 7 -> 6 -> 5 as cards were added; no duplicate within a mount | clean |
| AC4 item_view non-sliver — fav_item_view_widget.dart:42 Favourites items tab AR 1.3x brand+unit (MediQuick Pharmacy) | PASS | iv-fav-ar13-brandunit.png: rows 387px/129dp content-sized, separator 45px/15dp, discounted Omega-3 draws 17.10 + strike 21.38 | clean |
| (incident) ANR on emulator-5554 07:25:27 after heart tap -> BACK -> Profile; app CPU idle afterwards, dialog re-armed; host iow 188%. force-stop + monkey relaunch (state kept); flutter run lost connection -> logs from adb logcat flutter:V from here | env | anr-environment.log | n/a |
| AC4 item_view non-sliver — Favourites items tab AR 1.3x brand+rating (Spice Route Kitchen: Chicago Style Cheese 12% OFF, Chef Salad) | PASS | iv-fav-ar13-brandrating.png: rows 402px/134dp content-sized, separator 45px; discounted row draws current 37.99 AND strike 43.17 (full-width card) | clean |
| AC4 Favourites items tab EN 1.3x brand+rating (Chicago Style Cheese 12% OFF, Chef Salad) | PASS | iv-fav-en13-brandrating.png: rows 390px/130dp, both prices 37.99 + 43.17 | clean |
| AC4 Favourites items tab EN 1.3x brand+unit (MediQuick: Sunscreen, Omega-3 20% OFF) | PASS | iv-fav-en13-brandunit.png: rows 375px/125dp, separator 45px, both prices 17.10 + 21.38 | clean |
| AC4 item_view asSliver store_screen EN 1.3x (Green Cross list view) | PASS | iv-store-en13.png: SliverList rows 312px/104dp, separator 45px, discounted rows show both prices; scroll fired 2nd GET /api/v1/items/latest (200) = pagination loads | clean |
| AC3 context EN 1.3x food rail | (FAIL context) | rail-en13-brandrating-disc.png: Chicago Style Cheese 12% OFF label carries only 37.99 -> strike also dropped in EN at 1.3x; cards 531px/177dp | clean |
| Scope 3 stable card with discounted (tallest) card EN 1.3x | PASS | tap '+' Chicago: stepper state label "...\n1" shown, then re-filter; rail cards 531px before and after the discounted card left (no shrink) | clean |
| Targeted tests | PASS | flutter test cart_suggestion_rail_row_golden_test + item_view_row_golden_test + test/common/widgets/card_design/ : 135/135 | - |
| AC5 1.0x both hosts | PASS | rail EN/AR 1.0x cards 390px = 130dp (unchanged SizedBox branch): rail-en10-brandunit.png, rail-ar10-brandrating-disc.png (strike drawn at 1.0x), rail-en10-brandrating.png; item_view 1.0x rows 366px = 122dp fixed grid + 45px spacing: iv-store-en10.png, iv-fav-en10.png; 6 alchemist goldens (1.0x, rail+item_view box/sliver, EN/AR) green in the 135-test run | clean |
| AC4 not checked live | - | brands_product_screen.dart:68 and item_campaign_screen.dart:47 not driven (same ItemsView non-sliver branch as Favourites; covered by row_card_host_text_scale_test) | - |

Session-wide log scan (flutter run log + logcat after relaunch): 0 "overflowed", 0 EXCEPTION CAUGHT. [FAIL] lines are environmental only (Firebase off: no google-services.json by instruction; pick-map onMapCreated timeout; one cart/add 403 store_closed for a closed-store home card, paired [FAIL]+[ERR] snackbar log).
Instrument note: the same I/flutter channel captured "RenderConstraintsTransformBox overflowed by 15|20 pixels" on this rail in NEARS-3903 QA (bug-rail-brand-unit-overflow-head.log) - positive control for the overflow grep.
Private DB writes (nears_qa_3927 only): carts +4 (Ibuprofen, Hand Sanitizer, Falafel Wrap, Chicago Style Cheese), wishlists +2 (542, 544), marker item 1 name. Shared multi_food_db: carts user 6 = 5 (unchanged), wishlists 542/544 = 0, item 1 name unchanged (write landed on copy only).
font_scale reset to 1.0.

# Fix cycle 1 — DELTA re-QA (AC3 only, per re-read in Jira comment 22445)

Build: HEAD 8737e3d06 (lib/ identical to 6013e4e40: `git diff --stat 6013e4e40..8737e3d06 -- UserApp/lib` empty); cycle-0 APK was gone from 5554, rebuilt via qa-run.sh --root <worktree> --dart-define API_HOST=10.0.2.2:8127
Device: emulator-5554 (lock NEARS-3927), 1344x2992 @480dpi, light mode
Backend: /Users/Apple/Projects/nears/Admin/public (lsof cwd) @ d160b0fa4, :8127, DB_DATABASE=nears_qa_3927 --no-reload; copy proven by marker item 1 "Sample Product QA3927COPY" via :8127
Private DB writes (copy only): cart row item 542 removed (to reach the '+' state), wishlist 542 removed (unfavourite probe). Shared multi_food_db: carts user 6 = 5, wishlists 542 = 0 (unchanged).

| AC / scope | status | evidence | logs |
|---|---|---|---|
| AC3 EN 1.3x Chicago Style Cheese '+' state | FAIL (re-read condition: pill must be drawn whole) | c1-rail-en13-disc-plus(-crop).png: card [45,1596][975,2127] 531px/177dp; label '12% OFF / ... / 37.99 AED' (no 43.17 -> strike absent); '+' = Add To Cart button [723,1929][855,2037]; price 37.99 AED whole; zero overflow. BUT pill (red, x 96..325, y 1662..1733) sits under the Favourite heart (Switch [192,1662][324,1794]); visible text reads '12% O' — 'FF' hidden | clean (0 overflowed, 0 EXCEPTION; only env Firebase [FAIL]s) |
| AC3 AR 1.3x same card '+' state | FAIL (same) | c1-rail-ar13-disc-plus(-crop).png: card [369,1587][1299,2136] 549px/183dp; label no 43.17 (strike absent); price 'د.إ. 37.99' whole; '+' [489,1938][621,2046]; pill x 1018..1247 under heart [1020,1653][1152,1785]; visible 'F 12%' — 'OF' hidden | clean |
| Pill occlusion is favourite-state independent | observed | unfavourited 542 (AR 1.3x): red pill px 8391 both states; heart backdrop covers same area | clean |
| Pre-existing at 1.0x | observed | bug-rail-13x-discount-pill-occluded-by-heart.png (EN 1.0x vs 1.3x): 1.0x shows '12% OF' + NO strike in EN; bug-rail-13x-discount-pill-occluded-by-heart-ar.png (AR 1.0x vs 1.3x): 1.0x pill x 1083..1247 overlaps heart x 1020..1152, strike 43.17 drawn in AR 1.0x | clean |
| Targeted tests | PASS | flutter test --no-pub test/common/widgets/card_design/ + cart_suggestion_rail_row_golden_test + item_view_row_golden_test: 147/147 | - |
| AC1 AC2 AC4 AC5 | carried from cycle 0 (PASS) | no product-code change since cycle 0 | - |
font_scale reset to 1.0.
