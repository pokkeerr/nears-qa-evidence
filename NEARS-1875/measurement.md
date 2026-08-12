# NEARS-1875 — RTL mirror measurement (pixel, not eye)

Device `emulator-5554`, physical **1344x2992 @ 480** (no `wm` override), top inset 159 px = 53.0 dp.
Build under test: `feat/NEARS-1875-lightbox-close-rtl` @ `afae2239`. Installed APK md5
`3335639585e5d0094c502389bf621fb7` == locally built `UserApp/build/app/outputs/flutter-apk/app-debug.apk`
md5 (identical) — the running build IS the worktree build. Light mode both captures
(`Dark Mode` switch `checked="false"`). Same device, same resolution, same lightbox
(conversation 47, message 75, single attachment, page index 0) in both locales.

## Verdict shape declared BEFORE measuring
- PASS: `MSE(ltr, mirror(rtl))` clearly LOWER than `MSE(ltr, rtl)`.
- FAIL A: the two are comparable -> did not really mirror.
- FAIL B: `MSE(ltr, rtl)` is the LOWER of the two -> did not move at all (pre-fix).

## Results

| Scope | MSE(ltr, rtl) | MSE(ltr, mirror(rtl)) | mirroring helps? |
|---|---:|---:|---|
| Full frame `y[0:2992]` | 93.141 | **75.610** | YES (1.23x) |
| **Close band `y[159:363]` (decisive)** | 257.170 | **0.001** | **YES (463,880x)** |
| Media band `y[363:2920]` (control) | 0.000 | 0.004 | no |

### Full-frame residual is fully accounted for — none of it is layout
| Band | plain | mirrored | rows |
|---|---:|---:|---:|
| status bar `y[0:159]` | 1422.736 | 1422.736 | 159 |
| close `y[159:363]` | 257.170 | 0.001 | 204 |
| media `y[363:2920]` | 0.000 | 0.004 | 2557 |
| gesture bar `y[2920:2992]` | 0.000 | 0.000 | 72 |

`1422.736 * 159 / 2992 = 75.61` = the entire mirrored full-frame residual. The status-bar band
is **horizontally symmetric in the RTL capture** (self-vs-mirror MSE = 0.0), so it contributes
identically to both columns and cancels out of the comparison.

## Instrument validation (a measurement that cannot come out two ways is not evidence)

1. **Synthetic two-way control.** Same `mse.py` pipeline on a marker that moves right->left
   -> `helps = True` (4228.251 vs 82.907). On a marker that stays put -> `helps = False`
   (0.000 vs 4228.251, i.e. FAIL shape B). The instrument produces both verdicts.
2. **Band non-vacuity.** Close band self-vs-mirror MSE = **257.17** (>> 0): the band carries a
   real left-right asymmetric signal, so "mirroring helps" there is meaningful.
3. **Real-frame negative control (same decisive band).** LTR vs a SECOND LTR capture:
   close band plain **0.000** vs mirrored **257.170** -> `helps = False`. FAIL shape B reproduced
   on real frames, on the exact band that decides the ticket.
4. **Locale actually flipped** (not just a re-render): chat AppBar Back `[48,177][192,321]` (LTR)
   -> `[1152,177][1296,321]` (RTL); Settings AppBar Back likewise; attachment tile
   `[864,2209][1149,2494]` -> `[510,2209][795,2494]`.

### The media-band control DID discriminate, but is WEAK on this fixture — stated, not glossed
The seeded attachment (`2026-08-10-nears1719fixture.webp`, 266 bytes) is itself **horizontally
symmetric**: media-region self-vs-mirror MSE = **0.004**. So mirroring the media costs ~nothing and
the media band returns ~0 in BOTH columns. It came out in the intended direction (`helps = False`)
but it cannot strongly discriminate. Controls 1-3 above carry the validity claim.

**Consequence — the spawn's methodology caveat does not apply on this fixture.** The expectation
that `MSE(ltr, mirror(rtl))` would stay clearly nonzero on the full frame *because the photo also
flips* is void here: the photo is symmetric, so it contributes 0.004, not a large residual. The
nonzero full-frame residual comes entirely from the status bar instead.

## Direct bounds observation (corroboration, not the primary oracle)

| Locale | Close control bounds | top | glyph bright-pixel x-range |
|---|---|---|---|
| English (LTR) | `[1200,219][1344,363]` | 219 px = **73 dp** | 1251-1292 |
| Arabic (RTL) | `[0,219][144,363]` | 219 px = **73 dp** | **51-92** |

Exact horizontal mirror within 1 px (`1344-1292 = 52` vs observed `51`). Vertical seat **unchanged**
in both locales -> NEARS-1874's 73 dp offset (20 dp clear of the 53 dp inset) is preserved.
Pre-fix recorded RTL bounds were `[1200,219][1344,363]` (guide addendum, re-confirmed at NEARS-1950
on this same device 2026-08-12) — the control has moved.

**Not clipped (QA-2):** left system inset is 0 (`overrideNonDecorInsets ROTATION_0 = [0,159][0,72]`);
the 144 px tap target spans `x 0..144` fully on-screen and the 42 px glyph starts 51 px (17 dp) in
from the left edge.

## NOT TESTED — unreachable by construction
Conversation 47's only attachment message (`messages.id 75`) carries a **one-element** `file`
array — verified by SELECT, and corroborated live: the RTL and LTR lightbox dumps contain **only**
the Close button and the media pane, **no `previous`/`next` nodes render at all**. There is no
multi-attachment chat fixture anywhere (NEARS-1956, open). So the prev/next arrows and `PageView`
paging are **NOT TESTED — unreachable by construction**, and AC1's clause "mirroring the prev/next
arrows' behaviour on the same screen" is **not live-observable on conversation 47**. The only
coverage of that clause is the widget test
`AC7 — RTL mirroring > the close control sits on the END edge in both directions`
(`UserApp/test/features/chat/attachment_viewer_dls_test.dart`). Not rounded up to a pass.
