DELIMITER $$

DROP TRIGGER IF EXISTS order_completed_trigger $$

CREATE TRIGGER order_completed_trigger
AFTER UPDATE ON client_orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'Completed' AND OLD.status != 'Completed' THEN
        -- Handle Stock Orders
        IF NEW.stock_id IS NOT NULL THEN
            INSERT INTO nasdaq_equity_transactions (user_id, stock_id, transaction_type, quantity, price)
            VALUES (NEW.client_id, NEW.stock_id, NEW.order_type, NEW.quantity, NEW.price);

            IF NEW.order_type = 'BUY' THEN
                IF EXISTS (SELECT 1 FROM client_portfolio WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id) THEN
                    UPDATE client_portfolio
                    SET average_price = ((average_price * quantity) + (NEW.price * NEW.quantity)) / (quantity + NEW.quantity),
                        quantity = quantity + NEW.quantity,
                        last_updated = NOW()
                    WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id;
                ELSE
                    INSERT INTO client_portfolio (user_id, stock_id, quantity, average_price, last_updated)
                    VALUES (NEW.client_id, NEW.stock_id, NEW.quantity, NEW.price, NOW());
                END IF;
            ELSEIF NEW.order_type = 'SELL' THEN
                UPDATE client_portfolio
                SET quantity = GREATEST(0, quantity - NEW.quantity),
                    last_updated = NOW()
                WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id;

                DELETE FROM client_portfolio WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id AND quantity <= 0;
            END IF;
        END IF;

        -- Handle Fund Orders
        IF NEW.fund_id IS NOT NULL THEN
            INSERT INTO fund_transactions (user_id, fund_id, transaction_type, quantity, price)
            VALUES (NEW.client_id, NEW.fund_id, NEW.order_type, NEW.quantity, NEW.price);

            IF NEW.order_type = 'BUY' THEN
                IF EXISTS (SELECT 1 FROM client_portfolio WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id) THEN
                    UPDATE client_portfolio
                    SET average_price = ((average_price * quantity) + (NEW.price * NEW.quantity)) / (quantity + NEW.quantity),
                        quantity = quantity + NEW.quantity,
                        last_updated = NOW()
                    WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id;
                ELSE
                    INSERT INTO client_portfolio (user_id, fund_id, quantity, average_price, last_updated)
                    VALUES (NEW.client_id, NEW.fund_id, NEW.quantity, NEW.price, NOW());
                END IF;
            ELSEIF NEW.order_type = 'SELL' THEN
                UPDATE client_portfolio
                SET quantity = GREATEST(0, quantity - NEW.quantity),
                    last_updated = NOW()
                WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id;

                DELETE FROM client_portfolio WHERE user_id = NEW.client_id AND fund_id = NEW.fund_id AND quantity <= 0;
            END IF;
        END IF;
    END IF;
END $$

DELIMITER ;
