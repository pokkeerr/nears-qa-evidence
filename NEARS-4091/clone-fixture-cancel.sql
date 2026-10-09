UPDATE orders SET payment_status='paid', payment_method='digital_payment' WHERE id IN (167,168,165,162,158,171);
UPDATE orders SET payment_status='partially_paid', payment_method='partial_payment', partially_paid_amount=2 WHERE id IN (169,170);
UPDATE orders SET confirmed=NULL, delivery_man_id=1 WHERE id=171;
UPDATE admin_wallets SET digital_received=1000 WHERE id=1;
UPDATE business_settings SET value='1' WHERE `key`='canceled_by_deliveryman';
