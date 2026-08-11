# NEARS-1837 — QA progress log (append-only)

Device: emulator-5554 (physical 1344x2992 @ 480 = 448x997dp, NO active override).
Lock: acquired 2026-08-11T14:17:09Z, owner pid 40511 (kind=anchor), key NEARS-1837.
Disk at acquire: 1234892 KB free (1205.9 MB) — above the 800 MB floor.
Flutter: /Users/Apple/Tools/flutter/bin/flutter 3.41.9 (framework 00b0c91f06). meta pin = 1.17.0.

## PREDICTIONS — written BEFORE any measurement

Mapping assumed: a Flutter `Semantics(label:, button: true)` node surfaces in a uiautomator
dump as a virtual node whose `content-desc` is the label. Both arms are `button: true`, so
the node class must be identical across arms — that is what makes star 5 a same-class control.

### AC1 (BASELINE build, NEARS-964 decorated >=44dp box)
- Lesson-true reading: five nodes, content-desc "1 stars".."5 stars", clickable="true".
- Lesson-false reading: n/a — AC1 is not the discriminator. If AC1's stars do NOT project,
  the instrument itself is suspect and I escalate rather than concluding anything.
- Map-zoom: two nodes carrying the zoom-in / zoom-out labels.

### AC2 (EXPERIMENT build)
- Star index 4 (5th, DECORATED control) MUST come back with a real non-empty content-desc
  ("5 stars"). If it is empty, the dump is uninterpretable -> escalate, conclude nothing.
