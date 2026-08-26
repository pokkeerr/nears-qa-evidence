# NEARS-2527 — live GET regression checks (Admin `message/view`)

Backend booted from THIS worktree, own port (8033), against the real shared
`multi_food_db` (read-only — GET only, no POST to `admin.message.store`).
PID 11371 cwd confirmed = `nears-NEARS-2527-conversation-store-nulldeference/Admin/public`.

Admin login via `login/admin` + `login_submit` (captcha prefilled by `APP_MODE=dev`).

| Type | conversation_id | user_info_id (PK) | GET `/admin/message/view/<conv>/<uid>` | reply-form posted URL | View Details link |
|---|---|---|---|---|---|
| delivery_man | 1 | 1 | 200 | `.../admin/message/store/1` | absent (correct — AC4 of NEARS-2457) |
| vendor | 46 | 111 | 200 | `.../admin/message/store/111` | absent (correct) |
| customer | 60 | 3 | 200 | `.../admin/message/store/3` | present (correct — customer path unchanged) |

All three reply-form URLs post the **UserInfo PK**, confirming the blade fix
(`$user->id` instead of `$user->user_id ?? 0`) is live-rendering correctly for
every participant type. Raw JSON responses saved alongside this file:
`view-delivery_man-conv1-userinfo1.json`, `view-vendor-conv46-userinfo111.json`,
`view-customer-conv60-userinfo3.json`.

`storage/logs/laravel.log` scanned around the request timestamps
(05:43:19–05:43:25) — no `[FAIL]`/`[ERR]` tied to `ConversationController` or
`admin/message/view`; the only entries in that window are pre-existing,
unrelated OTel-collector-unreachable noise (no local collector running —
environmental, not caused by this change).
