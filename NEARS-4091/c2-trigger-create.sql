DROP TRIGGER IF EXISTS qa4091_block_refund;
DELIMITER $$
CREATE TRIGGER qa4091_block_refund BEFORE INSERT ON wallet_transactions FOR EACH ROW
BEGIN
  IF NEW.transaction_type = 'order_refund' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'qa4091 injected wallet failure';
  END IF;
END$$
DELIMITER ;
