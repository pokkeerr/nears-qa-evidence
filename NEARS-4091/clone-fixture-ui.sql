-- clone only; user 6 (customer@nears.com). Test-fixture rows for the AC-UI device pass.
INSERT INTO wallet_transactions (user_id,transaction_id,credit,debit,admin_bonus,balance,transaction_type,reference,created_at,updated_at) VALUES
(6,UUID(),0,3.000,0,38.000,'cashback_reversal','1234',NOW()-INTERVAL 1 MINUTE,NOW()-INTERVAL 1 MINUTE),
(6,UUID(),0,5.000,0,33.000,'referrer_reversal','1234',NOW()-INTERVAL 2 MINUTE,NOW()-INTERVAL 2 MINUTE),
(6,UUID(),0,8.500,0,28.500,'order_place','1250',NOW()-INTERVAL 3 MINUTE,NOW()-INTERVAL 3 MINUTE),
(6,UUID(),0,2.000,0,36.500,'partial_payment','1251',NOW()-INTERVAL 4 MINUTE,NOW()-INTERVAL 4 MINUTE),
(6,UUID(),4.000,0,0,38.500,'CashBack','1252',NOW()-INTERVAL 5 MINUTE,NOW()-INTERVAL 5 MINUTE);
INSERT INTO loyalty_point_transactions (user_id,transaction_id,credit,debit,balance,reference,transaction_type,created_at,updated_at) VALUES
(6,UUID(),0,10.000,40.000,'1234','loyalty_reversal',NOW()-INTERVAL 1 MINUTE,NOW()-INTERVAL 1 MINUTE),
(6,UUID(),0,20.000,50.000,'qa-redeem','point_to_wallet',NOW()-INTERVAL 2 MINUTE,NOW()-INTERVAL 2 MINUTE),
(6,UUID(),50.000,0,70.000,'1253','order_place',NOW()-INTERVAL 3 MINUTE,NOW()-INTERVAL 3 MINUTE);
