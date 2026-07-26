# NEARS-1397 QA progress (emulator-5558, light mode)
- Sign-in screen renders: Email/Phone (email mode, mint-tinted phone+mail icon on focus), Password (lock + eye). PASS render.
- Email->Phone swap: picker (+971 UAE flag) + 2px divider render inside border. digit-only numeric keypad. PASS render.
- BUG (task): email->phone swap dismisses keyboard (mInputShown true->false), drops focus+keystrokes. Breaks AC3/point2. evidence 03d + bug log.
