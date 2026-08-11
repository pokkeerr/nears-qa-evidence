# NEARS-1952 — live QA evidence (phase [8], fix cycle 1)

- Device: `emulator-5562` · **live geometry `Override size 1344x2992` @ `Override density 480`** (physical 1080x2400 @420 is overridden and NOT live) → **scale 3.0**, so 44dp = 132px, 45dp = 135px.
- Build: worktree `/Users/Apple/Projects/nears-NEARS-1952-map-expand-a11y` @ `e4d28998`, Flutter `/Users/Apple/Tools/flutter` 3.41.9.
- Installed APK md5 `8562bc0cfd9acb8ed451b41f3db63696` (== host `build/app/outputs/flutter-apk/app-debug.apk`), identical before and after every AC observation.
- Live-isolate probe (VM service, loaded kernel source of the running isolate, both `main` isolates): `view_fullscreen_map`=1, `minHeight: 44`=3, `top: 43`=1, **`top: 50`=0** → POST-FIX. Run immediately before driving and again after all ACs.
- Surface confirmed as the **`fromView: true` embedded map**: zone dropdown `Select Zone` at `[75,994][1269,1138]` + address `EditText` at `[75,1213][1269,1417]` above a bounded `Google Map` TextureView `[78,1495][1266,2539]` = 396x348dp. Not the fullscreen map.

## AC1 — non-empty content-desc — PASS
Third of three consecutive `uiautomator dump`s (first discarded per NEARS-1727 discipline); dumps B and C byte-identical.

```
<node index="5" text="" resource-id="" class="android.widget.Button" package="com.izzes.nears" content-desc="View fullscreen map" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[1131,1624][1266,1756]" drawing-order="0" hint="" />
```

Required-positive control, SAME class (`android.widget.Button`), SAME dump:

```
<node index="7" text="" resource-id="" class="android.widget.Button" package="com.izzes.nears" content-desc="Use my current location" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[1131,1765][1266,1855]" drawing-order="0" hint="" />
```

Documented pre-fix baseline (dump `zoneset-d2.xml`, emulator-5554, build md5 `4cbaef2e42d553c1711be0b1a56b59d8`, 2026-08-11) was `class="android.view.View" content-desc="" bounds="[1131,2221][1266,2311]"`.

## AC3 — >=44dp both axes — PASS
`[1131,1624][1266,1756]` → 135 x 132 px. At the live density 480 (scale 3.0): **45.00 x 44.00 dp**. Both axes >= 44dp.

## No-op check (circle must not move) — PASS
Circle centre measured relative to the positive control, which is invariant to scroll position:
- pre-fix: node centre y 2266, control centre y 2386 → delta **-120px (-40dp)**
- post-fix: node centre y 1690, control centre y 1810 → delta **-120px (-40dp)** — identical.
Screenshot `ac1-ac3-node-bounds-annotated.png` (red = node bounds, magenta = node centre y 1690) shows the white circle bisected by the centre line and unchanged in size. Gap to the control below = 1765-1756 = 9px = **3dp**, no overlap.

## AC2 — tap still navigates — PASS (mobile push arm; desktop arm inspection-only)
- (a) no zone selected → `Please select Zone` snackbar, **no navigation** (`ac2a-please-select-zone-snackbar.png`).
- (b) zone `Abu Dhabi Zone` selected → **top-edge tap (1198,1630)** opens the fullscreen map, app bar `Set Your Store Location`, `Back` returns to the embedded map (`ac2b-fullscreen-map-topedge-tap.png`).
- (b) **bottom-edge tap (1198,1750)** likewise opens the fullscreen map (`ac2b-fullscreen-map-botedge-tap.png`) — the whole 44dp box is live, not just the visible circle.
- neighbour non-regression: tapping the current-location control's own top edge (1198,1771) ran **its** action (address became `R989+PPW, Dhaka 1216, Bangladesh`, zone resolved to `Main Service Zone`), never the expand.
- (c) desktop `showGeneralDialog` arm: **code inspection only** — this pool is Android emulators, `ResponsiveHelper.isDesktop(context)` is false, that branch never executed. Not claimed as live-verified.

## RTL / Arabic — PASS
App language switched to عربى. Node announces `content-desc="عرض الخريطة بملء الشاشة"`, `bounds="[1131,1651][1266,1783]"` = 45.00x44.00dp; positive control `content-desc="استخدم موقعي الحالي"` `[1131,1792][1266,1882]`. Gap still 9px = 3dp, no collision. Screenshot `ac1-rtl-arabic-embedded-map.png`. Language restored to English afterwards.

## Logs
`ui_errors` **exit 0**, "scanned 208 flutter-tag lines of 166994 buffer lines; 4 match(es)". All 4 are `[ERR] msg="error snackbar shown"` from **pid 19902 (this run's app)** at 03:40:18 / 03:40:37 / 03:41:03 / 03:43:46, inside the run window — they are the paired `AppLogger.error` for the four `please_select_zone` snackbars deliberately triggered, stack `select_location_view_widget.dart:426:21 -> showCustomSnackBar -> _InkResponseState.handleTap`. That is the logging contract being *satisfied* (toast + paired log), not a defect. No `[FAIL]`, no unhandled exception, no RenderFlex overflow, no red screen.

## Automated backstop
`flutter test test/features/auth/select_location_fullscreen_control_a11y_test.dart` → **3/3 passed**.
