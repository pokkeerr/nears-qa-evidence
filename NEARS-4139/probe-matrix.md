# NEARS-4139 QA probe matrix: BASE (leak) vs FIXED

Clone DB `multi_food_db_qa4139` (Sep-29 dump + stamped seeder, blob a3cd5091). Rows: id 1 = live row (store 91116, zone 1, item 91122), id 2 = zone-1 fixture (store 91125), id 3 = zone-2 fixture (store 91129). Actors: z1/z2 = zone-1/zone-2 item-module admins, zl = zone-less item-module admin, super = role_id 1.
BASE = detached worktree at 69abec1ed served on :8140; FIXED = worktree eef0bd61e served on :8139; both on the same clone DB.

## Non-destructive (HTTP status or row-id set)

| actor | probe | BASE | FIXED |
|---|---|---|---|
| z1 | list | 200 ids=[1, 2, 3] | 200 ids=[1, 2] **DIFF** |
| z1 | list_zone2 | 200 ids=[] | 200 ids=[] |
| z1 | list_zone1 | 200 ids=[1, 2] | 200 ids=[1, 2] |
| z1 | list_store91129 | 404 ids=[] | 404 ids=[] |
| z1 | list_store91125 | 200 ids=[2] | 200 ids=[2] |
| z1 | list_nomodule | 200 ids=[1, 2, 3] | 200 ids=[1, 2] **DIFF** |
| z1 | list_pending | 200 ids=[1, 2, 3] | 200 ids=[1, 2] **DIFF** |
| z1 | view_1 | 200 | 200 |
| z1 | edit_1 | 200 | 200 |
| z1 | view_2 | 200 | 200 |
| z1 | edit_2 | 500 | 500 |
| z1 | view_3 | 200 | 404 **DIFF** |
| z1 | edit_3 | 500 | 404 **DIFF** |
| z1 | export_csv | 200 rows=3 | 200 rows=2 **DIFF** |
| z1 | store_export_91116 | 500 rows=0 | 500 rows=0 |
| z1 | store_export_91125 | 500 rows=0 | 500 rows=0 |
| z1 | store_export_91129 | 404 rows=0 | 404 rows=0 |
| z2 | list | 200 ids=[1, 2, 3] | 200 ids=[3] **DIFF** |
| z2 | list_zone2 | 200 ids=[3] | 200 ids=[3] |
| z2 | list_zone1 | 200 ids=[] | 200 ids=[] |
| z2 | list_store91129 | 200 ids=[3] | 200 ids=[3] |
| z2 | list_store91125 | 404 ids=[] | 404 ids=[] |
| z2 | list_nomodule | 200 ids=[1, 2, 3] | 200 ids=[3] **DIFF** |
| z2 | list_pending | 200 ids=[1, 2, 3] | 200 ids=[3] **DIFF** |
| z2 | view_1 | 200 | 404 **DIFF** |
| z2 | edit_1 | 200 | 404 **DIFF** |
| z2 | view_2 | 200 | 404 **DIFF** |
| z2 | edit_2 | 500 | 404 **DIFF** |
| z2 | view_3 | 200 | 200 |
| z2 | edit_3 | 500 | 500 |
| z2 | export_csv | 200 rows=3 | 200 rows=1 **DIFF** |
| z2 | store_export_91116 | 404 rows=0 | 404 rows=0 |
| z2 | store_export_91125 | 404 rows=0 | 404 rows=0 |
| z2 | store_export_91129 | 500 rows=0 | 500 rows=0 |
| zl | list | 200 ids=[1, 2, 3] | 200 ids=[1, 2, 3] |
| zl | list_zone2 | 200 ids=[3] | 200 ids=[3] |
| zl | list_zone1 | 200 ids=[1, 2] | 200 ids=[1, 2] |
| zl | list_store91129 | 200 ids=[3] | 200 ids=[3] |
| zl | list_store91125 | 200 ids=[2] | 200 ids=[2] |
| zl | list_nomodule | 200 ids=[1, 2, 3] | 200 ids=[1, 2, 3] |
| zl | list_pending | 200 ids=[1, 2, 3] | 200 ids=[1, 2, 3] |
| zl | view_1 | 200 | 200 |
| zl | edit_1 | 200 | 200 |
| zl | view_2 | 200 | 200 |
| zl | edit_2 | 500 | 500 |
| zl | view_3 | 200 | 200 |
| zl | edit_3 | 500 | 500 |
| zl | export_csv | 200 rows=3 | 200 rows=3 |
| zl | store_export_91116 | 500 rows=0 | 500 rows=0 |
| zl | store_export_91125 | 500 rows=0 | 500 rows=0 |
| zl | store_export_91129 | 500 rows=0 | 500 rows=0 |
| super | list | 200 ids=[1, 2, 3] | 200 ids=[1, 2, 3] |
| super | list_zone2 | 200 ids=[3] | 200 ids=[3] |
| super | list_zone1 | 200 ids=[1, 2] | 200 ids=[1, 2] |
| super | list_store91129 | 200 ids=[3] | 200 ids=[3] |
| super | list_store91125 | 200 ids=[2] | 200 ids=[2] |
| super | list_nomodule | 200 ids=[1, 2, 3] | 200 ids=[1, 2, 3] |
| super | list_pending | 200 ids=[1, 2, 3] | 200 ids=[1, 2, 3] |
| super | view_1 | 200 | 200 |
| super | edit_1 | 200 | 200 |
| super | view_2 | 200 | 200 |
| super | edit_2 | 500 | 500 |
| super | view_3 | 200 | 200 |
| super | edit_3 | 500 | 500 |
| super | export_csv | 200 rows=3 | 200 rows=3 |
| super | store_export_91116 | 500 rows=0 | 500 rows=0 |
| super | store_export_91125 | 500 rows=0 | 500 rows=0 |
| super | store_export_91129 | 500 rows=0 | 500 rows=0 |

