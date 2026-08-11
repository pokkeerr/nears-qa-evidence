# NEARS-1699 — AC5 on-device measurements

Branch `feat/NEARS-1699-appbar-maxlines`, worktree `nears-NEARS-1699-appbar-maxlines`.
Build: Flutter 3.41.9 (`/Users/Apple/Tools/flutter`), UserApp `com.izzes.nears` 3.8.0, light mode.

## Forced long-title case

`NAppBar(title: …, showBack: true)` with **no subtitle** — the arm this ticket clamps.
Call site: `UserApp/lib/features/profile/screens/setting_page.dart` (Profile → Settings),
title temporarily set to a **real seeded store name** (`stores.id=3632`, 88 chars):

```
Cosco Supermarket ( West Zone Supermarket ) | Lamar Residence - Al Rahah Creek - Al Seef
```

The edit was reverted afterwards; `git diff` is byte-identical to the pre-QA state.

| Device | Physical | Density | Logical | Title node bounds | Height px | Height dp | Lines |
|---|---|---|---|---|---|---|---|
| emulator-5558 (representative) | 1344×2992 | 480 (3.0) | 448×997dp | `[192,213][1200,285]` | 72 | **24.0** | **1** |
| emulator-5562 (stress, narrower) | 1080×2400 | 420 (2.625) | 411×914dp | `[168,183][954,246]`  | 63 | **24.0** | **1** |

`NearsText.subtitle` = 17sp × 1.4118 line-height = **24.0dp per line**. One line exactly, on both.
The full 88-char string is present in the accessibility tree on both devices — the clamp
affects the paint (ellipsis), not the string, so the reading is not vacuous.

App bar is 60dp; the title box sits inside it and inside the horizontal bounds
(5558: right edge 1200 of 1344 px; 5562: 954 of 1080 px). No paint past the bar.

## Baseline (short title, same screen, clean build)

`Settings` → `[592,213][800,285]` = 208×72 px = 69.3×24.0 dp. Unchanged before/after.

## Console

`flutter run` console for both devices: zero `RenderFlex overflowed`, zero
`EXCEPTION CAUGHT`, zero `[FAIL]`/`[ERR]` from the app process during the AC5
navigation and the regression sweep.

## Out-of-scope observation (NEARS-1702, back-arrow tap target)

Measured on 5558: back `Button bounds=[48,177][192,321]` = 144×144 px = **48×48 dp**.
Material's `MaterialTapTargetSize.padded` appears to expand the gesture target even
though `NAppBar` passes `constraints: const BoxConstraints()`. Reported as an
observation for that ticket, not adjudicated here.
