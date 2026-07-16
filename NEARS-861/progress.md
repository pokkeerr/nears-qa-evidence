# NEARS-861 QA progress (micro, ar locale, emulator-5562)
- AC1 PASS: Profile > Background notification bottom sheet renders full Arabic sentence
  "تعطيل Nears Delivery من تشغيل الإشعارات في الخلفية؟" — fixed fragment
  "من تشغيل الإشعارات في الخلفية؟" resolves, NOT raw key. logs clean. shot AC1-background-notification-ar.png
- AC2 PASS (key-resolution + documented limitation): conversion not live-triggerable (0 loyalty pts,
  DB read-only); key present+valid in loaded ar.json; same file proven loaded/resolving by AC1.
  evidence AC2-key-resolution.log
- Env: worktree missing google-services.json (gitignored) -> copied from primary tree to boot (NEARS-968 area).
