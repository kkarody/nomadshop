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
    "sample_limit": """
        SELECT * FROM orders LIMIT 10;
    """,

    "monthly_revenue": """
        WITH monthly AS (
          SELECT DATE_TRUNC('month', o.order_date) AS mon,
                 SUM(oi.quantity * oi.price_at_purchase) AS revenue
          FROM orders o
          JOIN order_items oi ON oi.order_id = o.order_id
          GROUP BY 1
        )
        SELECT mon, revenue
        FROM monthly
        ORDER BY mon;
    """,

    "top_products": """
        SELECT p.product_id, p.product_name,
               SUM(oi.quantity * oi.price_at_purchase) AS revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 10;
    """,

    "average_order_value": """
        SELECT ROUND(AVG(total_price),2) AS avg_order_value
        FROM orders;
    """,

    "payment_methods": """
        SELECT payment_method, COUNT(*) AS cnt, ROUND(SUM(amount),2) AS total
        FROM payment
        GROUP BY payment_method
        ORDER BY total DESC;
    """,

    "shipment_speed": """
        SELECT carrier,
               ROUND(AVG(delivery_date - shipment_date),2) AS avg_days
        FROM shipments
        WHERE delivery_date IS NOT NULL AND shipment_date IS NOT NULL
        GROUP BY carrier
        ORDER BY avg_days;
    """,

    "customer_top_spenders": """
        SELECT c.customer_id, c.first_name, c.last_name,
               ROUND(SUM(o.total_price),2) AS total_spent
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
        LIMIT 10;
    """,

    "product_ratings": """
        SELECT p.product_name,
               ROUND(AVG(r.rating),2) AS avg_rating,
               COUNT(r.review_id) AS reviews_count
        FROM reviews r
        JOIN products p ON r.product_id = p.product_id
        GROUP BY p.product_name
        HAVING COUNT(r.review_id) > 5
        ORDER BY avg_rating DESC, reviews_count DESC
        LIMIT 10;
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
