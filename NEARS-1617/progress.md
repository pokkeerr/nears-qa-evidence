# NEARS-1617 — live QA progress log (phase [8], fix_cycle 0)

Device `emulator-5556` · physical 1344x2992 px @ density 480 = **448x997 dp** (verified, not assumed).
Build: worktree `/Users/Apple/Projects/nears-NEARS-1617-loyalty-bottom-sheet-dls`, branch
`feat/NEARS-1617-loyalty-bottom-sheet-dls`.

## Build-freshness proof (artifact level)
| signal | value |
|---|---|
| APK | `UserApp/build/app/outputs/flutter-apk/app-debug.apk` |
| mtime | 2026-08-07 03:11:09 |
| sha256 | `aec6c405cd943dbf53c459c9586db1b23ad8b80cbb477cd48bce788e8e00e94d` |
| device `lastUpdateTime` BEFORE | 2026-08-07 02:08:38 |
| device `lastUpdateTime` AFTER | **2026-08-07 03:11:40** (advanced) |
| behavioural discriminator | Arabic close-X moved RIGHT -> **LEFT** (see AC6) = new `PositionedDirectional` code is live |
| flutter SDK | `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 (absolute) |

## AC results
| AC | status | note |
|---|---|---|
| AC1 tokens | PASS | 0 hits post-fix / 4 hits pre-fix (mutation control) |
| AC2 mobile mount | **BLOCKED** | config-gated off (`loyalty_point_exchange_rate = 0`); NOT a pass, NOT a fail |
| AC3 desktop mount | PASS | sheet renders through dialog chrome, no overflow |
| AC4 conversion | PASS | 2 conversions, prediction == actual on all 4 measures |
| AC5 over-balance reject | PASS | unchanged copy, DB unchanged, paired `[ERR]` log |
| AC6 RTL | PASS | mirrored, close-X on end side, numerics LTR |

## Device state restored
`wm density reset` -> `Physical density: 480`, no override line (re-read to confirm). Locale back to English.
