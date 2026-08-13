# NEARS-1688 QA progress (live checkpoints)

Device: emulator-5564 (booted by QA; pool 5554/5556/5558/5562 all held by live peers)
Geometry: 1344x2992 @ 480dpi = 448x997dp (pool standard, already overridden)
Build: installed 2026-08-13 20:10:53 from /Users/Apple/Projects/nears-NEARS-1688-compose-unavailable-state
Flutter: 3.41.9 (pinned absolute path)
Locale start: light mode only (dark deferred)

## DRIFT vs spawn prompt (measured, read-only SQL)
- `conversations.sender_id` is a **user_infos.id**, NOT a users.id.
- user_infos.id=3 -> users.id=6 (customer@nears.com "Customer Nears") owns conv 45-58.
- users.id=3 (Michael Brown) = user_infos.id 110, owns ONLY conv 44 (admin). Logging in as
  users.id=3 shows a single admin row - no vendor threads at all. Verified live.
- user 6 HAS in-flight orders -> conv 46/47/49/50/54 are status:TRUE (composer), NOT gated.
- Gated (status:false, >=1 msg): conv 48 "Sara Ali", 51 "Organic Shop", 52/53/55/56/57/58.
- => a LIVE vendor status:true thread IS reachable (conv 46 Demo Store), so AC3 need not be
  admin-only + widget-test. Upgrade over the spawn prompt's stated maximum.

## Automated backstop
flutter test (worktree UserApp): 3597 pass / 2 skip / 4 [E] == BASELINE exactly.
[E] set: coupon_controller_test x3 + category_screen_back_button_test x1. Zero chat failures.

## AC checkpoints

### AC1 — gated thread shows a visible notice, not a blank gap / not a disabled field  PASS
Conv 48 "Sara Ali" (status:false, 1 msg) AND conv 51 "Organic Shop" - both render
"Place an order to start messaging". Accessibility dump on the chat screen: **0 EditText
nodes**, **0 "Type here....."** -> not a bare disabled text field; text present -> not a blank
gap. Only clickable on screen = the Back button. Logs clean (0 [FAIL]/[ERR] at that point).
Shot: ac1-en-gated-notice-conv48.png

### AC2 — copy communicates unavailability + what restores it, all 4 locales  PASS
Live, one gated thread per locale, rendered string compared byte-for-byte to the shipped JSON:
  en "Place an order to start messaging"   exact
  ar "ضع طلباً لبدء المراسلة"                exact, RTL
  es "Realiza un pedido para chatear"       exact
  bn "চ্যাট করতে একটি অর্ডার দিন"              exact
Raw key `messaging_unavailable` never rendered; no English fallback in any non-English locale.
RTL proven by bounds mirror, not by eye: the 78px lock-icon block moves side to side —
LTR text [108..1314] (icon left), RTL text [30..1236] (icon right); 108-30 == 1314-1236 == 78.
Shots: ac2-ar-rtl-notice.png, ac2-es-notice.png, ac2-bn-notice.png

