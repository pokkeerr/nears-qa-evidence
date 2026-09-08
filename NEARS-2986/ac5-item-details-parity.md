# AC5 — persisted order_details.item_details snapshot parity (before/after, same cart)

Same 5-line cart (items 2,3,4,5,6 @ store 2) placed against pre-fix (abf27ae29) and post-fix (HEAD)
code, both against otherwise-identical scratch DB clones. Python diff of the two
`order_details.item_details` JSON blobs per item_id, keys normalized/sorted, only genuinely
volatile fields stripped (created_at/updated_at, storage[] rows carrying different auto-increment
ids, order_count/avg_rating/rating_count which can tick between runs).

Result: **DIFF: EMPTY** for all 5 items — structurally and value-identical.

Positive control (not vacuous): item 2's item_details carries 63 real keys including non-trivial
resolved values —
```
category_ids => [{'id': '3', 'position': 1, 'name': 'Fruits & Vegetables'}, {'id': '4', 'position': 2, 'name': 'Fresh Fruits'}]
flash_sale => 0
discount => 5
discount_type => percent
store_name => Fresh Mart Grocery
module_type => grocery
stock => 98
```
nutritions_name/allergies_name/generic_name/tax_data are legitimately `[]` for this fixture — this
DB seeds zero nutrition/allergy/generic/tax pivot rows for any item (confirmed: `item_nutrition`
table empty, `taxables` table empty). This is a real data characteristic of the fixture, not a
truncation caused by the fix (both before AND after render it identically empty).

Independently re-ran the engineer's own value-level fixture test (real Nutrition/Allergy/GenericName/
Tax rows attached to item 51 in a phpunit setUp(), asserting the EXACT batched-prefetch names/ids
come back correct, not just "present"):
```
✔ Five line cod cart query count stays bounded and order details shape intact  (86 assertions, incl.
  nutritions_name == ['NEARS-2986 Vitamin C'], allergies_name == ['NEARS-2986 Peanuts'],
  generic_name == ['NEARS-2986 Paracetamol'], tax_data[0].name == 'NEARS-2986 VAT'/rate 5.0,
  item 62 discount == 20.0/percent with flash_sale == 0)
```
