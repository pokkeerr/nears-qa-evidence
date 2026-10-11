-- NEARS-4123 QA fixtures. TARGET: multi_food_db_qa4123 (private clone) ONLY. Never apply to multi_food_db.
SELECT IF(DATABASE()='multi_food_db_qa4123','db ok',(SELECT 1 FROM information_schema.tables LIMIT 2));
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=91132;
UPDATE t_o SET id=91593, order_status='pending', payment_status='unpaid', payment_method='cash_on_delivery', order_type='delivery', delivery_man_id=3, store_id=39, module_id=2, user_id=6,
        refund_requested=NULL, accepted=NULL, handover=NULL, delivered=NULL, confirmed=NULL, processing=NULL, picked_up=NULL, canceled=NULL, refunded=NULL, failed=NULL,
        pending='2026-10-11 05:00:00', created_at='2026-10-11 05:00:00', updated_at='2026-10-11 05:00:00', schedule_at='2026-10-11 05:00:00', otp=4099, transaction_reference=NULL, delivery_charge=0.00, original_delivery_charge=0.00,
        free_delivery_by=NULL, store_discount_amount=0, total_tax_amount=0, order_amount=52.47, dm_vehicle_id=NULL;
INSERT INTO orders SELECT * FROM t_o;
INSERT INTO order_details (item_id,order_id,price,item_details,variation,add_ons,discount_on_item,discount_type,quantity,tax_amount,variant,created_at,updated_at,total_add_on_price,category_id,discount_on_product_by,tax_status,discount_percentage,addon_discount)
          SELECT 395,91593,price,item_details,variation,add_ons,0,discount_type,quantity,0,variant,'2026-10-11 05:00:00','2026-10-11 05:00:00',total_add_on_price,category_id,discount_on_product_by,tax_status,0,addon_discount FROM order_details WHERE id=90;
