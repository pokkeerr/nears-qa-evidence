# NEARS-3898 QA progress (phase 8, cycle 0)
env: own serve :8198 from worktree Admin (b116967ee), DB multi_food_db_qa3898, emulator-5580 (Pixel_10_Pro_2), pkg com.izzes.nears.nears_nears_3898_same_module_group_surge
copy-only setup: surge fixture id 1 (zone2/module1 +5 amount, 2026-09-30); admin_free_delivery_status 1->0 (else every delivery_charge=0); user 6 cart cleared
- AC1 PASS: flag OFF same-module group 12+13 ASAP -> 91418 dc 6.00 / odc 6.00, 91419 dc 6.00 / odc 6.00 (1.00 base + 5.00 surge). premise TRUE.
- AC2 PASS: cart rows 6.00/6.00; checkout per-store 6.00/6.00, Delivery Fees 12.00, breakdown 6.00/6.00, surge tooltip "High demand delivery fee"; placed children 6.00 each. logs clean (only env Firebase init [FAIL]).
- AC3 PASS: flag ON same-module 12+13 -> cart 6.00/6.00, checkout 6.00/6.00, Delivery Fees 12.00, tooltip on Fresh supermarket; placed 91422/91423 dc 6.00 each.
- AC4 PASS: flag ON mixed 12+49 -> cart 6.00/1.00; checkout 6.00/1.00, Delivery Fees 7.00, tooltip only on surged row; probe cash_removed=false valid=true (COD kept); placed 91428 dc 6.00, 91429 dc 1.00. Positive control satisfied (surged > base, unsurged at base).
- CONTROL: same-module pharmacy 58+55 (module 3, no surge) -> cart 1.00/0.00(store free delivery), checkout breakdown 1.00/0.00, no surge Info on fee rows; 3 get-surge-price 200.
- REG single-store: 58 (no surge) Delivery Fee +1.00; 12 (surge) Delivery Fee +6.00 (Info note present), Total 11.62 = placed child 91418 order_amount. PASS
- AC-LOG PASS: surge endpoint forced 500 (copy table rename) -> basket 1.00/1.00, no toast, 1 [FAIL] per failed per-store fetch (api_client, correlation joins BE [FAIL]); checkout-entry toast comes from pre-existing header-store getSurgePrice (checkout_controller.dart:282, unchanged), logged. Table restored.
- EXTRA percent variant (amount row parked): 50% of 1.00 -> basket 1.50/1.50 same-module; fixture restored to amount +5 (id 1).
