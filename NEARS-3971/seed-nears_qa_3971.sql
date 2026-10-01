-- NEARS-3971 QA seed — applied ONLY to the private copy nears_qa_3971 (never multi_food_db).
-- Adapted from the NEARS-3960 seed. Template row: item 102 (Tomatoes, store 1, grocery module 1).
USE nears_qa_3971;
DELETE FROM carts WHERE user_id = 3;
-- QA runs ~07:40 Asia/Dubai; stores 1/2 open 08:00 -> open around the clock (copy only)
UPDATE store_schedule SET opening_time = '00:00:00', closing_time = '23:59:59' WHERE store_id IN (1,2);
INSERT INTO items (name,description,image,category_id,category_ids,variations,add_ons,attributes,choice_options,price,tax,tax_type,discount,discount_type,available_time_starts,available_time_ends,veg,status,store_id,created_at,updated_at,order_count,avg_rating,rating_count,rating,module_id,stock,unit_id,pack_size_value,pack_size_unit,images,food_variations,slug,recommended,organic,maximum_cart_quantity,is_approved,is_halal)
SELECT v.name,description,image,category_id,category_ids,v.variations,'[]',v.attrs,v.choice,v.price,tax,tax_type,v.disc,v.dtype,'00:00:00','23:59:59',veg,1,v.sid,NOW(),NOW(),0,0,0,rating,module_id,500,unit_id,pack_size_value,pack_size_unit,images,food_variations,v.slug,0,organic,NULL,1,is_halal
FROM items t JOIN (
  SELECT 'QA3971 Alpha20' name, 20.00 price, 0.00 disc, 'percent' dtype, '[]' variations, '[]' attrs, '[]' choice, 'qa3971-alpha20' slug, 1 sid
  UNION ALL SELECT 'QA3971 Beta10', 10.00, 0.00, 'percent', '[]', '[]', '[]', 'qa3971-beta10', 1
  UNION ALL SELECT 'QA3971 FlashRice20', 20.00, 18.00, 'percent', '[]', '[]', '[]', 'qa3971-flashrice20', 1
  UNION ALL SELECT 'QA3971 ExampleA', 10.00, 3.00, 'amount', '[{"type":"Large","price":40,"stock":500}]', '["1"]', '[{"name":"choice_1","title":"Size","options":["Large"]}]', 'qa3971-examplea', 2
) v WHERE t.id = 102;
-- running grocery flash sale 1: FlashRice20 at 10%
INSERT INTO flash_sale_items (flash_sale_id,item_id,stock,sold,available_stock,discount_type,discount,discount_amount,price,status,created_at,updated_at)
SELECT 1, id, 50, 0, 50, 'percent', 10, 2.000, 20.000, 1, NOW(), NOW() FROM items WHERE slug = 'qa3971-flashrice20';
-- store 1 discount row id 1 -> case 11 (10%, min 0, cap 1.00); store 2 -> case 22 (10%, cap 3.50)
UPDATE discounts SET discount = 10.00, discount_type = 'percent', min_purchase = 0.00, max_discount = 1.00, start_time = '00:00:00', end_time = '23:59:59' WHERE id = 1 AND store_id = 1;
INSERT INTO discounts (start_date,end_date,start_time,end_time,min_purchase,max_discount,discount,discount_type,store_id,created_at,updated_at)
VALUES ('2026-09-01','2027-09-01','00:00:00','23:59:59',0.00,3.50,10.00,'percent',2,NOW(),NOW());
-- coupons (grocery module 1): P10 min 28 (between case-11 legacy 27 and server 29); HI min 36.75 (between case-22 server 36.50 and legacy 37.00)
INSERT INTO coupons (title,code,start_date,expire_date,min_purchase,max_discount,discount,discount_type,coupon_type,`limit`,status,created_at,updated_at,data,total_uses,module_id,created_by,customer_id,slug,store_id)
VALUES ('NEARS-3971 QA P10 min28','QA3971P10','2026-09-01','2027-09-01',28.00,0.00,10.00,'percent','default',NULL,1,NOW(),NOW(),'',0,1,'admin','["all"]','qa3971p10',NULL),
       ('NEARS-3971 QA P10 min36.75','QA3971HI','2026-09-01','2027-09-01',36.75,0.00,10.00,'percent','default',NULL,1,NOW(),NOW(),'',0,1,'admin','["all"]','qa3971hi',NULL);
-- per-cell edits (store 1 minimum_order, discount max, free-delivery option/threshold, flag 228) are logged in progress.md
