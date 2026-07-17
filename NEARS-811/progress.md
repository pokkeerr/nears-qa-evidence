# NEARS-811 QA progress (VendorApp FCM payload log-drop) — emulator-5556, debug build from worktree

- AC1 (full-payload onMessage debugPrint removed): PASS — git diff shows exact line deleted; grep confirms absent in running-build source.
- AC2 (full-payload onOpenApp debugPrint removed): PASS — git diff shows exact line deleted; grep confirms absent.
- AC3 (type-only lines remain + fire): PASS — lines 87/174 present; LIVE: real FCM foreground push logged `onMessage message type:message` (08:52:17.447).
- AC4 (routing unchanged): PASS — type=message push (app off chat screen) hit else-branch → getNotificationList() refresh fired live; diff shows routing code byte-identical.
- AC5 (no full data map logged): PASS — LIVE: PII-laden foreground push logged ONLY the type: line; full `message.data` map + PII sentinels absent from onMessage path.
- Regression guard: compile + clean boot (with google-services.json) + no crash. FCM messaging live.
- onOpenApp path (AC2 runtime): static-diff + running-build verified; live tap infeasible (grouped notification, no coordinate-tap per rule).
- Followup (non-blocking): onBackground handler line 372 customPrint logs full data map in DEBUG (kDebugMode-guarded → release-stripped, out of ticket scope).
