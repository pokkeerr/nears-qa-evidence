-- NEARS-4049 QA fixtures: applied ONLY against scratch DB nears_n4049_qa (copy of multi_food_db)
-- F0 stores open all day (QA clock 23:xx Asia/Dubai is outside 08:00-22:00)
UPDATE store_schedule SET opening_time='00:00:00', closing_time='23:59:59' WHERE store_id IN (1,2,3,4);
-- F1 flat campaign, clone of item_campaigns row 13 with overrides
INSERT INTO item_campaigns (title,image,description,status,admin_id,start_date,end_date,start_time,end_time,category_id,category_ids,variations,add_ons,attributes,choice_options,price,tax,tax_type,discount,discount_type,store_id,created_at,updated_at,veg,module_id,stock,unit_id,food_variations,slug,maximum_cart_quantity)
SELECT 'NEARS-4049 Flat Campaign',image,description,1,1,'2026-08-19','2027-08-19',NULL,NULL,1,'[{"id":1,"position":1}]','[]','[]',attributes,choice_options,25.00,0,'percent',5.00,'amount',2,NOW(),NOW(),0,1,100,unit_id,'[]','nears-4049-flat-campaign',NULL FROM item_campaigns WHERE id=13;
-- F2 variation + flat (store 2)
UPDATE items SET discount=20.00, discount_type='amount' WHERE id=84;
-- F1b: the grocery home has no campaign surface (JustForYouView only on food/shop homes), so a second flat campaign on the ecommerce store 91116 (module 9)
UPDATE store_schedule SET opening_time='00:00:00', closing_time='23:59:59' WHERE store_id IN (91116,91125);
INSERT INTO item_campaigns (title,image,description,status,admin_id,start_date,end_date,start_time,end_time,category_id,category_ids,variations,add_ons,attributes,choice_options,price,tax,tax_type,discount,discount_type,store_id,created_at,updated_at,veg,module_id,stock,unit_id,food_variations,slug,maximum_cart_quantity)
SELECT 'NEARS-4049 Flat Campaign Shop',image,description,1,1,'2026-08-19','2027-08-19',NULL,NULL,1,'[{"id":1,"position":1}]','[]','[]',attributes,choice_options,25.00,0,'percent',5.00,'amount',91116,NOW(),NOW(),0,9,100,unit_id,'[]','nears-4049-flat-campaign-shop',NULL FROM item_campaigns WHERE id=13;
UPDATE items SET discount=2.00, discount_type='amount' WHERE id=17;
UPDATE items SET available_time_starts='00:00:00', available_time_ends='23:59:59' WHERE id=17;
