# NEARS-4152 QA progress (checkpoint log)
Tested tip 0c7a79ede3a0 on base 730b280e2. Clone DB multi_food_db_qa4152 (pristine: no admin holds `settings`; role_id 1 modules NULL).
Servers: A :8152 worktree Admin (artisan serve --no-reload), B :8153 scratch copy of tip (artisan serve, then restarted as `php -S -t public server.php` cwd=Admin so index.blade's relative include resolves), C :8154 scratch copy of base 730b280e2. All DB_DATABASE=multi_food_db_qa4152.
Driver: authenticated HTTP session (python requests, real /login_submit logins, per-request X-Request-Id), Chrome DevTools MCP for the Toastr screenshot.
R1 A: r1_serverA*.json ; R1 B: r1_serverB_nonsuper.json ; RED base: r1_serverC_base_RED.json, r2_C_*.json
R2 B: r2_B_*.json ; lifecycle r2_B_c_lifecycle.json ; EXTRA sec_confirm_B.json ; sweep regression_sweep_A.json
Real Admin/Modules sha1 listing before == after (7125694c...); worktree git status clean.
