# NEARS-1280 QA progress (cycle 0)

## AC1 — solution doc — PASS
- docs/data-qa/NEARS-1280-accepted-placeholder-policy.md exists, reads correctly, states the
  accepted-placeholder policy (owner decision 2026-07-18), distinguishes from NEARS-1262.
- Referenced in docs/index.md under `## data-qa` section.
- Referenced in docs/catalog.json (valid JSON, verified via python3 json.load).

## AC2 — queryable report command — PASS
- `php artisan data:report-placeholder-image-items` (human output): "placeholder image
  \"673c408cef130\" — 951 item(s)"
- Independent SQL check: `SELECT COUNT(*) FROM items WHERE images LIKE '%673c408cef130%'` = 951.
  MATCHES.
- `--json` form: {"filename":"673c408cef130","count":951,"item_ids":[...951 ids...]} — count and
  ids_len both 951.
- `--filename=doesnotexist12345` (negative control): 0 items — confirms filter genuinely scopes.
- `--filename=c217422465b7` (real, different substring): command returned 1 item (id=2); SQL
  cross-check `SELECT COUNT(*) FROM items WHERE images LIKE '%c217422465b7%'` = 1. MATCHES —
  proves --filename is not hardcoded/stubbed.

## AC3 — no new photography, count unchanged by design — PASS
- `git show 5cced749b614a4f2f276a2fa92ef5dcd1ceafbb2 --stat --name-only`: 5 files, all
  code/docs/tests — zero image/binary extensions in the diff.
- NEARS-1262 disk-presence fix files (Admin/storage/app/public/.gitignore,
  .../product/2024-11-19-673c408ce{f130,db59}.png committed at dbcc81f9/e53ba4cb) show zero diff
  between e53ba4cb and 5cced749 — untouched.
- Placeholder file still present on disk: Admin/storage/app/public/product/2024-11-19-673c408cef130.png

## Automated backstop — PASS
- `php artisan test --filter=ReportPlaceholderImageItemsTest`: 4 passed (8 assertions), isolated
  test DB `multi_food_db_test_nears_nears_1280_seed_placeholder`.

## Regression — clean
- No UI surface touched. NEARS-1262 fix confirmed untouched (see AC3).

## Evidence note
Docs/data/CLI ticket — no screenshots taken (no UI surface, no [ui]-tagged ACs). Evidence is
command output + SQL cross-checks captured verbatim above.
