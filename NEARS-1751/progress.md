# NEARS-1751 — QA progress log (live, appended as observed)

Device `emulator-5562` (lock acquired, key NEARS-1751, disk 1681MB free at acquisition).
Fault proxy: `python3 faultproxy1751.py 8107` → upstream `127.0.0.1:8000`. Port 8107 chosen
(8099 belongs to another session's still-running proxy — left untouched).
Device clock runs **47s behind** the host — every host/device timestamp pair below is reconciled
with that offset.

## PIN — PRE-FIX behaviour (build from base `3bf46592`, worktree `nears-NEARS-1751-BASE`)

Freshness (behavioural, session-unique): the running app's traffic arrives on **port 8107**, a port
only *this* run's `--dart-define=API_HOST=10.0.2.2:8107` produces. No foreign APK can fake it.

Fault: `POST /api/v1/auth/login` → `HTTP/1.1 503 ` (EMPTY reason phrase), `application/json`,
body `{"error":"maintenance"}` — matches neither `{errors:[{code:` nor `{message`, so
`api_client.dart:1050` leaves `statusText` = the empty reason phrase.

| run | host time | proxy | app log | user-visible |
|---|---|---|---|---|
| pre-fix #1 | 23:50:53 | INTERCEPT mode=maintain | `[NET] 503` + `[FAIL] ... type=ApiFailure` | **nothing** at +1s, +3s |
| pre-fix #2 | 23:51:56 | INTERCEPT mode=maintain | `[NET] 503` + `[FAIL]` | **nothing** across 8 polls / ~16s, a11y node count constant **24** |
| pre-fix #3 | 23:52:15 (device) | INTERCEPT mode=maintain | `[NET] 503` + `[FAIL]` | screenshot `prefix-silent-failure.png` |

**NEGATIVE CONTROL for the instrument** (this is what makes "no toast" a real observation, not a
blind spot): same build, same proxy, body `{"message":"maintenance"}` → statusText = "maintenance":

| poll | a11y node count | contains "maintenance" |
|---|---|---|
| 1 | **25** | **yes** (the toast) |
| 2..6 | 24 | no (toast already gone) |

So the instrument DOES detect a transient toast (+1 node, string present, vanishes within ~2s),
and the empty-message fault produced no such node on any of 8 polls. The pre-fix failure was
genuinely **user-silent and log-visible**. **ABORT CONDITION NOT TRIGGERED — pin holds.**

## POST-FIX (build `3aa01e19`, worktree `nears-NEARS-1751-signin-view`)

(appended below as observed)
Freshness on the fix build: same behavioural probe (traffic on my private port 8107) **plus** the
panel itself — `Key('sign_in_submit_error')`'s rendered output exists only in this build, and the
base build demonstrably has none (the pin above).

### Negative control FIRST — empty-field submit (the discriminator)
Submit with both fields empty. Result: `hint="Email/Phone\nEnter email address or phone number"`
and `hint="Password\nPlease enter password"` appear on the EditTexts (field validation fired),
**no panel copy anywhere in the dump**, and the proxy intercept count is **unchanged (4 → 4)** —
no request was even made. The validation wall and the API failure stay cleanly separated.
Shot: `negative-control-empty-fields.png`.

### AC1 — panel on the manual submit, and ONE surface only
Fault `maintain`. Panel appears reading **"Sorry, something went wrong"** + **"Try Again"**.

| poll (10, ~20s span) | a11y nodes | nodes containing the copy |
|---|---|---|
| 1..10 | 23 (constant) | **1** (never 2) |

Exactly **one** surface — a panel *and* a toast would have shown 2 copy-bearing nodes, and poll1
fires immediately after the response, inside a toast's 3s life. Logcat: exactly **one** `[FAIL]`
(`endpoint=/api/v1/auth/login http_status=503 type=ApiFailure`), zero `[ERR]`, zero exceptions.
Shot: `ac1-panel-mobile-navy-hero.png`.

### Persistence + Try Again — measured, not eyeballed
`uiautomator dump` **fails closed (0 nodes) while the loading spinner animates**, so a dump-based
"panel absent" during an in-flight request is NO observation. Switched to a pixel probe over the
panel's own a11y bounds (near-white px in `[53,660]-[1028,920]`), with the fault held open 20s:

| poll | device time | near-white px |
|---|---|---|
| 1..13 | 00:02:21 → 00:02:40 (in flight) | **111,092** (panel gone — the cream email field has moved up into the region) |
| 14 | 00:02:42 (after the 503) | **12,721** — the exact panel-present calibration value |

Request 00:02:21.121 → response 00:02:41.596. So Try Again **re-fires the request** (new `[NET]`
POST + new `[FAIL]`), the panel **clears the moment it is tapped**, and it **re-raises** only
because the retry also failed. Persistence: >20s in the earlier run (a toast is 3s).
Shot: `ac1-retry-inflight-panel-cleared.png`.

### Companion fault — real backend copy survives verbatim
Body `{"message":"maintenance"}` → panel reads **`maintenance`** (`content-desc="maintenance"`),
generic copy count 0, across 3 polls. Not flattened into the fallback.

### Recovery actually recovers
Proxy back to `forward`, tap Try Again → `[NET] /api/v1/auth/login http_status=200`, panel gone,
app lands on the logged-in Profile screen. Zero `[FAIL]`/`[ERR]`.

### AC3 — loading state, demonstrated live (same artifact)
`ac1-retry-inflight-panel-cleared.png` shows the mint Sign In CTA rendering a **spinner arc in
place of its label** during the held-open request, with the panel gone and no toast. One artifact,
three facts. (Corroborating: `uiautomator dump` returns 0 nodes for the whole in-flight window and
succeeds either side of it — a continuously animating indicator is the only thing on that screen
that does this.)

### AC5 (panel-scoped) — RTL + tap target, measured
| check | LTR | RTL (ar) | verdict |
|---|---|---|---|
| message text node bounds | `[171,695][983,753]` | `[97,643][909,706]` | mirror image — icon→text order flips |
| warning glyph (salmon `errorDark` px) | **453** on the LEFT, 0 right | **456** on the RIGHT, 0 left | same glyph, position mirrored |
| retry button height | 116px @420dpi = **44.2dp** | 116px = **44.2dp** | ≥44dp, not clipped |
| accessible names | `Sorry, something went wrong` / `Try Again` | `عذرًا، حدث خطأ ما` / `حاول ثانية` | non-empty in both locales |

`mirrorForRtl: false` on the glyph is set in code; the warning triangle is vertically symmetric, so
mirroring is **visually non-discriminating** — stated rather than claimed as verified.
Shot: `ac5-panel-rtl-arabic.png`.

### The two colour branches — measured against the token values, not eyeballed
| host | fill | glyph/text | border | navy `#000080` |
|---|---|---|---|---|
| mobile navy hero (`sign_in_screen:236`) | `#1F1F6B..73` = white@12% over navy (`navyGlass`) | `errorDark #FFB4AB` 378px + white text 12,017px | navyGlassLine | n/a (is the hero) |
| desktop card (`sign_in_screen:550`) | `errorSurface #FFDAD6` **41,275px** | `onErrorSurface #93000A` 1,250px | `error #BA1A1A` 604px | **0 px** |
| `AuthDialogWidget` (desktop) | `errorSurface #FFDAD6` **44,336px** | `onErrorSurface #93000A` 1,495px | `error #BA1A1A` 549px | **0 px** |

`errorSurface`/`onErrorSurface`/`error` measure **0 px** on the navy hero, and `errorDark`/navy
measure **0 px** on both pale hosts. The branches are correct and mutually exclusive. No navy panel
on a white card. Shots: `ac1-panel-desktop-card-pale.png`, `ac1-panel-authdialog-desktop.png`.

### AuthDialogWidget reachability — a correction to the packet
All six hosts gate the dialog behind `isDesktop` (`not_logged_in_screen:26-29`,
`menu_drawer:150-151`, `order_successful_screen:246`, `digital_payment_failed_screen:205-211`,
`new_pass_screen:418-428`, `sign_up_widget:728-732`). So AuthDialogWidget-on-mobile is **not
reachable by navigation** — I could only produce it by resizing the window with the dialog already
open. In that state the panel is **white on white**: the message-text node has **0 pixels darker
than 200** across 44,080px (the same node on the desktop dialog has 461). Recorded as a followup
per the packet's standing ruling, not as a task bug, and it does not move the verdict.
Shot: `bug-authdialog-mobile-white-on-white.png`.

### Regression sweep (bounded)
Home, Basket, Categories after a successful login: all render, `ui_errors` **0 matches over 43
flutter-tag lines scanned** (instrument reported its own validity). Sign-in screen itself re-driven
in both locales and both widths without a red screen or an overflow.

### Automated backstop
`flutter test test/features/auth/` → **172 passed**.
`flutter test` (whole UserApp) → **3403 passed, 2 skipped, 6 failed**, all six in
`test/golden/dls_golden_test.dart`. Run in isolation the same file fails **identically on base
`3bf46592`** (`-2` both trees): `RenderFlex children have non-zero flex but incoming height
constraints are unbounded` inside the golden harness. **Pre-existing — not this change.** No
goldens were regenerated.

### OTP arm
Live-confirmed environment-blocked: the sign-in screen renders only the manual form (Email/Phone,
Password, Remember me, Sign In, Forgot Password, Create Account, Continue as Guest) — there is no
OTP toggle to drive. Not a defect.

---

## DELTA RE-QA — tip `5a25466a` (was `3aa01e19`), one question only

`onNavyHero` now arrives by declaration (`sign_in_screen.dart:241` passes `true`; the desktop card
at `:551` and `AuthDialogWidget` take the `false` default) instead of being inferred from
`!ResponsiveHelper.isDesktop(context)`. The only risk this carries is a **light panel on navy**.

Same device (`emulator-5562`), same geometry (1080x2400 @420dpi), same fault (`503` empty reason
phrase + `{"error":"maintenance"}` on port 8107), same crop boxes — so the two runs are directly
comparable.

| measure | `3aa01e19` | `5a25466a` |
|---|---|---|
| message-text a11y bounds | `[171,695][983,753]` | `[171,695][983,753]` |
| Try Again a11y bounds | `[97,784][983,900]` | `[97,784][983,900]` |
| a11y node count | 23 | 23 |
| dominant fill (navyGlass over navy) | `#1F1F6B` x39,432 · `#1F1F72` x37,343 · `#1F1F70` x20,160 | **identical** |
| `errorDark #FFB4AB` (glyph) | 378 px | **378 px** |
| `textOnNavy #FFFFFF` | 12,017 px | **12,017 px** |
| `errorSurface #FFDAD6` | 0 px | **0 px** |
| `onErrorSurface #93000A` | 0 px | **0 px** |
| `error #BA1A1A` | 0 px | **0 px** |
| near-white in the persistence box | 12,721 | **12,721** |

**Pixel diff of the panel region between the two builds: 0 differing px out of 253,500.**
Byte-for-byte identical. The palette moved from inference to declaration with no change to the
rendered result. Logs clean: exactly one `[FAIL] endpoint=/api/v1/auth/login http_status=503
type=ApiFailure`, zero `[ERR]`. Shot: `delta-5a25466a-panel-mobile-navy-hero.png`.

The `AuthDialogWidget`-at-mobile case was **not** re-attempted, per instruction — it is unreachable
by navigation and is recorded as a resize/foldable-shaped followup.
