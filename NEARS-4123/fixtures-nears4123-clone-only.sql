-- NEARS-4123 QA fixtures. TARGET: multi_food_db_qa4123 (private clone) ONLY. Never apply to multi_food_db.
SELECT IF(DATABASE()='multi_food_db_qa4123','db ok',(SELECT 1 FROM information_schema.tables LIMIT 2));
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91501, order_status='processing', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET confirmed='2026-10-11 05:00:00', processing='2026-10-11 05:00:00' WHERE id=91501;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91501,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91502, order_status='processing', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET confirmed='2026-10-11 05:00:00', processing='2026-10-11 05:00:00' WHERE id=91502;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91502,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91503, order_status='handover', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET confirmed='2026-10-11 05:00:00', processing='2026-10-11 05:00:00', handover='2026-10-11 05:00:00' WHERE id=91503;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91503,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91504, order_status='failed', payment_status='unpaid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET failed='2026-10-11 05:00:00' WHERE id=91504;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91504,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91505, order_status='pending', payment_status='unpaid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91505,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91506, order_status='pending', payment_status='unpaid', payment_method='offline_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91506,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO offline_payments (order_id,payment_info,status,method_fields,created_at,updated_at) SELECT 91506,payment_info,'pending',method_fields,'2026-10-11 05:00:00','2026-10-11 05:00:00' FROM offline_payments WHERE id=50;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91507, order_status='pending', payment_status='unpaid', payment_method='cash_on_delivery', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91507,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91508, order_status='returned', payment_status='paid', payment_method='digital_payment', order_type='parcel', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET store_id=NULL, module_id=5, parcel_category_id=1, payment_method='digital_payment' WHERE id=91508;
INSERT INTO orders SELECT * FROM t_o;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91511, order_status='canceled', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00' WHERE id=91511;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91511,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91521, order_status='canceled', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00' WHERE id=91521;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91521,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91531, order_status='canceled', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00' WHERE id=91531;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91531,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91541, order_status='canceled', payment_status='unpaid', payment_method='offline_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00' WHERE id=91541;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91541,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO offline_payments (order_id,payment_info,status,method_fields,created_at,updated_at) SELECT 91541,payment_info,'pending',method_fields,'2026-10-11 05:00:00','2026-10-11 05:00:00' FROM offline_payments WHERE id=50;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91561, order_status='canceled', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00' WHERE id=91561;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91561,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO refunds (order_id,user_id,order_status,image,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES (91561,6,'delivered','[]','QA fixture 4123',52.47,'pending','wallet','2026-10-11 05:00:00','2026-10-11 05:00:00');
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91512, order_status='refunded', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00', refunded='2026-10-11 05:00:00' WHERE id=91512;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91512,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91522, order_status='refunded', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00', refunded='2026-10-11 05:00:00' WHERE id=91522;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91522,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91532, order_status='refunded', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00', refunded='2026-10-11 05:00:00' WHERE id=91532;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91532,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91542, order_status='refunded', payment_status='unpaid', payment_method='offline_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00', refunded='2026-10-11 05:00:00' WHERE id=91542;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91542,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO offline_payments (order_id,payment_info,status,method_fields,created_at,updated_at) SELECT 91542,payment_info,'pending',method_fields,'2026-10-11 05:00:00','2026-10-11 05:00:00' FROM offline_payments WHERE id=50;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91562, order_status='refunded', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00', refunded='2026-10-11 05:00:00' WHERE id=91562;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91562,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO refunds (order_id,user_id,order_status,image,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES (91562,6,'delivered','[]','QA fixture 4123',52.47,'pending','wallet','2026-10-11 05:00:00','2026-10-11 05:00:00');
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91513, order_status='failed', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET failed='2026-10-11 05:00:00' WHERE id=91513;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91513,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91523, order_status='failed', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET failed='2026-10-11 05:00:00' WHERE id=91523;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91523,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91533, order_status='failed', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET failed='2026-10-11 05:00:00' WHERE id=91533;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91533,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91543, order_status='failed', payment_status='unpaid', payment_method='offline_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET failed='2026-10-11 05:00:00' WHERE id=91543;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91543,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO offline_payments (order_id,payment_info,status,method_fields,created_at,updated_at) SELECT 91543,payment_info,'pending',method_fields,'2026-10-11 05:00:00','2026-10-11 05:00:00' FROM offline_payments WHERE id=50;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91563, order_status='failed', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET failed='2026-10-11 05:00:00' WHERE id=91563;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91563,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO refunds (order_id,user_id,order_status,image,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES (91563,6,'delivered','[]','QA fixture 4123',52.47,'pending','wallet','2026-10-11 05:00:00','2026-10-11 05:00:00');
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91514, order_status='returned', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91514,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91524, order_status='returned', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91524,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91534, order_status='returned', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91534,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91544, order_status='returned', payment_status='unpaid', payment_method='offline_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91544,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO offline_payments (order_id,payment_info,status,method_fields,created_at,updated_at) SELECT 91544,payment_info,'pending',method_fields,'2026-10-11 05:00:00','2026-10-11 05:00:00' FROM offline_payments WHERE id=50;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91564, order_status='returned', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91564,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO refunds (order_id,user_id,order_status,image,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES (91564,6,'delivered','[]','QA fixture 4123',52.47,'pending','wallet','2026-10-11 05:00:00','2026-10-11 05:00:00');
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91551, order_status='canceled', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00' WHERE id=91551;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91551,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91552, order_status='refunded', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET canceled='2026-10-11 05:00:00', refunded='2026-10-11 05:00:00' WHERE id=91552;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91552,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91553, order_status='returned', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91553,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91554, order_status='failed', payment_status='unpaid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET failed='2026-10-11 05:00:00' WHERE id=91554;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91554,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91565, order_status='refund_requested', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET confirmed='2026-10-11 05:00:00', processing='2026-10-11 05:00:00', handover='2026-10-11 05:00:00', delivered='2026-10-11 05:00:00', refund_requested='2026-10-11 05:00:00' WHERE id=91565;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91565,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO refunds (order_id,user_id,order_status,image,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES (91565,6,'delivered','[]','QA fixture 4123',52.47,'pending','wallet','2026-10-11 05:00:00','2026-10-11 05:00:00');
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91571, order_status='pending', payment_status='unpaid', payment_method='cash_on_delivery', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91571,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91572, order_status='pending', payment_status='unpaid', payment_method='cash_on_delivery', order_type='delivery', delivery_man_id=3, store_id=2, module_id=1, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 2,91572,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91573, order_status='pending', payment_status='unpaid', payment_method='cash_on_delivery', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91573,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91574, order_status='pending', payment_status='unpaid', payment_method='offline_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91574,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO offline_payments (order_id,payment_info,status,method_fields,created_at,updated_at) SELECT 91574,payment_info,'pending',method_fields,'2026-10-11 05:00:00','2026-10-11 05:00:00' FROM offline_payments WHERE id=50;
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91581, order_status='processing', payment_status='paid', payment_method='digital_payment', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
UPDATE t_o SET confirmed='2026-10-11 05:00:00', processing='2026-10-11 05:00:00' WHERE id=91581;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91581,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
INSERT INTO refunds (order_id,user_id,order_status,image,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES (91581,6,'delivered','[]','QA fixture 4123',52.47,'pending','wallet','2026-10-11 05:00:00','2026-10-11 05:00:00');
