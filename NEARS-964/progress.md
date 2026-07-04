# NEARS-964 live QA — completed per-site record

Device: emulator-5560 (420dpi → 44dp = 115.5px). Build: worktree
`fix/NEARS-964-a11y-tap-box-enlarge` @ 53d19b62. Light mode. Logged in
customer@nears.com, zone 2 (Abu Dhabi). Authoritative check = on-device
`uiautomator` AccessibilityNodeInfo dump (content-desc = TalkBack label,
class = role, bounds → dp). Logs gate (`ui_errors` logcat-flutter) = clean on
every surface exercised.

Positive control (mechanism works on this build): non-platform Semantics
buttons project correctly on-device — "Pick Location" role=Button 52dp,
bottom-nav Home/Categories/Search/Basket/Profile role=Button 64dp labelled,
app Back buttons role=Button 44.2dp. So the Semantics+≥44dp pattern DOES
project; the only failure mode observed is the Maps platform-view overlay.

| # | Site | Result | On-device evidence |
|---|------|--------|--------------------|
| 1 | Search filter dialog stars (`search/widgets/filter_widget.dart`) | UNVERIFIABLE on Android — web/desktop-only | Fixed dialog reachable only via `search_screen.dart:903` legacy `_actionSearch` else-path. Android Filter button opens `SearchFilterBottomSheetWidget`; its 5 "Rating" stars have ZERO a11y nodes (no label). |
| 2 | Store filter dialog stars (`store/widgets/filter_widget.dart`) | UNVERIFIABLE on Android — web/desktop-only | Fixed dialog (store_screen.dart:983) sits INSIDE the `///web view.. isDesktop()?` branch (line 467). Android toolbar filter opens `StoreFilterBottomSheetWidget`; its 5 stars = role=View, EMPTY content-desc, 32.0x32.0dp, bounds [53,2001]..[473,2085]. |
| 3 | Map zoom in/out (`select_location_view_widget.dart` !fromView) | RESOLVED — platform-view exclusion (ACCEPTABLE) | Over `Google Map` TextureView: no Zoom in/Zoom out/Use-current-location nodes across 2 dumps, while sibling non-overlay nodes ("Pick Location" 52dp Button, search bar) project. Buttons render + touch-usable. UX collision fix confirmed: location button separated above zoom card. |
| 4 | CustomToolTip info + Halal (`custom_tool_tip_widget.dart`) | UNVERIFIABLE — not reached | Default 'Info' trigger is in checkout (prescription picker / note); Halal caller on food-item detail. Not reached; Vitamin D3 pharmacy sheet had no info/halal tooltip. Source + nameTrigger gate reviewed correct. |
| 5 | Items-you-love arrows (`item_that_you_love_view.dart` forShop) | UNVERIFIABLE — no shop module | forShop:true only in `shop_home_screen` (ecommerce module); seed exposed grocery/food/pharmacy only. |
| 6 | Chat image-preview arrows (`image_preview_widget.dart`) | UNVERIFIABLE — no chat data | Needs a chat thread with 2+ images. |
| 7 | Web arrow button (`arrow_icon_button.dart`) | UNVERIFIABLE on Android — web-only | Desktop/web home rails only; not rendered on Android. |
| 8 | Prescription FAB (`store_screen.dart`) | UNVERIFIABLE — config/scroll gated | Reached CarePlus Pharmacy (Abu Dhabi, prescription_order=1) logged-in; FAB did not render (gated by module orderAttachment / prescriptionStatus / showFavButton). |
| 9 | highlight_widget arrows View store/Back | UNVERIFIABLE — no video ad | Arrows render on VIDEO ad cards; seeded home ads are image "Claim Deal" cards. |

## Verdict: BLOCKED (cannot certify on Android)
No NEARS-964 code defect found and the fix mechanism is proven on-device.
But 8 of 9 ACs are undemonstrable on this Android surface/seed:
- 1, 2, 7 are web/desktop-only → need a Flutter-web QA pass.
- 4, 5, 6, 8, 9 need mobile test data/config (checkout tooltip; shop module;
  chat images; prescription config + FAB scroll; a video advertisement).
- 3 is the only Android-resolvable site → acceptable platform-view exclusion.

## Scope decision for PO (blocks Done)
The ticket goal is "labels project on **Android** (WCAG 2.5.5)", yet the
rating-star fix (sites 1 & 2) lands only on the web/desktop dialogs. On Android
the rating-star filters (the two bottom sheets) remain fully unlabelled
(pre-existing, out of the literal 964 file scope). Decide: extend 964 to the
mobile `SearchFilterBottomSheetWidget` + `StoreFilterBottomSheetWidget`, or
accept web/desktop-only scope for the star fix and verify it on Flutter web.
