# NEARS-1042 QA — store-settings delivery_time 500 fix

Branch: fix/NEARS-1042-store-settings-delivery-time-500 (fix present as working-tree edit in Admin/resources/views/admin-views/vendor/view/settings.blade.php)
Served from worktree: /Users/Apple/Projects/nears-NEARS-1042-store-settings-500/Admin @ http://127.0.0.1:8042
DB: multi_food_db (read-only)

Precondition delivery_time values observed:
- store 1 = "30-40 min"  (suffixed)
- store 2 = "30-45"      (UNSUFFIXED — reproduces bug scenario)
- store 3 = "25-35"      (UNSUFFIXED — reproduces bug scenario)

| AC | Result | Evidence |
|----|--------|----------|
| AC1 store2 admin settings | PASS — HTTP 200, min=30 max=45 unit=min | ac1-store2-settings.png |
| AC1 store3 admin settings | PASS — HTTP 200, min=25 max=35 unit=min | ac1-store3-settings.png |
| AC2 store1 admin settings (no regression) | PASS — HTTP 200, min=30 max=40 unit=Minutes | ac2-store1-settings.png |
| AC3 laravel.log "Undefined array key 1" | PASS — no laravel.log created at all; zero errors | (log absent) |
| AC4 store2 vendor business-settings | PASS — HTTP 200, no 500, min=30 max=45 | ac4-store2-vendor-business-settings.png |
| AC4 store3 vendor business-settings | PASS — HTTP 200, no 500, min=25 max=35 | ac4-store3-vendor-business-settings.png |

Falsifiable pre-fix check: original expression explode(' ',explode('-','30-45')[1])[1] THREW "Undefined array key 1"; post-fix parse returns min=30 max=45 unit=min cleanly.

VERDICT: PASS