### AC3 — working path still renders the normal composer  PASS (UPGRADED)
Spawn prompt expected admin-only + widget-test for vendor. Measured otherwise:
 - conv 46 "Demo Store" — a LIVE VENDOR thread, status:true (user 6 has a pending order on
   store 1, the vendor's stores[0]). Composer complete: Add Image button, EditText 933px,
   48dp send circle. Notice absent (0 hits). No DB write needed.
 - conv 45 admin — composer likewise complete.
Shots: ac3-en-open-composer-vendor-conv46.png, ac3-en-admin-conv45-composer.png

### AC4 — mutation-provable test  PASS (backstop)
Full suite re-run == baseline exactly (see above). 48 chat_null_field_degrade_test lines, 0 in
the failure set. Notice tests T20/T21/T23/T24/T25/T26/T27 + the 4-locale test all green.

### HIGHEST-RISK — loading arm (messageModel == null) must stay EMPTY  PASS
Reached honestly: list loaded online -> network cut (svc wifi/data disable, "Active default
network: none") -> opened gated conv 51.
POSITIVE CONTROL (so the negative is not vacuous): the chat screen really was open — header
placeholder "Receiver's name", body "Something went wrong / Please check your connection and
try again / Retry".
8 total samples in the null state: **notice=0, EditText=0** — slot completely empty, no notice,
no flash. Then Retry with network restored -> model resolves status:false -> notice appears.
That transition is the cleanest possible proof the two arms are distinct.
The offline error path DOES emit its paired PII-safe failure log (logging contract satisfied):
  [FAIL] endpoint=/api/v1/customer/message/details http_status=null type=ApiFailure
         msg="chat: message thread fetch failed"
Shot: loading-arm-null-model-slot-empty.png

### No-flash, online direction  PASS
8 rapid samples on an online open of a gated thread: notice present from sample 1, EditText 0
throughout. Switching admin(open) -> Sara Ali(gated) drops the previous composer immediately,
so neither direction leaks the other arm's chrome. Structurally guaranteed too:
getMessages(firstLoad:true) nulls _messageModel, and the notice requires model != null.

### Notice is not interactive  PASS
Node: class=android.view.View, clickable=false, long-clickable=false.
Tapped it by label: keyboard mInputShown=false before AND after, screen unchanged, no new logs.

### TalkBack  PASS (verified on the node TalkBack consumes)
class=android.view.View (NOT Button, NOT EditText), content-desc = the full localised sentence,
clickable=false + long-clickable=false (so no "double-tap to activate"), focusable=true (so it
IS reached in linear navigation, not skipped), checkable/password false, not editable.
=> announced as coherent text, not as a control.

### 1.3x text scale, ar + bn  PASS
font_scale 1.3 confirmed APPLIED before measuring (the guide's Trap-1 positive control):
notice height bn 57->75px, ar 60->78px (~1.32x). Rendered string still byte-exact vs JSON,
**no ellipsis, single line, inside the container** in both. RTL mirror held at 1.3x.
Shots: ac2-bn-notice-textscale-1.3.png, ac2-ar-rtl-notice-textscale-1.3.png

### Gate-true regression — attach preview strip  PASS
Attached an image on open conv 46: preview strip renders [30,2518][1314,2818] with the
thumbnail ImageView + Remove affordance, composer intact below. Not sent (no DB write).
Shot: regression-attach-preview-strip-intact.png

### Regression sweep (bounded) — clean
conversation list, gated chat (x2 threads), open vendor chat, admin chat, profile, settings +
language switching (x6 switches), module home smoke. No new [FAIL]/[ERR]: total stayed 22, all
22 traceable to my own deliberate network cut (every one transport/socket), all PII-safe.

### task_bug — shipped icon 'lock' vs [7d]-adjudicated 'info'
chat_screen.dart:1674 renders NIcon('lock') at HEAD 82f8e749 (committed 19:53:42).
docs/design/NEARS-1688-chat-compose-unavailable-notice.md (mtime 20:07:17, UNCOMMITTED) records a
[7d] ux-review ruling that the icon must be 'info' — a padlock asserts a permission state, and on
a compose row reads as "conversation locked/muted" (moderation), the exact false read this ticket
exists to prevent. Ruling never reached the code. All 10 QA shots show the padlock and would need
re-shooting. breaks_ac:false (AC1-4 functionally met) -> verdict stays PASS, routed to engineer.
Artifact: bug-icon-lock-vs-reviewed-info.log

### FINAL: PASS on AC1-AC4. 1 task_bug (icon, non-AC-breaking), 1 regression_bug (pre-existing
attachment leak). Device lock released; emulator-5564 left running; font_scale restored 1.0.

## ===== DELTA RE-QA — fix cycle 1, HEAD 501a57f5 (was 82f8e749) =====
Rebuilt + reinstalled from the worktree: lastUpdateTime 20:10:53 -> **20:58:59** (newer, so not a
stale APK). Code delta verified as exactly 1 insertion / 1 deletion: NIcon('lock') -> NIcon('info')
at chat_screen.dart:1673; px/color/mirrorForRtl untouched. 'info': Symbols.info confirmed at
n_icon.dart:215, same map as 'lock' at :196.

GLYPH — hard measurement, not eyeballed. Live render tree off the running isolate:
  U+E88E (Symbols.info) present, count = 1
  U+E899 (Symbols.lock) present = FALSE, count = 0
  painting node: family packages/material_symbols_icons/MaterialSymbolsOutlined, size 18.0,
  color RGB(0.4157,0.4157,0.4706) = textMuted  -> px and colour provably unchanged.
BOTH ARMS by construction: _ComposeUnavailableNotice builds `row` (containing the single NIcon)
ONCE and both the isDesktop and mobile return paths embed that same row — one glyph site, so the
desktop arm cannot differ. Desktop not separately bootable on a phone emulator; stated as a
code-structure guarantee, not a live desktop demo.

RTL MIRROR re-measured with the new glyph (measured, not assumed):
  LTR(en) [108,2908][1314,2962]   RTL(ar) [30,2902][1236,2962]
  108-30 = 78  and  1314-1236 = 78  -> MATCH. Byte-identical to the padlock run; the number did
  not move, which is the expected result since px:18 is unchanged.

RE-SHOT (padlock versions overwritten in place, nothing stale left alongside):
  ac1-en-gated-notice-conv48.png, ac2-ar-rtl-notice.png, ac2-ar-rtl-notice-textscale-1.3.png,
  ac2-es-notice.png, ac2-bn-notice.png, ac2-bn-notice-textscale-1.3.png
  The other 5 artifacts show NO notice (empty loading slot / open composer / attach strip) and
  remain current and correct.

1.3x TEXT SCALE with the new glyph (scale confirmed applied before measuring):
  ar 60 -> 78px (1.30x), exact vs ar.json, no ellipsis, mirror still 78/78
  bn 57 -> 75px (1.32x), exact vs bn.json, no ellipsis
  Both byte-identical to the padlock run -> the swap changed no layout. Scale restored to 1.0.

TONE (the new qa_point): PASS in my judgement. The rendered glyph is an outline circled lowercase
"i" in textMuted at the same optical weight as the sentence. It carries no permission or
restriction semantics, and specifically does NOT read as "conversation locked/muted/archived" —
the false moderation reading the padlock was ruled to carry. Outline-only and untinted (no red or
amber, no fill), so it also does not read as an error or warning; it sits as a quiet annotation on
the sentence rather than a status badge. Honest limitation: `info` is generic — it does not itself
say "you need an order"; the sentence carries that. That trade was explicitly accepted at review.

TEST-OUTPUT [FAIL] LINES — measured from my own cycle-0 suite log, not relayed: 394 [FAIL] lines
appear in the raw output. They are AppLogger emissions from tests that DELIBERATELY exercise
failure paths (19x "chat: message thread fetch failed", 19x "chat: conversation list fetch
failed", 25x "api request threw", plus profile/coupon/wallet degrade tests). NONE coincides with
the 4 real [E] failures (coupon x3, category x1). [FAIL] in test stdout is instrumentation, not a
failure signal — the only failure signal is [E], which is 4 = baseline.

NOT re-run, per scope and because the glyph cannot reach them: loading arm, gate-true attach
regression, non-interactivity, TalkBack semantics class, locale copy strings, full suite.
Cycle-0 results for those stand.

DELTA VERDICT: PASS.
