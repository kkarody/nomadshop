import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения (.env)
load_dotenv()

# Подключение к БД
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    print("✅ Connected to database")
except Exception as e:
    print("❌ Connection failed:", e)
    exit(1)

# SQL-запросы
queries = {
    # 0. Пример: первые 10 заказов
    "sample_limit": """
        SELECT * FROM orders LIMIT 10;
    """,

    # 1. Revenue by month
    "monthly_revenue": """
        SELECT DATE_TRUNC('month', o.order_date) AS month,
               SUM(oi.quantity * oi.price_at_purchase) AS revenue
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        GROUP BY 1
        ORDER BY 1;
    """,

    # 2. Top 10 products by revenue
    "top_products": """
        SELECT p.product_name,
               SUM(oi.quantity * oi.price_at_purchase) AS revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT 10;
    """,

    # 3. Average order value
    "average_order_value": """
        SELECT ROUND(AVG(total_price), 2) AS avg_order_value
        FROM orders;
    """,

    # 4. Top 10 customers by total purchases
    "top_customers": """
        SELECT c.customer_id, c.first_name, c.last_name,
               SUM(o.total_price) AS total_spent
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
        LIMIT 10;
    """,

    # 5. Payment method popularity
    "payment_methods": """
        SELECT payment_method,
               COUNT(*) AS cnt,
               SUM(amount) AS total_amount
        FROM payment
        GROUP BY payment_method
        ORDER BY total_amount DESC;
    """,

    # 6. Average delivery time by carrier
    "shipment_speed": """
        SELECT carrier,
               ROUND(AVG(delivery_date - shipment_date), 2) AS avg_days
        FROM shipments
        WHERE delivery_date IS NOT NULL AND shipment_date IS NOT NULL
        GROUP BY carrier
        ORDER BY avg_days;
    """,

    # 7. Average product rating (top 10)
    "product_ratings": """
        SELECT p.product_name,
               ROUND(AVG(r.rating),2) AS avg_rating,
               COUNT(*) AS reviews_count
        FROM reviews r
        JOIN products p ON r.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY avg_rating DESC
        LIMIT 10;
    """,

    # 8. Number of orders per customer (top 10)
    "orders_per_customer": """
        SELECT c.first_name, c.last_name,
               COUNT(o.order_id) AS orders_count
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.first_name, c.last_name
        ORDER BY orders_count DESC
        LIMIT 10;
    """,

    # 9. Product categories by total sales
    "category_revenue": """
        SELECT p.category,
               SUM(oi.quantity * oi.price_at_purchase) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
    """,

    # 10. Average order amount by year
    "yearly_avg_order": """
        SELECT DATE_PART('year', order_date) AS year,
               ROUND(AVG(total_price),2) AS avg_order
        FROM orders
        GROUP BY 1
        ORDER BY 1;
    """
}

# Выполнение запросов
with conn, conn.cursor() as cur:
    for name, q in queries.items():
        print(f"\n=== {name} ===")
        try:
            cur.execute(q)
            cols = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=cols)
            print(df.head(20).to_string(index=False))
        except Exception as e:
            print(f"⚠️ Query {name} failed:", e)

conn.close()
