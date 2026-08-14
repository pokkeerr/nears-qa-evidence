# NEARS-1931 — QA [8] progress log

Device `emulator-5566` (448x997dp, Android, Asia/Dubai, TZ +04) · branch
`fix/NEARS-1931-yesterday-date-arithmetic` · worktree `/Users/Apple/Projects/nears-NEARS-1931-yesterday`
· APK host mtime `2026-08-14 21:14:41 +0400` == device `lastUpdateTime=2026-08-14 21:14:42` (stale-APK ruled out
by mtime match, not by firstInstallTime).

| # | Check | Result | Evidence |
|---|---|---|---|
| L1 | Chat bubble, today-stamped message (EN) | PASS | `Today, 7:11/7:24/7:36 AM` — matches `messages.created_at` 07:11:59 / 07:24:16 / 07:36:34 (conv 45). `ac-live1-chat-today-en.png` |
| L2 | Notification list, today + dated headers (EN) | PASS | `Today` / `12 Aug 2026` / `11 Aug 2026`. `ac-live2-notifications-today-en.png` |
| L3 | Chat bubble, Arabic | PASS | codepoints `اليوم` + `, ` + U+202A `7:11 AM` U+202C — translated word, time LTR-isolated exactly once. `ac-live3-chat-today-ar.png` |
| L4 | Notification list, Arabic | PASS | `اليوم` bare (near branch), `‪12 Aug 2026‬` LTR-wrapped (dated branch). `ac-live4-notifications-today-ar.png` |
| L5 | RTL mirror, by pixel | PASS | MSE(ltr,rtl)=2772.9 vs MSE(ltr,mirror(rtl))=2409.9 — mirror closer; control MSE(ltr,ltr)=0.0 |
| L6 | Runtime logs during every AC | clean | 0 `[FAIL]`, 0 `[ERR]`, 0 `EXCEPTION CAUGHT`, 0 overflow — positive control 290 `[NET]` lines |
| L7 | Regression: orders list, conversation list, profile | clean | `01 Jul 2026, 06:55 PM • #164`, `07:40 AM \| 14-Aug-2026`, `Joined 01 Mar, 2026` all render |
| A1 | Automated backstop, full UserApp suite | PASS | `+3830 ~2 -4`; the 4 `[E]` are the 4 expected pre-existing failures, matched BY NAME |

## Not demonstrated live (honest gaps)
- **1st-of-month yesterday rendering** — today is the 14th; the trigger needs the device calendar date AND a
  matching `created_at`. No yesterday-dated chat/notification row exists on seeded data (NEARS-1947), and
  creating one requires a DB write (forbidden). Unit-pinned only.
- **DST / timezone behaviour** — `TZ` is process-level, unreachable from the app UI. Unit-pinned only.
- **Mutation-checked RED** — build-time proof, not observable at runtime.
