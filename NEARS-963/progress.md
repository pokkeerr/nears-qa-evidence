# NEARS-963 QA fix-cycle 3 progress (2026-07-04T08:51:00Z)
Device: emulator-5560 (AVD nears_qa_wave56)
Worktree: /Users/Apple/Projects/nears-NEARS-963-a11y-tail branch fix/NEARS-963-a11y-tail

SOURCE EDIT (search filter last-modified above) is what must PRE-DATE app.dill

===== BUILD FRESHNESS PROVEN (cycle 3) =====
- flutter run compiler root: /Users/Apple/Projects/nears-NEARS-963-a11y-tail/UserApp (the worktree)
- source edits: 12:42:26-12:43:04 (cycle-3 SizedBox shape)
- fresh app.dill: 12:52:15  (POST-dates source)
- fresh APK: 12:52:22
- clean install firstInstallTime==lastUpdateTime=12:52:28 (uninstalled cycle-2 build first)
- Dart VM Service: http://127.0.0.1:60526
VERDICT: running app == cycle-3 build. Results trustworthy.

===== AC4 SEARCH FILTER — FAIL (DECISIVE) =====
5 star nodes rendered at [53,2007]-[473,2091], each 84px wide, clickable=true focusable=true
content-desc = '' (EMPTY) ; class = android.view.View (NOT Button)
The "<n> stars" label is NOT projected. Same failure as cycles 1 & 2.
Cycle-3 fix (Semantics->InkWell->SizedBox(32==icon)->Icon) does NOT fix on-device.
Stars remain tappable (tap 4th star executed).

===== SIZE COMPARISON (FAIL root-cause finding) =====
Density 420dpi (x2.625). AC4 star vs device-proven AC5 toggle, same device same session:
  STAR (FAIL):  Semantics(button,label)->InkWell->SizedBox(32)->Icon(32). NO padding/deco.
                device node 84px = 32dp. content-desc='' class=View.  BOX == ICON.
  AC5  (PASS):  Semantics(button,selected,label)->InkWell->Container(margin2+pad5+BoxDecoration)->Icon(22).
                device node 94px = ~36dp. content-desc='Grid view' class=Button. BOX = icon+14dp, DECORATED.
CONCLUSION: 'non-leaf child' theory DISPROVEN (SizedBox is non-leaf yet fails).
Remaining differentiator = AC5 box is LARGER than its icon (padded ~64%) AND carries a BoxDecoration/paint;
the fix's SizedBox is layout-neutral (== icon, undecorated). Matching AC5 needs a padded/decorated box
= VISUAL CHANGE = product decision. (Confirms the engineer's cycle-3 RISK note.)

===== AC4 STORE FILTER — FAIL (confirmed second site) =====
5 stars at [53,2001]-[473,2085], 84px each, clickable=true, content-desc='' class=View.
Identical failure to search filter. AC4 FAILS on BOTH sheets.
===== AC5 store toggle regression — PASS =====
Grid view/List view content-desc present, class=Button, selected flips on tap. No regression.

===== AC3 map zoom (non-gating) =====
Live on location-picker map (select_location_view_widget). Two stacked zoom buttons
[912,1865]+[912,1999] over Google Map TextureView, both content-desc='' (empty).
Documented AC-path-(b) exclusion (platform-view). Same label-projection mechanism as AC4.
===== AC9 verified badge — PASS (no regression, code-confirmed) =====
Semantics(image:true,label)->Image. Diff unchanged from cycle-0/1/2 (3x live PASS).
cycle-3 SizedBox change targeted only bare-Icon InkWell sites, not this Image suffix.
===== AC1 halal — UNVERIFIABLE (data gap) =====
DB: 0 halal-active store_configs (halal_tag_status), 2 halal items. Condition
isStoreHalalActive && isHalalItem never satisfied -> tooltip never renders.
Shape: Semantics(button,label)->InkWell->Image(halalTag) — hybrid (failing outer nesting, AC9-like Image leaf).
===== CR-963-D1 — NOT reintroduced (structural + partial live) =====
CustomToolTip nameTrigger = child==null || semanticsLabel!=null. home_screen passes its own
child InkWell (navigateToLocationScreen) with NO semanticsLabel -> nameTrigger FALSE -> tooltip
does NOT wrap -> caller InkWell keeps 'select_your_location'+navigate. Live: home address-branch
selector announced its OWN content ('Deliver To: Your Location...'), NOT 'info'. Exact null-address
home branch gated behind app forced location-pick routing (not directly reachable live).
===== Visual neutrality — PASS =====
SizedBox == icon size (stars 32==32, zoom 25==25). Star device nodes 84px = 32dp = icon footprint.
Zero layout shift vs bare Icon. Bounds byte-identical.
===== FINAL logs-first sweep: CLEAN (no Flutter exceptions/overflow during ACs) =====
===== VERDICT: FAIL — AC4 rating stars still empty content-desc on BOTH sheets (3rd cycle). ESCALATE. =====
