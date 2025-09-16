--Define 10 analytical topics for my project

-- 1. Revenue by month
SELECT DATE_TRUNC('month', o.order_date) AS month,
       SUM(oi.quantity * oi.price_at_purchase) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY 1
ORDER BY 1;

-- 2. Top 10 products by revenue
SELECT p.product_name,
       SUM(oi.quantity * oi.price_at_purchase) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;

-- 3. Average order value
SELECT ROUND(AVG(total_price), 2) AS avg_order_value
FROM orders;

-- 4. Top 10 customers by total purchases
SELECT c.customer_id, c.first_name, c.last_name,
    SUM(o.total_price) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 10;

-- 5. Payment method popularity
SELECT payment_method,
    COUNT(*) AS cnt,
    SUM(amount) AS total_amount
FROM payment
GROUP BY payment_method
ORDER BY total_amount DESC;

-- 6. Average delivery time by carrier
SELECT carrier,
    ROUND(AVG(delivery_date - shipment_date), 2) AS avg_days
FROM shipments
WHERE delivery_date IS NOT NULL AND shipment_date IS NOT NULL
GROUP BY carrier
ORDER BY avg_days;

-- 7. Average product rating (top 10)
SELECT p.product_name,
    ROUND(AVG(r.rating),2) AS avg_rating,
    COUNT(*) AS reviews_count
FROM reviews r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.product_name
ORDER BY avg_rating DESC
LIMIT 10;

-- 8. Number of orders per customer (top 10)
SELECT c.first_name, c.last_name,
    COUNT(o.order_id) AS orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.first_name, c.last_name
ORDER BY orders_count DESC
LIMIT 10;

-- 9. Product categories by total sales
SELECT p.category,
    SUM(oi.quantity * oi.price_at_purchase) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- 10. Average order amount by year
SELECT DATE_PART('year', order_date) AS year,
    ROUND(AVG(total_price),2) AS avg_order
FROM orders
GROUP BY 1
ORDER BY 1;
