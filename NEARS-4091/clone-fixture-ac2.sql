-- clone only. S1: user 5 robert (ref_by 4 sophie), all rewards. S2: user 2 emily, clamp. S3: user 3 michael, delivered partially_paid (manual) + loyalty only
UPDATE users SET ref_by=4 WHERE id=5;
CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=166;
UPDATE t_o SET id=9101, user_id=5, payment_method='digital_payment', payment_status='paid', order_status='refund_requested', order_amount=20, delivery_charge=2, dm_tips=1, transaction_reference='qa4091-ref-1', refund_requested=now();
INSERT INTO orders SELECT * FROM t_o;
UPDATE t_o SET id=9102, user_id=2, order_amount=12, delivery_charge=0, dm_tips=0, transaction_reference='qa4091-ref-2';
INSERT INTO orders SELECT * FROM t_o;
UPDATE t_o SET id=9103, user_id=3, payment_status='partially_paid', partially_paid_amount=5, order_amount=15, payment_method='partial_payment', transaction_reference='qa4091-ref-3';
INSERT INTO orders SELECT * FROM t_o;
CREATE TEMPORARY TABLE t_t AS SELECT * FROM order_transactions WHERE order_id=166;
SET @mx=(SELECT MAX(id) FROM order_transactions);
UPDATE t_t SET id=@mx+1, order_id=9101; INSERT INTO order_transactions SELECT * FROM t_t;
UPDATE t_t SET id=@mx+2, order_id=9102; INSERT INTO order_transactions SELECT * FROM t_t;
UPDATE t_t SET id=@mx+3, order_id=9103; INSERT INTO order_transactions SELECT * FROM t_t;
INSERT INTO refunds (order_id,user_id,order_status,customer_reason,refund_amount,refund_status,refund_method,created_at,updated_at) VALUES (9101,5,'refund_requested','qa',17,'pending','manual',now(),now()),(9102,2,'refund_requested','qa',12,'pending','manual',now(),now()),(9103,3,'refund_requested','qa',5,'pending','manual',now(),now());
INSERT INTO cash_backs (id,title,customer_id,cashback_type,same_user_limit,total_used,cashback_amount,min_purchase,max_discount,status,created_at,updated_at) VALUES (9001,'qa4091','["all"]','amount',5,2,3,0,0,1,now(),now());
INSERT INTO cash_back_histories (cash_back_id,order_id,user_id,cashback_type,calculated_amount,cashback_amount,min_purchase,max_discount,created_at,updated_at) VALUES (9001,9101,5,'amount',3,3,0,0,now(),now()),(9001,9102,2,'amount',4,4,0,0,now(),now());
