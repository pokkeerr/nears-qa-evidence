-- second batch: round c2 first vendor demo ran before the trigger existed (9201/9202 canceled normally = positive control)
DROP TEMPORARY TABLE IF EXISTS t_o; CREATE TEMPORARY TABLE t_o AS SELECT * FROM orders WHERE id=9207;
UPDATE t_o SET id=9221; INSERT INTO orders SELECT * FROM t_o;
UPDATE t_o SET id=9222, payment_status='partially_paid', payment_method='partial_payment', partially_paid_amount=10; INSERT INTO orders SELECT * FROM t_o;
DROP TEMPORARY TABLE IF EXISTS t_d; CREATE TEMPORARY TABLE t_d AS SELECT * FROM order_details WHERE order_id=9207;
UPDATE t_d SET id=92210, order_id=9221; INSERT INTO order_details SELECT * FROM t_d;
UPDATE t_d SET id=92220, order_id=9222; INSERT INTO order_details SELECT * FROM t_d;
