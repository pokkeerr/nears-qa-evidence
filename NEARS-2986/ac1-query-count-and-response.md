# AC1 — 5-line COD cart place-order + independent query-count measurement

## Response (200)
```
POST /api/v1/customer/order/place  store_id=2 (Fresh Mart Grocery, zone 1, grocery module)
items: 2(x2), 3(x1), 4(x1), 5(x1), 6(x1) — plain, no addons, no coupon
{
  "message": "Order placed successfully",
  "order_id": 91213,
  "total_ammount": 17.96,
  "status": "pending",
  "user_id": 6
}
```

## Independent query-count measurement (QA's own, not the engineer's phpunit number)
Methodology: booted the REAL Laravel HTTP kernel in-process (`Illuminate\Contracts\Http\Kernel::handle()`)
against (a) this worktree's HEAD (post-fix) and (b) a disposable `git worktree` checked out at the
pre-fix base commit `abf27ae29`, each against its own disposable scratch-DB clone of the same seeded
cart/store fixture, with a REAL Passport bearer token (not `Passport::actingAs`'s auth bypass — this
measurement pays the full oauth-token-validation query cost the engineer's phpunit harness does not),
counted via `DB::listen()`.

| | query count |
|---|---|
| baseline (abf27ae29, pre-fix) | **292** |
| this worktree (HEAD, post-fix) | **136** |
| reduction | 53.4% |

Engineer's own number (PR, via `Nears2986PlaceOrderQueryCountTest`'s `DB::listen()`, `Passport::actingAs` bypass): 253 -> 106 (~58%). Different absolute numbers (different auth-cost baseline), same conclusion: real, substantial, order-of-magnitude-consistent reduction — not a rounding/measurement artifact.

Also independently RAN the engineer's own test live on this worktree (not just read/trusted it):
```
$ vendor/bin/phpunit --filter Nears2986 --testdox
Nears2986Place Order Query Count
 ✔ Five line cod cart query count stays bounded and order details shape intact
OK (4 tests, 86 assertions)
```
