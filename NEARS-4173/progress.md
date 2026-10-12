# NEARS-4173 QA progress (checkpoint)
- BASE-RED twin (scratch copy, PlaceOrder.php = 9eb9b3013): phpunit --filter Nears4173 = 25 tests, 112 assertions, 5 failures (t3, t5, default, nameless t3, nameless t5). HEAD a16601b35: 25 tests, 141 assertions, 0 failures, 4 skipped (t6, t10 x2).
- Render all templates BASE vs HEAD: t3 -209 bytes (whole Download Invoice wrapper gone), t5 -262 bytes (whole bare-URL span gone); t6/t10 throw identically at BASE and HEAD.
- route:list --name=invoice md5 bcc08b197e53992d088c6142332edf6e at BASE and HEAD; full route:list md5 67338bea9edde4c19287efd853d7a212 both.
- AC3 HTTP on own server :8173 (worktree HEAD, private clone): anon/bogus/customer-Passport 403; panel sessions pass the gate.
