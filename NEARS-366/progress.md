# NEARS-366 (AW-01 db-wipe whitelist) — QA progress checkpoint

Surface: Admin Laravel web panel. Branch: fix/NEARS-366-db-wipe-whitelist. Backend :8000, APP_MODE=dev.

- AC1 (super-admin view, protected tables excluded from clearable list): **PASS (live)**.
  - db-index renders 134 clearable `tables[]` checkboxes, HTTP 200, no error.
  - 0 protected tables leaked; users/admins/oauth_access_tokens/phone_verifications/email_verifications/social_media all NOT offered.
  - DB cross-check: 154 total tables − 20 protected (all real) = 134 clearable. Exact match.
  - Evidence: 01-db-index-clearable-list.png
- AC2 (non-super-admin reject): **covered by phpunit** — no admin employee (role_id != 1) exists in users_test_data.md or the live admins table (only id=1, role_id=1). Cannot exercise live without fabricating an account. Verified via test_non_super_admin_cannot_clean_db.
- AC3 (strict whitelist all-or-nothing, deletion paths): **verified via transactional phpunit** (DB read-only rule — not live-mutated).
- Focused backstop DbCleanWhitelistTest: 7/7 green, 57 assertions.
