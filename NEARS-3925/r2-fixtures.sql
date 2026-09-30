-- COPY ONLY (multi_food_db_qa_bug3925). Mirrors the Nears3925 test setUp.
update stores set zone_id=2, latitude=24.4648, longitude=54.3783, minimum_order=0 where id in (39,1);
update stores set minimum_order=0 where id in (57,12);
update store_schedule set opening_time='00:00:00', closing_time='23:59:59' where store_id in (39,57,12,1);
update zones set digital_payment=0 where id=2;
update module_zone set delivery_charge_type='distance', per_km_shipping_charge=2.5, minimum_shipping_charge=1, maximum_shipping_charge=1000, maximum_cod_order_amount=NULL where zone_id=2 and module_id in (1,2,3);
update business_settings set value='0' where `key` in ('admin_free_delivery_status');
delete from cache;
update stores set minimum_order=0 where id in (52,54);
update stores set status=1 where id=54;
update store_schedule set opening_time='00:00:00', closing_time='23:59:59' where store_id in (52,54);
update coupons set expire_date='2027-12-31' where id=5; -- COPY ONLY (coupon expired 2026-09-06 in dump)
