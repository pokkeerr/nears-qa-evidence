# NEARS-1732 — live QA progress log

Worktree `/Users/Apple/Projects/nears-NEARS-1732`, branch `feat/NEARS-1732-video-error-state`.
Device `emulator-5562` (lock held, key NEARS-1732). Light mode only (dark deferred).

## Instrument setup (validated before use)

| Instrument | Predicted | Actual |
|---|---|---|
| proxy `GET /broken.mp4` | 404 | 404, 11 bytes |
| proxy `GET /slow.mp4` | 200, 1293015 B, ~6.0 s | 200, 1293015 B, 6.003 s |
| proxy `GET /slow.mp4` w/ `Range: bytes=0-99` | 206, ~6.0 s | 206, 100 B, 6.004 s |
| proxy passthrough `/api/v1/config` | 200 | 200, 9018 B |
| rewrite regex, POSITIVE (fixture URL) | 1 substitution | 1 |
| rewrite regex, NEGATIVE (`other.jpg`) | 0 substitutions, unchanged | 0, unchanged |

mp4 fetched OK (egress present) -> AC3 live half is achievable, not degraded.
ZERO DB writes: only SELECT/DESCRIBE issued against `multi_food_db`.

## Per-AC log

(appended live)
### Build freshness (live-isolate symbol check, NOT a hash)
`getObject(libraries/@... image_preview_widget.dart)` -> classes = `['ChatVideoInitFailure',
'ChatVideoCleanupFailure', '_ImagePreviewWidgetState', 'ImagePreviewWidget']`; state fields =
`['_pageController','_currentIndex','_videoControllers','_chewieControllers','_failedIndexes','_inFlight']`.
Negative control `ChatVideoNotARealClass` absent. Neither sentinel exists on base 5ab0de66 => running build IS the fix.
Route proof: `REWRITE /api/v1/customer/message/details x1 -> http://10.0.2.2:8791/broken.mp4` (18:03:11).
Device clock is 6 s BEHIND host (measured) - all log/proxy times reconciled with that offset.

### AC1 PASS — error state, not an indefinite spinner
Tap attachment (conv 47) -> "Error loading video" + "Retry" + "Close". Proxy served 404 x4
(ExoPlayer's own retry) then the state settled. Shot `ac1-ac2-video-error-state.png`.

### AC2 PASS (legibility) / visual point FAIL (CTA width)
Measured off the PNG: backdrop #000000; glyph + label #FFFFFF (21:1 on black); CTA fill #00FF99
mint, label #00003C. Legibility confirmed, no blend/opacity surprise.
BUT the CTA measures x=0..1078 of 1080 - FULL-BLEED, not a centred pill, despite `fullWidth: false`.
Render tree: NButton's Container = Size(411.4, 44.0) under LOOSE constraints 0<=w<=411.4, while its
inner Row is Size(40.3, 20.0). Cause is `Container(alignment: Alignment.center)` in
`n_button.dart` — the Align expands to the max constraint when `width` is null.

### AC4 PASS — PII-safe sentinel
Exactly ONE line, pid 24106, inside my cleared window:
`[FAIL] endpoint=null http_status=null type=ChatVideoInitFailure msg="chat video init failed (PlatformException)"`
Leak scan over all flutter-tag lines for `broken.mp4|10.0.2.2|nears1719fixture|ExoPlayer|Source error`:
predicted 0, actual 0.

### Q8 confirmed present, NOT logged: "BOTTOM OVERFLOWED BY 22 PIXELS" (NEARS-1829, pre-existing).

### AC3 PASS — a slow but successful load still spins, then PLAYS (positive proof, not "no error")
`/slow.mp4` = 6 s sleep then the real 1,293,015-byte h264 mp4 (Flutter's `bee.mp4`; egress worked,
so AC3's live half is NOT degraded).
- t+2 s and t+4 s: a11y = `Close/Loading` (spinner HELD through the whole delay)
- t+6 s: a11y = `00:00 / 00:04` (Chewie time readout — the media is open and running)
- proxy: `sleep 6.0s -> SERVED 200 bytes=0-1293014/1293015`, then a tail Range request
- **motion measured** (a static first frame or a black box would score ~0): three captures 1 s
  apart differ by 48,498 and 81,115 sampled pixels over the media region; the evidence frame
  carries 94,890 non-dark sampled pixels and shows a real bee.mp4 frame.
- `[FAIL]` count over the whole sequence: predicted 0, actual 0. No error state at any moment.

### Q2 PASS — Retry / the `_inFlight` latch
3 sequential retries -> predicted 3 `[FAIL]`, actual 3; each showed `Loading` then the error state
again; app responsive throughout. Rapid burst of 3 taps -> 1 `[FAIL]`, no stuck spinner.
(Caveat: after tap 1 the CTA is replaced by the spinner, so the burst corroborates the latch
rather than proving it — the unit test remains its primary evidence.)

### Q4 PASS — sticky, measured by ABSENCE of new traffic
Swipe to the image page and back: the error state returns directly (no spinner), and
`/broken.mp4` hits stayed 31 -> 31 and `[FAIL]` stayed 1 -> 1. A silent re-attempt would have
incremented both.

### Q7 PASS — image arm unchanged: page 2 a11y = `Close/Previous` only. No error text, no Retry.

### Q5 PASS — Arabic RTL
`خطأ في تحميل الفيديو` + `أعد المحاولة` render. Bubble/attach row mirror (bubble 171-696 vs
384-909 in LTR). Label bbox 174x44 px, centred at x=540, clearance 32 px top / 41 px bottom
inside the 116 px button band => NOT clipped.

### Q6 PASS — TalkBack role
uiautomator: `class="android.widget.Button" content-desc="أعد المحاولة" clickable="true"
focusable="true"` => announced as a button.

### Pre-existing, NOT this change: the lightbox Close (X) is inert (see bug-lightbox-close-inert.log)
### Pre-existing, NOT logged: NEARS-1829 22 px bottom-overflow banner, present in every shot.
