CREATE TABLE customers (
  customer_id   BIGINT PRIMARY KEY,
  first_name    TEXT,
  last_name     TEXT,
  address       TEXT,
  email         TEXT,
  phone_number  TEXT
);

CREATE TABLE suppliers (
  supplier_id   BIGINT PRIMARY KEY,
  supplier_name TEXT,
  contact_name  TEXT,
  address       TEXT,
  phone_number  TEXT,
  email         TEXT
);

CREATE TABLE products (
  product_id    BIGINT PRIMARY KEY,
  product_name  TEXT,
  category      TEXT,
  price         NUMERIC(12,2),
  supplier_id   BIGINT REFERENCES suppliers(supplier_id)
);

CREATE TABLE orders (
  order_id     BIGINT PRIMARY KEY,
  order_date   DATE,
  customer_id  BIGINT REFERENCES customers(customer_id),
  total_price  NUMERIC(12,2)
);

CREATE TABLE order_items (
  order_item_id     BIGINT PRIMARY KEY,
  order_id          BIGINT REFERENCES orders(order_id),
  product_id        BIGINT REFERENCES products(product_id),
  quantity          INT,
  price_at_purchase NUMERIC(12,2)
);

CREATE TABLE payment (
  payment_id        BIGINT PRIMARY KEY,
  order_id          BIGINT REFERENCES orders(order_id),
  payment_method    TEXT,
  amount            NUMERIC(12,2),
  transaction_status TEXT
);

CREATE TABLE shipments (
  shipment_id     BIGINT PRIMARY KEY,
  order_id        BIGINT REFERENCES orders(order_id),
  shipment_date   DATE,
  carrier         TEXT,
  tracking_number TEXT,
  delivery_date   DATE,
  shipment_status TEXT
);

CREATE TABLE reviews (
  review_id    BIGINT PRIMARY KEY,
  product_id   BIGINT, -- временно убираем FK, чтобы не было ошибки
  customer_id  BIGINT,
  rating       INT CHECK (rating BETWEEN 1 AND 5),
  review_text  TEXT,
  review_date  DATE
);
