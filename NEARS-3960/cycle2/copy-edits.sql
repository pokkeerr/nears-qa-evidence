UPDATE nears_qa_3960.discounts SET max_discount=1.00 WHERE id=1; -- cycle2 R2
UPDATE nears_qa_3960.discounts SET max_discount=999999 WHERE id=1; -- cycle2 R6/R7
UPDATE nears_qa_3960.discounts SET max_discount=5.00 WHERE id=1; -- cycle2 teardown: restored to found state
