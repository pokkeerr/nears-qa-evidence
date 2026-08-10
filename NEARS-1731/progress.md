# NEARS-1731 — live QA evidence (phase [8], fix cycle 0)

**Verdict: PASS** · device `emulator-5556` (1005 MB free at acquire, 976 MB after) ·
branch `feat/NEARS-1731-video-glyph-contrast` · base `d84d464b` · light mode only (dark deferred).

## Build freshness — two stage, both stages green
| stage | instrument | result |
|---|---|---|
| 1 pre-filter | md5 of the **INSTALLED** `com.izzes.nears` APK, before and after every AC observation | `303570c398d56ae3b28572245e5ec461` — identical at 14:30, 14:38 and after the base-build round trip at 14:45 |
| 2 verdict | **live Dart VM isolate**, `getObject` on the running script `package:sixam_mart/features/chat/widgets/image_file_view_widget.dart` (VM service, device port 36749, isolate `isolates/1267264434871335`) | `Colors.black54` ×3 · `Colors.black12` ×0 · `Colors.white70` ×0 · `NEARS-1731` comment ×1. Source pulled from the isolate is **byte-identical** to the worktree file. Re-run after the drive: unchanged. |
| 3 corroboration | the running build carries this run's `--dart-define=API_HOST=10.0.2.2:8731`; every API call landed on the QA proxy | proxy log |

## QA route (§6 of the solution doc) — **route A, the response-rewrite proxy. Zero DB writes.**
Stdlib Python proxy on `0.0.0.0:8731` in front of the **primary** `Admin/` backend (`127.0.0.1:8000`),
rewriting the NEARS-1719 fixture's extension in the response body. App pointed at it with
`--dart-define=API_HOST=10.0.2.2:8731`. The extension is switchable at runtime through a control
file, so the SAME build and the SAME DB row drives all four `FileTypeHelper` arms.
Proxy killed at teardown; the shared backend was never stopped; **no DML, no seeder, no schema change.**

Independently re-verified in the tree: `FileTypeHelper.isVideo` lists `.webm`, `isImage` lists
`.webp` → **`messages.id 75` renders the IMAGE arm at base.** The dispatch brief's claim that the
NEARS-1719 fixture reaches the video glyph is FALSE, exactly as the solution doc says.

Login `customer@nears.com` (`users.id 6` / `user_infos.id 3`), conversation **47** ("Ahmed Khan").

## Instrument validation (WCAG sampler)
5 published anchors, all exact: 21.00 · 1.00 · 4.54 (`#767676`/white) · 3.03 (`#949494`/white) ·
8.59 (`#0000FF`/white). **5 distinct outputs** — the instrument demonstrably comes out more than one
way. Two further "expected" values I guessed pre-run (navy 15.30, mint 1.42) were **my arithmetic
that was wrong, not the sampler's** (correct: 16.01 and 1.33); they were removed from the pass
criteria rather than back-fitted.

## Predicted vs measured — every figure measured from ACTUAL device pixels
Tile geometry (identical on both builds): scrim `x 999..1148, y 2209..2358` (150×150 px = 50 dp);
play circle `x 1005..1142, y 2215..2352` (138 px = 46 dp), concentric.

| pair | BEFORE (base build, observed) | AFTER (fix build, observed) | packet prediction | Δ |
|---|---|---|---|---|
| **AC1** videocam glyph vs its tile scrim | rgb(245,244,244) / rgb(221,219,218) = **1.257:1** | rgb(255,255,255) / rgb(116,114,114) = **4.781:1** | 4.78:1 | +0.001 |
| **AC2** play_arrow vs play circle | **5.898:1** | **12.410:1** | 5.87 → 12.35 | +0.03 / +0.06 |
| **AC2** play-circle edge vs surrounding scrim | **4.275:1** | **2.596:1** | 4.26 → 2.59 | +0.015 / +0.006 |
| scrim vs page bg `#FCF9F8` | 1.317:1 | 4.563:1 | — | — |
| videocam glyph where the play circle overlays it | 1.191:1 | 2.693:1 | — | — |

My own pre-run prediction was **4.73:1** (I rounded the black54 composite to rgb(116,115,114));
the device produced rgb(116,**114**,114) and **4.781:1**. The packet's rgb(116,114,114) was exact.
Gap explanation: one LSB of rounding in the green channel of the alpha composite, nothing more.

## AC3 — proven by pixel diff, not asserted
Base build (`d84d464b`, md5 `7d4d510928590b17c36e17362f4ba107`) vs fix build, same fixture, same
screen region, one arm at a time via the proxy:

| arm | differing pixels |
|---|---|
| image (`.webp`) | **0 / 504000** |
| pdf (`.pdf`) | **0 / 504000** |
| other (`.zip`) | **0 / 504000** |
| video (`.mp4`) | 20 028 (3.97%), diff bbox exactly the 150×150 scrim, nothing outside it |

## Files
- `ac1-before-after.png` — side-by-side of the video tile, base vs fix (the AC1 `[ui]` compare).
- `ac1-BEFORE-base-video-tile.png` / `ac1-video-tile-raw.png` — the raw full-device shots the
  numbers were sampled from.
- `ac3-arm-{webp,pdf,zip}.png` / `base-arm-{webp,pdf,zip}.png` — the AC3 diff inputs.
- `reg-*.png` — regression sweep.
- `bug-guest-boot-401-error-snackbar.log` — the one pre-existing finding (unrelated to this diff).
