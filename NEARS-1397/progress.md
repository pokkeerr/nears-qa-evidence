# NEARS-1397 DELTA re-QA (fix-cycle 1) — checkpoint

Device: emulator-5558 | fresh build from worktree feat/NEARS-1397-ninput-migrate (uncommitted) | UserApp

- AC3/TB1 money shot (email->phone autodetect swap): PASS — keyboard stayed up (mInputShown=true throughout), all 10 digits landed (1501234567), picker "+971" appeared instantly on first digit. Log clean.
- Reverse toggle: PASS via clearing field -> email mode returns, picker gone, "Email/Phone" placeholder, keyboard up, mail glyph returns; @ typed in email mode NOT filtered (a@b landed).
  - NOTE: typing @/letter WHILE in phone mode does NOT flip back (digit-only formatter strips it) -> reverse only via clearing. Low finding.
- Phone-mode filter: PASS (letters/'@' stripped, only digits). Email-mode no filter: PASS.
- NPhoneField regression (sign-up): PASS — picker + 2px divider render; picker opens; select American Samoa -> dial code +971 -> +1684; digit filter (ab12cd34 -> 1234).
- Logs: CLEAN (322-line app log, 0 [FAIL]/[ERR]/exception/overflow).
- Automated: email_or_phone_login_field_test 2 pass (IME-identity + falsifiable control); n_phone_field+login_a11y 9 pass; nears_dls n_input 31 pass.
