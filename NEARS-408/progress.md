# NEARS-408 QA progress (live)
Build: branch feat/NEARS-408-settings-notifications-reskin @ 0c6c4e7e
Device: emulator-5554 (Android). Backend: http://10.0.2.2:8000 (local, HTTP 302 OK).
Account: customer@nears.com (zone 2). Light mode start.

## AC checkpoints (appended live as observed)

- ORIGINAL notification state = ON (mint switch). MUST restore to ON at end.
- S-01 PASS: navy appbar, white "Settings" centered, white back arrow, no extra icons. [S-01-settings-light.png]
- S-02 PASS: "SYSTEM APPEARANCE" muted caps eyebrow above white 16px-radius elevated card.
- S-03 PASS: Dark Mode row mint-tile crescent navy glyph + Switch OFF (light).
- S-06 PASS: Language row mint-tile globe + "English" muted + chevron.
- S-09/S-10 PASS: COMMUNICATIONS eyebrow + Notification row mint-tile bell + Switch ON.
- S-13 PASS: Version: 3.8 centered muted footer.
- S-14 PASS: no Profile hero / Sign Out / Preferences / bottom nav (a11y tree + visual).
- S-15 PASS: cards ambient shadow only, no hard border.

- S-04 CRITICAL PASS: tapping Dark Mode row flips WHOLE app theme live (settings card+bg, Profile menu, Home appbar/surfaces all dark; switches stay mint). [S-04-settings-dark, S-04b-profile-menu-dark, S-04c-home-dark]
- S-05 CRITICAL PASS: dark mode persists across hot-restart (home + reopened settings still dark, switch ON). [S-05-home-dark-after-restart, S-05b-settings-dark-after-restart]
- N-14 settings PASS: dark legible; mint dark-mode + notification switches stay mint.
- REG-06 (home appbar no showBack, dark): location selector + bell+mint-dot + cart badge unchanged, no back arrow. [S-04c-home-dark]

- S-11 CRITICAL PASS: Notification row tap -> NotificationStatusChangeBottomSheet "Are you sure / disable notification" Yes/No; Yes flips switch OFF. Confirm-gate intact. [S-11-notif-confirm-sheet-dark, S-11b-notif-off-dark]
- NEARS-428 observed: "Yes" button salmon/pink in dark mode (pre-existing debt, NOT failed).
- S-12 PASS: notif OFF persists across hot-restart [S-12-notif-off-after-restart]; sheet copy is state-aware ("enable" when OFF).
- RESTORE: notification toggled back ON (original state) [S-12b-notif-restored-on].

- N-01 PASS (dark): navy appbar, white "Notification" title, white back arrow, NO more_vert. [N-01-notifications-dark]
- N-03 PASS: date headers Yesterday/13 Jun/10 Jun/04 Jun 2026 each once, descending; grouping correct.
- N-04 PASS: unread cards = mint dot at title start + bold title + ambient shadow.
- N-07 PASS: order_status type = green check_circle in green-surface circle (FILL). Cancellations show green check (known deferred backend-contract gap; NOT failed).
- N-14 PASS (notif dark): legible, cards dark surface, mint dots stay mint, green semantic circles conventional.
- N-16 PASS: no bottom nav on notifications.
- No runtime errors (Dart MCP get_runtime_errors clean) on settings or notifications.

- N-06 PASS: card tap opens NotificationBottomSheet (navy sheet, title+body+close X). [N-06-notif-detail-sheet-dark]
- N-05 PASS: tapped card becomes seen (dimmed grey circle, muted title, no dot, no shadow) — persists in session.
- N-11/N-17 PASS: pull-to-refresh shows mint spinner; logs confirm GET /api/v1/customer/notifications [200] reload. [N-17-refresh-spinner-dark]
- N-07 data note: this account's notifications are ALL type=order_status (logs). No push_notification type present -> N-08 push-image thumbnail not exercisable live (unverifiable via this data).

- S-04 reversibility PASS: dark toggled back OFF -> light restored. [S-04d-restored-light]
- S-07 PASS: Language row opens LanguageBottomSheetWidget modal (not page push); EN/AR/ES/BN + Update. [S-07-language-picker]
- S-08 + N-13(settings) PASS: Arabic switches locale to RTL; back arrow + chevron mirror to logical end, icon tiles at logical start (right), switches at logical end (left), value pill+chevron logical end, eyebrows at start; new section strings render in Arabic, no glyph corruption. [S-08-settings-arabic-rtl]

- REG-06 RTL home appbar (no showBack) PASS: location selector at logical start (right) + bell+mint-dot at logical end (top-left); no back arrow; title/badge/height intact. [REG-home-arabic]
- N-13 notifications RTL PASS: back arrow mirrors to end, type circles + unread dot at logical start (right), title right-aligned, time at end, date headers right-aligned each once, seen-card holds. [N-13-notifications-arabic-rtl]

- REG (Orders appbar, no showBack) PASS: navy bar, "My Orders" left-aligned (centerTitle:false), cart action+mint badge at end, no back arrow, height intact. [REG-orders-appbar]
- REG static: checkout_screen NearsAppBar(title:'checkout', actions:[basket]) — no showBack, same backward-compat pattern; image_viewer/guest_track/order/offline_payment/digital_payment_failed also no-showBack. Additive param defaults false; existing layout untouched (also verified by 38 green DLS backward-compat tests).
- Cart "Your Basket" screen rendered fine (separate app bar; not in NearsAppBar set) — no breakage observed.

## RESTORE confirmed: English + Light + LTR + logged-in + Notification ON [Z-restored-english-light]
## Automated backstop: 38 tests passed (DLS backward-compat + notification grouping/payload pins).
## No runtime errors throughout (Dart MCP get_runtime_errors clean).
