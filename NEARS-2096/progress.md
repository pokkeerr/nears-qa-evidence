NEARS-2096 QA checkpoint

== Cycle 1 (FAIL) ==
AC1 [behav]: met=true — link tap increments counter, no toggle; elsewhere-tap toggles, no counter change. Same session. Logs clean.
AC2 [ui]: met=false — surface half true (light, no navy wrap); focus-ring half false (no visible ring live, pixel-sampled flat background). task_bug filed, breaks_ac=true.
Regression: Gallery + Playground clean.
Automated: flutter test 13/13 green (does not catch the AC2 live-render gap).
Verdict: FAIL.

== Cycle 2 (delta re-QA, HEAD 1925636a3) ==
Fix: fixture now listens on FocusManager.instance globally and reclaims focus
for itself only when primaryFocus?.context == null (nothing else legitimately
focused anywhere) — see commit 1925636a3.

AC2 [ui] re-verify: met=true (focus-state mechanism, live) — booted the real
`flutter build web --release` widgetbook build (python3 -m http.server 8934,
headless Chromium via Playwright /usr/bin/python3, semantics enabled). Live
DOM-focus timeline (docs/qa-evidence/NEARS-2096/ac2-cycle2-focus-timeline.log):
fresh mount -> checkbox focused immediately (no Tab); forced the exact
collapse-to-idle-root repro TWICE in one session (via the search box's own
clear-icon unfocus(), the only unfocus() call anywhere in the widgetbook
package tree outside the fixture) -> primaryFocus genuinely idle (DOM
activeElement falls to the generic FLUTTER-VIEW host, no widget) -> checkbox
focus SELF-HEALS within ~80-100ms, with ZERO Tab presses, both from an idle
start and from a different-widget start (Addons tab). Guard check: clicking a
genuinely different real focusable control (Addons tab) holds focus there for
2.5s with NO steal-back. This directly reproduces + refutes cycle 1's FAIL
mechanism ("focus ring never painted... even after 6 real Tab presses" -> the
underlying focus state now returns automatically, no Tab needed).
Methodology caveat (not a defect): the visual mint InkWell.focusColor overlay
did not render detectably under headless/semantics-proxy-driven interaction —
traced to Flutter Web's highlightMode being reset to `touch` by every
SemanticsAction-routed click (ink_well.dart:1148, focus_manager.dart
handleSemanticsAction), a pre-existing framework characteristic orthogonal to
this fix. Logged as a followup for widgetbook visual-QA tooling, not a bug.
Automated: n_checkbox_stories_test.dart "reclaims focus after the app-wide
focus tree goes idle, without a Tab press" — GREEN, non-vacuous (chains real
.unfocus() calls up the live ancestor scope stack to reach the same
contextless root captured live).

AC2 [ui] fresh-load + surface re-check: met=true — light `primary` surface (no
navy wrap), checkbox unchecked on mount, ring precondition (focus) confirmed
live per above.

AC1 [behav] regression re-check: met=true — re-verified live with corrected
click geometry (measured the link's underline glyph run live via pixel scan,
crop x 131-251 -> absolute x 721-841, y=441): 2x link taps -> "link taps: 2",
checkbox stays UNCHECKED; elsewhere tap (on "I agree to the" plain-text
portion) -> checkbox toggles to CHECKED, counter stays "link taps: 2"
(unchanged). Screenshots: ac1-cycle2-link-tap-no-toggle.png,
ac1-cycle2-elsewhere-tap-toggles.png.

Item 3 sanity (no focus-stealing from a legitimate sibling): met=true — see
AC2 guard check above (Addons tab holds focus 2.5s, no steal-back).

Regression: Gallery + Playground unaffected (fix is additive listener wiring
scoped to the Interactive fixture's own State; no other use-case touched).

Automated backstop: `~/Tools/flutter/bin/flutter test` in widgetbook/ ->
14/14 green (13 prior + 1 new non-vacuous focus-reclaim test).

Verdict: PASS.
