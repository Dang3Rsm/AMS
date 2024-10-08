DELIMITER $$

CREATE TRIGGER order_completed_trigger
AFTER UPDATE ON client_orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'Completed' THEN
        -- Check if the stock already exists in the portfolio
        IF EXISTS (SELECT 1 
                    FROM client_portfolio 
                    WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id) THEN
            -- Update the existing record
            UPDATE client_portfolio
            SET 
                quantity = quantity + NEW.quantity,
                average_price = (average_price * quantity + NEW.price * NEW.quantity) / (quantity + NEW.quantity),
                last_updated = NOW()
            WHERE user_id = NEW.client_id AND stock_id = NEW.stock_id;
        ELSE
            -- Insert a new record
            INSERT INTO client_portfolio (user_id, stock_id, quantity, average_price, last_updated)
            VALUES (NEW.client_id, NEW.stock_id, NEW.quantity, NEW.price, NOW());
        END IF;
    END IF;
END $$

DELIMITER ;
