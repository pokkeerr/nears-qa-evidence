# NEARS-1638 — F1 decisive check: **OUTCOME A**

Pre-registered prediction (written before any device measurement):
`prediction-preregistered.md` in this directory — predicted Outcome A. **Confirmed.**

Device: **emulator-5558** (NOT 5560 — the broken-bridge device that produced ALL of the
NEARS-963 evidence). Build: `feat/NEARS-1638-info-a11y` @ `086defa3`, installed APK md5
`aa44287eb74b8dcb31958cb90d39085f`, app pid 31139.

## The raw dump line (verbatim, `uiautomator dump`, taken AFTER navigation)

```xml
<node index="2" text="" resource-id="" class="android.widget.Button" package="com.izzes.nears"
 content-desc="Info" checkable="false" checked="false" clickable="true" enabled="true"
 focusable="true" focused="false" scrollable="false" long-clickable="false" password="false"
 selected="false" bounds="[1224,159][1296,339]" drawing-order="0" hint="" />
```

`content-desc="Info"` — **non-empty**, role `android.widget.Button`, `clickable="true"`,
`focusable="true"`.

## Validity control (SAME dump) — the instrument can see a label

```xml
<node index="0" ... class="android.widget.Button" content-desc="Back" clickable="true"
 bounds="[48,177][192,321]" />
```

Back reads `"Back"`. The dump is therefore measuring what we think it is measuring; an empty
Info result would have been meaningful. **The measurement could come out two ways.**

## No absorption (P4)

```xml
<node index="1" ... class="android.view.View" content-desc="Refer &amp; Earn" clickable="false"
 bounds="[551,213][865,285]" />
```

The title still announces as its own node. The new label swallowed nothing.

## Why this NARROWS the NEARS-963 lesson

The ledger rule `a11y-icon-label-needs-larger-decorated-tap-box-android` (severity high,
`seen: 1`, `first_seen: NEARS-963`) asserts that on Android a `Semantics(button,label)` over an
`InkWell` whose child is a **small, undecorated, icon-sized box** does **not** project its label
to the AccessibilityNodeInfo tree, and that this makes a zero-visual-change a11y labelling of
tiny bare-icon tap targets **"IMPOSSIBLE on Android"**.

This call site is that exact shape, with nothing added to make it easier:
- `NInkWell.padding` defaults to `EdgeInsets.zero` (`packages/nears_dls/lib/elements/inkwell/n_ink_well.dart`, field declaration)
- `Material(color: Colors.transparent)` — no `BoxDecoration` anywhere
- child is `Center -> NIcon('info')`, and the resulting node measures **72 x 180 px**
  (`bounds="[1224,159][1296,339]"`) — 72 px wide is the bare icon box, un-enlarged
- no `MergeSemantics`, no `container: true`, no `SizedBox` — the diff is literally
  `semanticLabel: 'info'.tr` and nothing else (+3 lines, comment included)

It projected anyway, first try, reproducibly. **The rule as written is refuted at its own shape.**

## Robustness of the refutation

Reproduced across **5 independent `uiautomator dump`s in 3 app configurations**, all with a
passing Back-button validity control in the same dump:

| Configuration | Info `content-desc` | Bounds | Back control |
|---|---|---|---|
| en, logged in (dump 2) | `Info` | `[1224,159][1296,339]` | `Back` |
| en, logged in (dump 3, independent) | `Info` | `[1224,159][1296,339]` | `Back` |
| en, logged in, post-dismiss | `Info` | `[1224,159][1296,339]` | `Back` |
| **ar, RTL** | `معلومات` | `[48,159][120,339]` | `رجوع` |
| en, **logged out** | `Info` | `[1224,159][1296,339]` | `Back` |

## The confound that most likely produced the original lesson

Every device observation behind NEARS-963 was taken on **emulator-5560**, whose uiautomator
bridge is broken on every screen (NEARS-1727) and which the workflow profile excludes from the
usable pool. A broken bridge and a missing label present identically in a dump — which is
exactly why NEARS-963's own validity was never establishable.

One further mechanism observed live in THIS run and worth recording: the **first**
`uiautomator dump` issued against a freshly-navigated Flutter screen did not produce a pullable
file at all (`dump_1.xml` was absent; `dump_2.xml` one second later was complete). Flutter only
builds its semantics tree once an accessibility client attaches, so a single first-dump against a
Flutter screen can legitimately come back empty **while the label is present**. A methodology
that dumps once and concludes "no label" is not sound on Flutter.

**Recommendation (conductor's/owner's call, not QA's):** re-open
`a11y-icon-label-needs-larger-decorated-tap-box-android` and narrow or retire it. Its
"IMPOSSIBLE on Android" clause is false as stated, and while it stands it will keep pushing
tickets toward unnecessary visual changes to tap targets. Note this run does NOT re-test
NEARS-963's own two widgets (rating stars, map zoom) — those remain unmeasured on a good device.
