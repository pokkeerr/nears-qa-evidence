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

---

# RE-QA (fix-cycle) @ bc6bca1a — TARGETED: 2 Android star bottom sheets

Engineer extended the SAME star fix into the two Android bottom sheets. Goal:
positively demonstrate on-device that the 5 star rows in each sheet now
announce content-desc `'<n> stars'`, role Button, tap box >=44dp.
Density 420 -> 44dp = 115.5px.

## Re-QA checkpoints
- [x] build/install from worktree @ bc6bca1a — VM service :61958, app pid 13657, clean boot
- [x] Site 1: search filter bottom sheet — 5 stars a11y dump — **PASS**
- [x] Site 2: store filter bottom sheet — 5 stars a11y dump — **PASS**
- [x] behaviour: Site2 tap4->1-4 filled; Site1 tap3->1-3 filled; both Apply dismiss; logs clean
- [x] light PASS; dark DEFERRED (light-first policy — not booted/checked); RTL code-verified (see below)

## RE-QA VERDICT: PASS (both Android star bottom sheets now project labels)
Fix at bc6bca1a lands on the CORRECT Android surfaces (the two bottom sheets), unlike
the prior 963/964 fix that only touched web/desktop filter_widget.dart. Both star rows
now: content-desc `'<n> stars'`, role **Button**, tap box ~44dp (115-116px @ 420dpi =
the 44dp minWidth/minHeight constraint quantized to pixels), 5 discrete faint-navy chips,
each individually sets rating, Apply/Filter applies + dismisses. Logs clean throughout.
No task-bug. NOT fix-cycle-2 territory.

### RTL / Arabic
- Star label is code-localized: both files use `label: '${index+1} ${'stars'.tr}'`;
  `assets/language/ar.json "stars":"نجوم"`, `en.json "stars":"stars"`. The live English
  render "1 stars".."5 stars" IS the `.tr` output for the active en locale, proving the
  label flows through `.tr` (not hardcoded) -> under AR locale it resolves to "1 نجوم"..
- Live Arabic render NOT obtained: after selecting عربى (Settings->Language, pref showed
  عربى) AND a full force-stop+relaunch, the app UI stayed English ("Favourite","Deliver
  To","Grocery & Food" etc. never localized). This is a pre-existing locale-apply/persist
  behavior UNRELATED to the 964 star fix and out of this targeted scope -> logged as a
  non-blocking followup regression-candidate, not a task-bug, not a FAIL.

### Logs gate
Full logcat flutter scan + ui_errors across both sheets + all interactions: ZERO
`[FAIL]`/`[ERR]`/EXCEPTION/overflow/GetX-not-found. Clean.

### Dark mode
DEFERRED per light-first policy — not booted, not checked.

### Device note
emulator-5560 (nears_qa_wave56) unstable as warned: one uiautomator dump raced the modal
(sheet captured after dismiss) — recovered by re-opening + atomic dump. Force-stop for the
AR restart detached the flutter-run debug session; app kept running from the installed
bc6bca1a debug APK (star labels in the running binary = proof the fix shipped).

### Site 1 (search_filter_bottom_sheet_widget) — PASS @ bc6bca1a — reached via Search tab -> Filter (idle search)
| star | content-desc | role | clickable | size |
|------|--------------|------|-----------|------|
| 1 | `1 stars` | Button | true | 43.8x44.2dp (115x116px) |
| 2 | `2 stars` | Button | true | 44.2x44.2dp (116x116px) |
| 3 | `3 stars` | Button | true | 43.8x44.2dp (115x116px) |
| 4 | `4 stars` | Button | true | 44.2x44.2dp (116x116px) |
| 5 | `5 stars` | Button | true | 44.2x44.2dp (116x116px) |
- BEFORE (prior QA): ZERO a11y nodes for the 5 rating stars (no label at all). NOW: 5 Button nodes labelled ~44dp.
- sheet identity confirmed: Apply Filters + Reset + "Price: high/low to..." sort chips (search-specific).
- behaviour: tap "3 stars" -> stars 1-3 fill navy (setRating(3) OK); "Apply Filters" dismisses sheet. Logs clean.
- evidence: search_filter_dump.xml, search_filter_sheet_after.png, search_filter_3stars_selected.png

### Site 2 (store_filter_bottom_sheet_widget) — PASS @ bc6bca1a — reached via store detail (Abu Dhabi Fresh Market) toolbar Filter
| star | content-desc | role | clickable | size |
|------|--------------|------|-----------|------|
| 1 | `1 stars` | Button | true | 43.8x43.8dp (115x115px) |
| 2 | `2 stars` | Button | true | 44.2x43.8dp (116x115px) |
| 3 | `3 stars` | Button | true | 43.8x43.8dp (115x115px) |
| 4 | `4 stars` | Button | true | 44.2x43.8dp (116x115px) |
| 5 | `5 stars` | Button | true | 44.2x43.8dp (116x115px) |
- BEFORE (prior QA): role=View, EMPTY content-desc, 32.0x32.0dp. NOW: Button + labelled + ~44dp.
- 115/116px = 44dp logical constraint (minWidth/minHeight:44) quantized to pixels at 420dpi (44dp=115.5px). WCAG 2.5.5 met.
- behaviour: tap "4 stars" -> stars 1-4 fill navy (setRating(4) OK); mint "Filter" apply dismisses sheet. Logs clean.
- evidence: store_filter_dump.xml, store_filter_sheet_after.png, store_filter_4stars_selected.png
