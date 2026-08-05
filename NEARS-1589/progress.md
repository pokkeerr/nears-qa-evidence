# NEARS-1589 — live QA log (phase [8], fix cycle 0)

Device `emulator-5556` (1344x2992 @ density 480 = 448x997 dp), light mode only
(dark deferred). Backend `php artisan serve --port=8000` from the primary tree;
app reaches it at `10.0.2.2:8000`. DB read-only (SELECTs only).

## Build provenance — proven, not inferred

AC2 is "zero visual change", so a stale APK and a correct build look identical.
Provenance was established by hash, and cross-checked behaviourally:

| | value |
|---|---|
| post-change APK built from | `/Users/Apple/Projects/nears-NEARS-1589-ntabbar/UserApp` @ `e9d5e433`, clean tree |
| build command | `/Users/Apple/Tools/flutter/bin/flutter build apk --debug --target-platform android-arm64` (SDK 3.41.9 by absolute path) |
| post APK sha256 | `b58095fb887ce8dc50cebe30bedcb4550d81219b08a2efb9e0475b20fe28d7ef` |
| installed `base.apk` sha256 on device | `b58095fb887ce8dc50cebe30bedcb4550d81219b08a2efb9e0475b20fe28d7ef` — **identical** |
| pre-change APK built from | `/Users/Apple/Projects/nears-1589-prechange/UserApp` @ `ccc43ccf` (temp worktree) |
| pre APK sha256 | `aa58c419020fa6dd986b3ae9da0051b58fdde1952386f3a9bd1adecff1148199` — **differs**, so the swap really changes code |
| installed `base.apk` sha256 when pre was on device | `aa58c419…` — identical to the pre build |

Independent behavioural control that the swap took effect: on the **pre** build the
three tab nodes dump as `android.view.View` with `selected="false"` on all three;
on the **post** build they dump as `android.widget.Button` with `selected="true"`
on the active one. A stale APK could not produce that difference.

Install succeeded on both swaps (`Success`); `/data` free stayed ~1.0 GB
(1,059,216 KB after install, 83% used) — above the 500 MB floor throughout.

## Per-AC results

| AC | verdict | evidence | logs |
|---|---|---|---|
| AC1 pixel-identity | PASS | pre/post band diff = **0 differing px / 215,040**, max channel delta 0, on all 4 states | clean |
| AC2 rewire, no regression | PASS | 3 filters tap, body switches, indicator cross-fade caught mid-flight | clean |
| AC3 host-slot generic | PASS | component imports material + 3 package-internal files only; widgetbook Gallery renders non-order labels | clean |
| AC4 RTL (a)(b)(c) | PASS | EN/AR pair; order reverses; underline under own label; 20/8 inset mirrors to 8/20 | clean |
| AC5 catalog entry | PASS | `catalog.yaml` +NTabBar, `generated_count` 45→46, sidecar + export present | n/a |

## Measurements (density 480 ⇒ 3 px per dp)

LTR, active slot 0, screencap `post-en-all-orders.png`:
`mint_x=(60,423) mint_y=(465,473) height=3.0dp lead_gap=20.0dp trail_gap=8.0dp`
slots `[0,448] [448,896] [896,1344]` — exactly 448 px each (equal-width `Expanded`).

RTL Arabic, active slot 2, `post-ar-rtl-tab1.png`:
`mint_x=(920,1283) height=3.0dp lead_gap=8.0dp trail_gap=20.0dp` — the 20 dp gap
moved to the opposite physical side. The falsifier (a symmetrically centred RTL
render, i.e. `EdgeInsets` substituted for `EdgeInsetsDirectional`) does **not** fire.

Label ink centres sit off-slot-centre by ~17.5 px (5.8 dp) to the **right** in LTR
and by the same magnitude to the **left** in RTL, for every tab — AC4(c).

## Sequence actually driven

1. Guest → Settings → language ar→en; signed in `customer@nears.com` (51 orders).
2. Profile → My Orders. Captured `post-en-all-orders/ongoing/cancelled.png`.
3. Tapped each tab: `selected` moves, order-id set in the body changes each time.
4. Cross-fade sampled by on-device `screencap` bursts: one frame caught slot 0 at
   `(244,242,240)` (fading out of mint) while slot 1 was at `(8,247,151)` (fading
   into mint) simultaneously — a per-tab cross-fade, not an instant swap.
5. Locale → Arabic; captured `post-ar-rtl-tab1.png` + a11y dump.
6. Installed the **pre** APK; repeated 2 + 5 → `pre-*.png`.
7. Restored the post APK (hash re-verified).
8. Logged out → guest profile hides `My Orders` (node count 0).
9. Signed in `qa.singlestore@nears.com` (0 orders) → all three per-tab empty states.
10. `wm size 2600x1400` + `wm density 160` to cross the 1300 dp desktop breakpoint;
    geometry reset to `1344x2992 / 480` afterwards (verified).
