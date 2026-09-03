# NEARS-2890 QA progress

Device: emulator-5556 (locked via qa-lock-guard, key NEARS-2890)
Backend: primary Admin/ tree, php artisan serve :8000, proxied through qa_fail_proxy.py (run-key NEARS-2890, port 24985)
App: UserApp worktree /Users/Apple/Projects/nears-NEARS-2890-group-roster-error, launched with --dart-define=API_HOST=10.0.2.2:24985
Login: customer@nears.com / 123456789
Group used: order_group_id=2a6a7cfb-ea29-41bb-b0a8-30c4582889c8 (orders #91179 Nears Mart, #91180 Tower Mart, both pending, zone 1)
Reached: Profile -> Orders -> Ongoing tab -> "Orders from multiple stores" accordion -> Track Order on a child -> GroupTrackingView

- Baseline reach confirmed: GroupTrackingView renders normal header "0 of 2 delivered" + 2 child cards (Nears Mart #91179, Tower Mart #91180). No [FAIL]/[ERR] in logs for this action.
