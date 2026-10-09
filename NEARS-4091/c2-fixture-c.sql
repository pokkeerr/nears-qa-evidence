-- admin parcel callers (cloned from parcel fixtures 9211 / 9213)
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=9211;
UPDATE t_o SET id=9215, order_status='accepted', delivery_man_id=1; INSERT INTO orders SELECT * FROM t_o;
DROP TEMPORARY TABLE IF EXISTS t_p; CREATE TEMPORARY TABLE t_p AS SELECT * FROM orders WHERE id=9213;
UPDATE t_p SET id=9216; INSERT INTO orders SELECT * FROM t_p;
INSERT INTO parcel_cancellations (order_id,reason,cancel_by,note,return_otp,return_fee,return_fee_payment_status,before_pickup,created_at,updated_at) VALUES (9216,'[]','deliveryman','qa4091',1234,0,'unpaid',0,NOW(),NOW());
