# NEARS-2059 — static + widget-test analysis (pre-live)

Base `fa3a77ca` on `feat/userapp-reskin2`. Worktree
`nears-NEARS-2059-storereg-overflow-recon`. **Zero product code changed.**
Flutter SDK `~/Tools/flutter` (pinned 3.41.9).

Probes were throwaway files under `UserApp/test/features/auth/`
(`zz_overflow_probe_test.dart`, `zz_font_control_test.dart`), deleted before
commit. Everything below is reproducible from the recipe in each section.

## 1. The widget-test overflow reproduces today

The shipped test suppresses the error, so it can never show it:
`store_registration_desktop_submit_blocks_test.dart` installs a
`FlutterError.onError` filter that returns early on
`A RenderFlex overflowed`. The probe copied that file and changed **only** the
filter body, from discarding to recording. Mutation confirmed landed (the
collector appears at three sites).

```
PROBE_COUNT: 1
A RenderFlex overflowed by 75 pixels on the right.
```

## 2. The offending Row — named by the framework, not inferred

Captured from `FlutterErrorDetails.toString()`, whose "relevant error-causing
widget" line is the framework's own attribution:

```
Row:file:///…/UserApp/lib/common/widgets/footer_view.dart:198:28
```

**The ticket's "Affected areas" field is wrong.** The Row is in
`common/widgets/footer_view.dart` (the `Expanded(flex: 8)` desktop block);
`store_registration_screen.dart` only embeds it via `webView()` → `FooterView`.
This is NEARS-511's site (511 cites `:190:28` — same column, line has drifted).

## 3. Viewport-invariance — a prediction that held

`Dimensions.webMaxWidth = 1170` caps the footer container, so a wider viewport
cannot relieve the overflow. Predicted in advance, then tested:

| pump geometry (logical dp, dpr 1.0) | overflow |
|---|---|
| 1600 x 1200 | 75 px right |
| 1400 x 1000 | 75 px right |

Identical, as predicted.

## 4. Mechanism of the test/live divergence — the test font

`flutter_test` renders with a uniform-advance (Ahem-style) font: every glyph
occupies ~1.025 em regardless of shape. Measured on the three footer labels
in-app, `perChar/fontSize` = **1.025** for all three (20, 21 and 12 chars at
fontSize 10).

Three similar lowercase strings could match by coincidence, so the control was
chosen to discriminate a proportional font from an em-square one:

| string @ fontSize 10 | width | per char |
|---|---|---|
| `iiiiiiiiii` | 102.5 | 10.25 |
| `WWWWWWWWWW` | 102.5 | 10.25 |
| `..........` | 102.5 | 10.25 |

In any proportional font `W` is many times wider than `i` or `.`. They are
identical, so the font is provably content-blind. Test text renders roughly
**2x** its real-device width. Test content = 1170 + 75 = 1245 px; with real
metrics the same content fits inside the 1170 cap.

**Refuted sub-hypothesis:** raw `.tr` keys are *not* the driver. English values
are the same length or longer — `become_a_delivery_man` (21) →
"Become a Delivery Partner" (25); `help_support` (12) → "Help & Support" (14).
Raw keys slightly *deflate* width. The font is the mechanism.

## 5. Instrument validity — the live zero is a true negative

`docs/qa-evidence/NEARS-1718/…-swallows-framework-errors.log` proves UserApp
debug builds once discarded every framework error: an overflow was painted
(hazard stripes) while `grep -c 'RenderFlex overflowed'` returned 0 in a healthy
121-line logcat window. Under that defect a zero means nothing, so it had to be
ruled out rather than assumed away.

It is fixed at this base:

- NEARS-1860's fix `6eea7d7e` (2026-08-11) **is an ancestor of `fa3a77ca`**
  (`git merge-base --is-ancestor`, rc 0).
- `main.dart:225` installs `handleFlutterFrameworkError` unconditionally;
  `app_logger.dart:140-144` emits
  `[FAIL] framework_error library=… type=… msg="<summary>"`.
- Probe capture of the real overflow's fields:
  `LIBRARY=rendering library TYPE=FlutterError SUMMARY=A RenderFlex overflowed
  by 75 pixels on the right.` — so the emitted `msg="…"` contains
  `overflowed by`.
- `scripts/app-nav/uinav.sh:269` matches on three independent alternatives:
  `[(FAIL|ERR)]`, `overflowed by`, `FlutterError`.
- NEARS-2029's evidence is dated Aug 14, after the Aug 11 fix.

So NEARS-2029's *"0 matches over 483–495 flutter-tag lines scanned"* is a sound
true negative with a stated denominator, and **AC2 is executable at this base**.

## 6. Falsifiable prediction for the live run

At forced ≥1300 dp (1600x1200 dp) in a **debug** build on `fa3a77ca`: zero
RenderFlex overflow at `footer_view.dart`, while an independent positive control
(e.g. the NEARS-1586 narrow-viewport NRating overflow) **must** fire on the same
device, build and session. A zero is reportable only alongside a firing control
and a scanned-line denominator. If the control does not fire, the result is
NOT ASSERTED — never PASS.

## 7. Open items for the owner (not actioned here)

1. NEARS-511's evidence is itself widget-suite-derived, for **both** its sites
   (footer ~75 px, campaign_screen ~72 px). It may rest on this same test-font
   artifact rather than a live defect. That is a claim about another open
   ticket, so it is the owner's call.
2. Any UserApp QA pass **before 2026-08-11** that concluded "no exceptions in
   logcat" was reading the silenced channel (NEARS-1718's own blast-radius
   note). Scope unknown.
3. The desktop arm is gated at `width >= 1300` logical dp and UserApp ships
   `android` + `ios` only — no `web`/desktop platform dir. The Row is
   unreachable on shipped targets, with a very large landscape tablet as the
   one theoretical path.
