# NEARS-729 Store-Panel IDOR sweep — QA progress checkpoint

Backend: worktree fix/NEARS-729-storepanel-idor-sweep booted on http://127.0.0.1:8010 (fixed code, working-tree).
Attacker session = Store A (ecomarket@demo.com, store_id 19, vendor 16). Victim = Store B (store_id 21).
Seeder StorePanelIdorQaFixtureSeeder ran clean. All cross-store POST/GET fired with A's session cookie + valid CSRF token.

| AC | Attack | Result | State on B |
|----|--------|--------|------------|
| 729 packageBuy | POST package-buy store_id=21 | 403 (abort) | store21 txns still 1 ✓ |
| 730 switchToCommission | POST switch-to-commission/21 | 403 (abort) | store21 model still commission ✓ |
| 751 packageView | GET package-view/1/21 | 403 | n/a (read) ✓ |
| 751 invoice | GET invoice/1000000 | 404 (findOrFail scoped) | n/a (read) ✓ |
| 733 campaign add | POST add-store/2/21 | 403 | store21 NOT in campaign2 ✓ |
| 733 campaign remove | POST remove-store/1/21 | 403 | store21 still in campaign1 ✓ |
| 733 old GET route | GET add-store/2/19 | 405 Method Not Allowed ✓ | n/a |
| 735 review reply | POST store-reply/6 | 404 (whereHas item.store_id) | review6 still store21, reply null ✓ |
| 775 make_payment | POST make-collected-cash store_id=21 | 403 (abort, post-validation) | no cross-store payer built ✓ |
| 776 employee role | POST add-new role_id=2 (AJAX) | 422 role_id invalid ✓ | no employee created ✓ |

Own-store happy paths (reversible, live):
- 733 join campaign2 (store19) -> 302 success; leave -> 302; net 0 in DB ✓
- 735 reply own review7 (store19) -> 302; reply updated, store_id stays 19 ✓
- 751 own package-view/1/19 -> 200 render ✓
- 776 own role_id=1 -> role_id error ABSENT (accepted by rule), only unrelated image/password errors ✓
- 729/730 own debit/flip -> cited phpunit (no live irreversible mutation)

Logs-first: grep [FAIL]/[ERR] on worktree laravel.log = clean for this run. Pre-existing testing.ERROR memory-exhaustion entries (15:07-15:10) = phpunit-channel, the known Review::saved() recursion regression-candidate, NOT this run.

phpunit Round729 backstop: running.
