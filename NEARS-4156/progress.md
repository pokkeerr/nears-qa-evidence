# NEARS-4156 QA [8] cycle 0 - evidence index (text-only, harmless markers)

Tested tip 930990010ad091de9676aeffbd8dba2cc5562f7c, base b64817f95ae0071ddcace57bb98b10756661ea46. Device-free ticket (no device lock).
Private clone `multi_food_db_qa4156` built from a read-only mysqldump of the shared DB; stamped seeders 4130 (8dba3b76) and 4139 (a3cd50916) run UNCHANGED, inline env, then cache:clear. Shared DB verified untouched (0 qa.zone1 rows).
Servers (each `OTEL_SDK_DISABLED=true DB_DATABASE=multi_food_db_qa4156 php artisan serve --no-reload`, `ps eww` DB proof before any write arm; SESSION_SECURE_COOKIE=false inline so curl/requests keep the cookie):
- A :18156 the worktree (GET/guard arms only, no upload; freshness guard PASS @ 930990010)
- B :18157 scratch rsync copy of the tested tip with its own vendor/, storage/app and landing/custom = TESTED server (freshness guard exit 2: not a git work tree, expected for a scratch copy; app/ routes/ resources/ config/ database/ diff-identical to the tip)
- C :18158 scratch `git archive b64817f95` + own composer install (artisan serve cwd=public) and C2 :18159 `php -S -t public server.php` with cwd=Admin (production-like cwd: base uses relative `storage/app/` and `resources/views/...` paths, which land under public/ with artisan serve) = RED arms
Logins: settings admin and role_id 1 via the real login form (settings admins use role=admin_employee). Password per users_test_data.md (not recorded here).

Log streams: every refusal is written to BOTH storage/logs/laravel.log (text) and laravel-structured.log (JSON); "ONE line" below = exactly one line in EACH stream, located by X-Request-Id == correlation_id; keys endpoint,status,reason (+correlation_id); name/marker tokens in all 168 refusal lines of tree B: 0 (`fail_lines_sample_B.txt`).

## Per-AC
| AC | Status | Evidence file |
|---|---|---|
| AC1 | PASS | ac1_tested_B_table.txt (25 hostile archives, all refused, tree + rows byte-identical, one line each), ac1_with_legacy_present_B.json (store + legacy file both untouched on 5 refusals), ac1_base_RED_C_table.txt (19/25 land at base) |
| AC2 | PASS (note) | ac2_tested_B_table.txt (122 cases over both registrations, 110 with exactly one [FAIL]; 12 explained: 10 validator-layer php-family image names, 2 trimmed path "sp "), ac2_base_RED_C2_table.txt |
| AC3 | PASS for 6 of 8 routes; UNVERIFIABLE for /shipping-policy and /cancelation | ac3_B.json, ac3fm_B.json vs ac3fm_C2.json, ac3c_B.json, ac3_extra_B.json, direct_store_read.txt |
| AC4 | test-proven | phpunit_*.txt (70 + 57 + 53 + 3 tests green); base-RED also shown live |
| AC5 | test-proven | conductor holds the mutation table |
| AC6 | PASS | ac6_route_inventory.txt (0 lines diff over 1466 routes) |
| AC7 | PASS | AC1-AC3 arms + ac7_web_reachability.txt (measured on a scratch Apache+php-fpm vhost, not production) |
| AC8 | PASS | ac8_B.json |
| AC9 | PASS (process prerequisites only) | ticket body carries AC1-AC9, PO comment 24907, TL comment 24908 (owner-list item, operational guard, 5 behaviour changes); close-out/epic record is a [10]/[11] conductor step |

## Notes that matter
- /shipping-policy and /cancelation: HomeController aborts 404 BEFORE the landing branch while data_settings `shipping_policy_status` / `cancellation_policy_status` are absent (absent from the pristine dump and from both stamped seeders). Same 404 at base (C2). Making them reachable needs a data_settings write: not stamped, not done. Test `Nears4156LandingUploadTest::test_a_legit_archive_installs_and_is_served_literally_and_sandboxed_on_all_eight_routes` seeds those keys and passes.
- libzip normalises control bytes / NUL in entry names to CP437 glyph / space under the default getNameIndex flags, so such entries never reach the guard as control characters; they install as ordinary names (measured, harmless; guard's own control-char refusal is unit-tested and probe-verified).
- FM index returned 500 while my planted symlinks sat in storage/app (Flysystem refuses links; same at base C2; A without symlinks returned 200); after removing them: 200 on B and C2. Environmental, not a finding.
- Pre-existing: `admin.file-manager.download` has no module:settings middleware (unchanged; route diff 0).

## Cycle 1 (delta re-QA, same tip 930990010, AC3-residual only)
Fresh clone multi_food_db_qa4156 (read-only mysqldump, stamped seeders 4130 8dba3b76 / 4139 a3cd50916 unchanged), fresh scratch tree B (rsync of tip, own vendor) and base tree C (git archive b64817f95, own composer install, php -S cwd=Admin).
Server env note: this cycle artisan serve's child process carried a duplicate DB_DATABASE (including the shared name) and the .env SESSION_SECURE_COOKIE=true, and logins failed 419 (secure cookie over http). Before ANY write I set DB_DATABASE=multi_food_db_qa4156 and SESSION_SECURE_COOKIE=false in the SCRATCH copies' .env (never the worktree's) and restarted; proof = the clone-only account qa.zone1.subscription@nears.test logs in on both servers (it does not exist in the shared DB: 0 rows). Shared DB afterwards: 0 qa.zone1 admins, 0 shipping/cancellation status rows.
Controller read first: BusinessSettingsController::shipping_policy_status / cancellation_policy_status -> policy_status_update($key,$status) = DataSetting::firstOrNew(['key'=>$key,'type'=>'admin_landing_page']); value=$status; save(); returns {"status":"changed"}. Nothing else.
Steps as role_id 1 (admin@admin.com, role=admin) on tree B: data_settings before = no rows; /shipping-policy and /cancelation = 404; POST pages/shipping-policy/1 and pages/cancellation-policy/1 -> 200 {"status":"changed"}; data_settings after = exactly ids 165 shipping_policy_status and 166 cancellation_policy_status, type admin_landing_page, value 1 (read-only SELECT); update-landing-setup with lz_legit.zip -> success, landing_page=0, landing_integration_type=file_upload.
Result (cycle1_delta_tip_B.json): all 8 routes 200, Content-Security-Policy exactly "sandbox allow-scripts allow-forms allow-popups", text/html; charset=UTF-8, response sha1 == uploaded index sha1 350ae2ca3585b051fc0232157efcaf9a695b819c, {{ 'MARK4156' }} and <?php echo 'MARK4156'; ?> present as text.
RED at base (cycle1_delta_base_RED_C2.json, cwd=Admin): same toggles + install; all 8 routes 200 incl. /shipping-policy and /cancelation, body = executed template ("MARK4156MARK4156"), NO CSP header.
Real-tree guard (cycle1_real_tree_guard_*.txt): equal, listing sha1 d270f026...; git status shows only the conductor's doc edit.
