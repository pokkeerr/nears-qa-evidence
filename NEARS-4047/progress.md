# NEARS-4047 QA progress (checkpoint)
Backend: own `php artisan serve` :8047 from worktree @ aa097e940, DB clone multi_food_db_qa4047 (clone-only: local_storage=1, vendor 37 auth_token).
- AC1 PASS api-ac1-edit-and-db-identity.log
- AC2 PASS / AC3 PASS / AC4 PASS api-ac2-ac3-ac4-update-delete-status.log
- AC6 PASS api-ac6-idor-cross-store-and-admin-banner.log
- AC8 PASS phpunit-green.log (7/7), RED re-proved on scratch copy: phpunit-red-prefix-scratch.log (6/7 fail 500)
- BE log: 0 hits "Unknown column" in run window
- AC7: UNVERIFIABLE - VendorApp build refused by mem-guard (swap 11.5-12.6 GB > 6 GB cap for 10+ min); see vendorapp-build-blocked-memguard.log
- AC7 step1 add via app OK (list shows QA4047Alpha, scope-modified list() 200); first submit 422 invalid_upload was env (clone cache table held local_storage=0; cleared clone cache only) - not a code defect; 'probe' row curl-added to clone while diagnosing
- AC7 step2 edit via app OK: GET edit/{id} loaded form, PUT update -> list shows QA4047Beta, DB row 91109 title QA4047Beta, no [FAIL]
- AC7 step3 delete via app OK (QA4047Beta gone from list + DB), no [FAIL], ui_errors 0. AC7 PASS cycle 1