- Stars index 0..3 (BARE arm):
  - **If the NEARS-963 lesson is TRUE**: these four carry NO content-desc (absent from the
    dump, or present with content-desc="") while star 5 carries "5 stars".
  - **If the NEARS-963 lesson is FALSE (an artifact of 963's method)**: these four carry
    content-desc "1 stars".."4 stars", indistinguishable from star 5 apart from bounds.
- Both outcomes are acceptable results. No preference.

## Log

### AC1 part 1 — rating-star row (BASELINE build) : PASS
Freshness stage 1 (md5): built baseline APK md5 `4cbaef2e42d553c1711be0b1a56b59d8`
(112,718,558 B) == installed `/data/app/.../base.apk` md5, checked BEFORE and AFTER the
observation. lastUpdateTime 2026-08-11 18:19:46.
Freshness stage 2 (live VM service, http://127.0.0.1:53297/hXG9pNrzyBc=/):
  library `package:sixam_mart/.../search_filter_bottom_sheet_widget.dart` -> libraries/@1496487427
  EVAL positive control `SearchFilterBottomSheetWidget` -> OK kind=Type  (eval instrument alive)
  EVAL `kNears1837BuildVariant` -> "Undefined name" => BASELINE PROVEN RUNNING.
JIT precondition: kernel_blob.bin present (1), libapp.so count 0 => Debug/JIT. STATED.
Nav: Home -> Food & Restaurant module -> module search -> "Filter" (content-desc).
Surface identification: `Get.isDialogOpen` == false live while the rating stars were on
screen; `ResponsiveHelper.isDesktop(Get.context!)` == false => the mobile branch ran and the
surface is the showModalBottomSheet-hosted SearchFilterBottomSheetWidget, NOT FilterWidget.
Geometry corroborates: "Scrim" node bounds [0,0][1344,1012] => sheet is bottom-anchored.
Dumps: 3 taken (ac1sheet-d1/d2/d3), d1 DISCARDED per protocol; d1==d2==d3 by md5
(112192f3c5e6b13bb0aedad84b761fe8) so the discard changed nothing here.
In-dump positive control: `Close` — class android.widget.Button, content-desc="Close"
(NON-EMPTY, asserted), same class as the star nodes, same dump d2/d3.
Result: all five stars project. 132x132 px bounds = 44x44 dp exactly.
Logs: ui_errors rc=0, 17 matches — ALL from foreign dead pids 19555/22121 @ 17:03-17:10,
outside my window. My app pid 24854: 122 flutter lines scanned (instrument alive), 0 [FAIL]/[ERR].

### AC1 part 2 — map-zoom controls (BASELINE build) : PASS
Nav: Profile tab -> scroll -> "Open Vendor" -> Vendor Registration -> scroll to Location Info
-> "Select Zone" (ui_tap returned **exit 3 AMBIGUOUS**, 2 nodes; re-issued as
`ui_tap "Select Zone" --first` which picked the clickable dropdown) -> "Abu Dhabi Zone"
-> the 30x30 expand control. That control carries NO Semantics in source and dumps as
content-desc="" so it is unreachable by label; it was resolved LIVE from the dump by a
structural predicate (only small unlabelled clickable inside the "Google Map" container)
-> [1131,2221][1266,2311] -> centre 1198,2266. Not a written-down coordinate.
GoogleMap platform view: **RENDERED** — android.view.TextureView, content-desc="Google Map",
bounds [0,369][1344,2972], drawing-order=1. The zoom labels project ON TOP of it.
Dumps: 3 (ac1map-d1/d2/d3), d1 DISCARDED; all three identical (md5 6f429536ea468cc1dbb0b1ac8b9faaf3).
In-dump positive control: `Use my current location` — android.widget.Button, content-desc
NON-EMPTY, same class as the zoom nodes, same dump.
Result: "Zoom in" + "Zoom out" both project. 132x132 px = 44x44 dp.
Post-observation freshness: installed md5 unchanged 4cbaef2e...; VM re-eval unchanged
(control resolves, kNears1837BuildVariant still Undefined) => baseline never swapped mid-AC.
Logs: my pid 24854, 216 flutter lines scanned, 0 [FAIL]/[ERR].

### Corroborating observation on the SAME baseline build (not an AC)
`search_navy_header_widget.dart` back button is the EXACT bare shape NEARS-963 says cannot
project: Semantics(button,label:'back') > InkWell > Padding(all 4) > Icon(18dp). No
decoration, no >=44dp box, no container:true, no MergeSemantics. Raw node, dump searchnow-d2:
  class="android.widget.Button" content-desc="Back" clickable="true" bounds="[45,189][129,273]"
84x84 px = 28x28 dp. It PROJECTS.

### AC2 — the experiment (EXPERIMENT build) : PASS (measurement completed cleanly)
Freshness stage 1 (md5): installed `/data/app/.../base.apk` md5 = 7bda7e1974ee4aded2b7bf399ea4e5d1
== the handed-over experiment APK (142,072,151 B) EXACTLY. Checked before AND after the
observation, unchanged. lastUpdateTime 2026-08-11 18:36:00.
Freshness stage 2 (live VM service, http://127.0.0.1:56813/sMbckqK0k_E=/):
  EVAL positive control `SearchFilterBottomSheetWidget` -> OK kind=Type (eval instrument alive)
  EVAL `kNears1837BuildVariant` -> OK kind=String value='AC2-BARE-EXPERIMENT'
  => EXPERIMENT PROVEN RUNNING. Re-evaluated after the observation: unchanged.
JIT precondition: kernel_blob.bin present (1), libapp.so count 0 => Debug/JIT confirmed.
Precondition: rating filter UNSET — `Get.find<SearchController>().rating` == -1,
`storeRating` == -1, `isStore` == false, read live BEFORE dumping. All five stars therefore
render star_border_rounded in the identical visual state.
Surface: `Get.isDialogOpen` == false, `isDesktop` == false, Scrim [0,0][1344,1012] => bottom sheet.
Dumps: 4 taken (ac2sheet-d1..d4), d1 DISCARDED per protocol; all four byte-identical
(md5 c3655926f81f0a72783a0d8f715d0396).
In-dump positive control (REQUIRED positive, star index 4 = decorated arm):
  content-desc="5 stars" — NON-EMPTY, class android.widget.Button, dump ac2sheet-d3. ASSERTED.
Second same-class control in the same dump: content-desc="Close".

RESULT — the four BARE-arm stars ALL PROJECT:
  1 stars  class=android.widget.Button clickable=true bounds=[60,2515][156,2611]   96x96 px = 32x32 dp
  2 stars  class=android.widget.Button clickable=true bounds=[171,2515][267,2611]  96x96 px = 32x32 dp
  3 stars  class=android.widget.Button clickable=true bounds=[282,2515][378,2611]  96x96 px = 32x32 dp
  4 stars  class=android.widget.Button clickable=true bounds=[393,2515][489,2611]  96x96 px = 32x32 dp
  5 stars  class=android.widget.Button clickable=true bounds=[504,2497][636,2629] 132x132 px = 44x44 dp  <- CONTROL
The 32dp vs 44dp bounds split is the internal-validity check: it proves the bare arm really is
the undecorated shape in the RUNNING build, not the baseline's decorated one.

ACTIONABILITY (stronger than presence): `ui_tap "3 stars"` resolved the BARE-arm node by LABEL
and fired its callback — `rating` went -1 -> 3 over the live VM service. So the node is a real,
findable, activatable a11y node, not a stale dump ghost.

Logs: my pid 26827, 161 flutter lines scanned (instrument alive), 0 [FAIL]/[ERR].

### VERDICT ON THE CLAIM
NEARS-963's "a Semantics(button,label) around a small undecorated icon-sized InkWell can NEVER
project its label on Android" is **REFUTED** on clean evidence, twice independently:
(1) the AC2 experiment's four 32dp bare stars, and (2) the baseline's own 28dp navy-header
Back button. Both outcomes were pre-declared and could have come out the other way.

### Secondary observation (b) — store-side sheet
STATICALLY confirmed: store_filter_bottom_sheet_widget.dart carries the same NEARS-964 44dp
decorated shape with an `NIcon('star', filled:, px:32)` leaf instead of a raw Icon.
LIVE: **NOT OBSERVED** — nav drifted back to the search tab and this is not an AC, so I stopped
rather than infer. Stated as unobserved.