## Destructive (clone rebuilt from the seeded snapshot before every case)

| case | BASE status / row after | FIXED status / row after | new FAIL/ERROR log lines (BASE; FIXED) |
|---|---|---|---|
| z1_cross_deny_row3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | 404 / before rej=0 images=3 after rej=0 images=3 | clean ; clean |
| z1_inzone_deny_row2 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | clean ; clean |
| z1_cross_delete_row3 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | 404 / before rej=0 images=3 after rej=0 images=3 | clean ; clean |
| z1_inzone_delete_row2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | clean ; clean |
| z1_cross_delete_twice_row3 | 302->/admin/item/new/item/list?module_id=9 ; 2nd=500 / before rej=0 images=3 after ABSENT | 404 ; 2nd=404 / before rej=0 images=3 after rej=0 images=3 | ERROR: [FAIL] Attempt to read property "image" on null  ; clean |
| z1_inzone_delete_twice_row2 | 302->/admin/item/new/item/list?module_id=9 ; 2nd=500 / before rej=0 images=3 after ABSENT | 302->/admin/item/new/item/list?module_id=9 ; 2nd=404 / before rej=0 images=3 after ABSENT | ERROR: [FAIL] Attempt to read property "image" on null  ; clean |
| z1_cross_remove_image_row3 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | 404 / before rej=0 images=3 after rej=0 images=3 | clean ; clean |
| z1_inzone_remove_image_row2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | clean ; clean |
| z2_cross_deny_row2 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | 404 / before rej=0 images=3 after rej=0 images=3 | clean ; clean |
| z2_inzone_deny_row3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | clean ; clean |
| z2_cross_delete_row2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | 404 / before rej=0 images=3 after rej=0 images=3 | clean ; clean |
| z2_inzone_delete_row3 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | clean ; clean |
| z2_cross_delete_twice_row2 | 302->/admin/item/new/item/list?module_id=9 ; 2nd=500 / before rej=0 images=3 after ABSENT | 404 ; 2nd=404 / before rej=0 images=3 after rej=0 images=3 | ERROR: [FAIL] Attempt to read property "image" on null  ; clean |
| z2_inzone_delete_twice_row3 | 302->/admin/item/new/item/list?module_id=9 ; 2nd=500 / before rej=0 images=3 after ABSENT | 302->/admin/item/new/item/list?module_id=9 ; 2nd=404 / before rej=0 images=3 after ABSENT | ERROR: [FAIL] Attempt to read property "image" on null  ; clean |
| z2_cross_remove_image_row2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | 404 / before rej=0 images=3 after rej=0 images=3 | clean ; clean |
| z2_inzone_remove_image_row3 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | clean ; clean |
| zl_zoneless_deny_row3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | clean ; clean |
| zl_zoneless_delete_row2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | clean ; clean |
| zl_zoneless_remove_image_row3 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after rej=0 images=2 | clean ; clean |
| super_deny_row3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | 302->/admin/item/new/item/list / before rej=0 images=3 after rej=1 images=3 | clean ; clean |
| super_delete_row2 | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | 302->/admin/item/new/item/list?module_id=9 / before rej=0 images=3 after ABSENT | clean ; clean |
| z1_approve_row1_positive_control | 302->/admin/item/new/item/list / before rej=0 images=0 after ABSENT {'item91122_is_approved': '1'} | 302->/admin/item/new/item/list / before rej=0 images=0 after ABSENT {'item91122_is_approved': '1'} | ERROR: FCM API Error  ; ERROR: FCM API Error  |
| z2_approve_row1_cross | 404 / before rej=0 images=0 after rej=0 images=0 {'item91122_is_approved': '0'} | 404 / before rej=0 images=0 after rej=0 images=0 {'item91122_is_approved': '0'} | clean ; clean |
| z1_item_delete_91122_inzone_1093_control | 302->/admin/item/new/item/list?module_id=9 / before ABSENT after ABSENT {'before_item': '1', 'before_temp1': '1', 'after_item': '0', 'after_temp1': '0'} | 302->/admin/item/new/item/list?module_id=9 / before ABSENT after ABSENT {'before_item': '1', 'before_temp1': '1', 'after_item': '0', 'after_temp1': '0'} | clean ; clean |
