-- NEARS-3960 QA seed — applied ONLY to the private copy nears_qa_3960 (never multi_food_db).
-- Template row: item 102 (Tomatoes, store 1, grocery module 1) / item 16 (store 4, food module 2).
USE nears_qa_3960;

-- store 1: drop the order minimum so single-line cells (18.00 pay) are placeable
UPDATE stores SET minimum_order = 0 WHERE id = 1;
-- clean customer cart (michael.brown id 3)
DELETE FROM carts WHERE user_id = 3;

-- grocery items in store 1
INSERT INTO items (name,description,image,category_id,category_ids,variations,add_ons,attributes,choice_options,price,tax,tax_type,discount,discount_type,available_time_starts,available_time_ends,veg,status,store_id,created_at,updated_at,order_count,avg_rating,rating_count,rating,module_id,stock,unit_id,pack_size_value,pack_size_unit,images,food_variations,slug,recommended,organic,maximum_cart_quantity,is_approved,is_halal)
SELECT v.name,description,image,category_id,category_ids,v.variations,'[]',v.attrs,v.choice,v.price,tax,tax_type,v.disc,v.dtype,available_time_starts,available_time_ends,veg,1,store_id,NOW(),NOW(),0,0,0,rating,module_id,500,unit_id,pack_size_value,pack_size_unit,images,food_variations,v.slug,0,organic,NULL,1,is_halal
FROM items t JOIN (
  SELECT 'QA3960 Loaf100 Own5' name, 100.00 price, 5.00 disc, 'percent' dtype, '[]' variations, '[]' attrs, '[]' choice, 'qa3960-loaf100-own5' slug
  UNION ALL SELECT 'QA3960 Loaf100 Own8', 100.00, 8.00, 'percent', '[]', '[]', '[]', 'qa3960-loaf100-own8'
  UNION ALL SELECT 'QA3960 Alpha20', 20.00, 0.00, 'percent', '[]', '[]', '[]', 'qa3960-alpha20'
  UNION ALL SELECT 'QA3960 Beta10', 10.00, 0.00, 'percent', '[]', '[]', '[]', 'qa3960-beta10'
  UNION ALL SELECT 'QA3960 ExampleA', 10.00, 3.00, 'amount', '[{"type":"Large","price":40,"stock":500}]', '["1"]', '[{"name":"choice_1","title":"Size","options":["Large"]}]', 'qa3960-examplea'
  UNION ALL SELECT 'QA3960 ExampleB', 50.00, 3.00, 'amount', '[{"type":"Small","price":20,"stock":500}]', '["1"]', '[{"name":"choice_1","title":"Size","options":["Small"]}]', 'qa3960-exampleb'
  UNION ALL SELECT 'QA3960 FlashRice20', 20.00, 18.00, 'percent', '[]', '[]', '[]', 'qa3960-flashrice20'
) v WHERE t.id = 102;

-- running grocery flash sale 1: FlashRice20 at 10%
INSERT INTO flash_sale_items (flash_sale_id,item_id,stock,sold,available_stock,discount_type,discount,discount_amount,price,status,created_at,updated_at)
SELECT 1, id, 50, 0, 50, 'percent', 10, 2.000, 20.000, 1, NOW(), NOW() FROM items WHERE slug = 'qa3960-flashrice20';

-- food store 4 (Burger Palace): add-on 5.00 + two plain items, one carrying the add-on
INSERT INTO add_ons (name,price,created_at,updated_at,store_id,status) VALUES ('QA3960 Addon5',5.00,NOW(),NOW(),4,1);
INSERT INTO items (name,description,image,category_id,category_ids,variations,add_ons,attributes,choice_options,price,tax,tax_type,discount,discount_type,available_time_starts,available_time_ends,veg,status,store_id,created_at,updated_at,order_count,avg_rating,rating_count,rating,module_id,stock,unit_id,pack_size_value,pack_size_unit,images,food_variations,slug,recommended,organic,maximum_cart_quantity,is_approved,is_halal)
SELECT v.name,description,image,category_id,category_ids,'[]',v.addons,'[]','[]',v.price,tax,tax_type,0,'percent','00:00:00','23:59:59',veg,1,store_id,NOW(),NOW(),0,0,0,rating,module_id,500,unit_id,pack_size_value,pack_size_unit,images,'[]',v.slug,0,organic,NULL,1,is_halal
FROM items t JOIN (
  SELECT 'QA3960 FoodA20' name, 20.00 price, CONCAT('["',(SELECT MAX(id) FROM add_ons WHERE name='QA3960 Addon5'),'"]') addons, 'qa3960-fooda20' slug
  UNION ALL SELECT 'QA3960 FoodB10', 10.00, '[]', 'qa3960-foodb10'
) v WHERE t.id = 16;

-- store 4 discount (case 4 shape): 10%, min 32, no cap
INSERT INTO discounts (start_date,end_date,start_time,end_time,min_purchase,max_discount,discount,discount_type,store_id,created_at,updated_at)
VALUES ('2026-09-01','2027-09-01','00:00:00','23:59:59',32.00,0.00,10.00,'percent',4,NOW(),NOW());

-- QA runs at ~03:40 Asia/Dubai: open stores 1, 2 and 4 around the clock (copy only)
UPDATE store_schedule SET opening_time = '00:00:00', closing_time = '23:59:59' WHERE store_id IN (1,2,4);

-- Burger Palace (4) is not listed for the Dhaka address in-app; move the cell-3 seed to the listed
-- always-open food store 91112 (module 2, zone 1, tax 0)
UPDATE add_ons SET store_id = 91112 WHERE name = 'QA3960 Addon5';
UPDATE items SET store_id = 91112 WHERE name IN ('QA3960 FoodA20','QA3960 FoodB10');
UPDATE discounts SET store_id = 91112 WHERE store_id = 4 AND min_purchase = 32.00;

-- cell 8 (group basket): open store-2 item Cheddar Cheese (id 7) around the clock; flag 228 ON for cells 8/9
UPDATE items SET available_time_starts = '00:00:00', available_time_ends = '23:59:59' WHERE id = 7;
UPDATE business_settings SET value = '1' WHERE id = 228 AND `key` = 'cross_module_basket';
-- per-cell store-1 discount row edits (id 1): max/min set per cell, see progress.md
