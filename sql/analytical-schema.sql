CREATE SCHEMA IF NOT EXISTS analytics;

-- Dimension: Date
DROP TABLE IF EXISTS analytics.dim_date;
CREATE TABLE analytics.dim_date AS
SELECT
    d::date AS date,
    EXTRACT(YEAR FROM d) AS year,
    EXTRACT(MONTH FROM d) AS month,
    EXTRACT(DAY FROM d) AS day,
    EXTRACT(QUARTER FROM d) AS quarter,
    TO_CHAR(d, 'Day') AS day_name,
    TO_CHAR(d, 'Month') AS month_name,
    EXTRACT(DOW FROM d) AS day_of_week,
    CASE WHEN EXTRACT(DOW FROM d) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
FROM generate_series(
    '2016-01-01'::date,
    '2018-12-31'::date,
    '1 day'::interval
) AS d;

-- Dimension: Customers
DROP TABLE IF EXISTS analytics.dim_customers;
CREATE TABLE analytics.dim_customers AS
SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state,
    customer_zip_code_prefix
FROM staging.customers;

-- Dimension: Products
DROP TABLE IF EXISTS analytics.dim_products;
CREATE TABLE analytics.dim_products AS
SELECT
    p.product_id,
    COALESCE(ct.product_category_name_english, p.product_category_name) AS product_category,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM staging.products p
LEFT JOIN staging.category_translation ct
    ON p.product_category_name = ct.product_category_name;

-- Dimension: Sellers
DROP TABLE IF EXISTS analytics.dim_sellers;
CREATE TABLE analytics.dim_sellers AS
SELECT
    seller_id,
    seller_city,
    seller_state,
    seller_zip_code_prefix
FROM staging.sellers;

-- Fact: Order Items
DROP TABLE IF EXISTS analytics.fact_order_items;
CREATE TABLE analytics.fact_order_items AS
SELECT
    oi.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    o.order_purchase_ts::date AS order_date,
    o.order_status,
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_item_value,
    o.order_delivered_customer_ts,
    o.order_estimated_delivery_ts,
    CASE 
        WHEN o.order_delivered_customer_ts IS NOT NULL 
        THEN EXTRACT(DAY FROM (o.order_delivered_customer_ts - o.order_purchase_ts))
        ELSE NULL 
    END AS delivery_days
FROM staging.order_items oi
JOIN staging.orders o ON oi.order_id = o.order_id;

-- View: Monthly Revenue (running total)
CREATE OR REPLACE VIEW analytics.vw_monthly_revenue AS
SELECT
    d.year,
    d.month,
    SUM(f.total_item_value) AS monthly_revenue,
    SUM(SUM(f.total_item_value)) OVER (ORDER BY d.year, d.month) AS running_total_revenue
FROM analytics.fact_order_items f
JOIN analytics.dim_date d ON f.order_date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- View: Top Products by Category
CREATE OR REPLACE VIEW analytics.vw_top_products_by_category AS
SELECT
    product_category,
    product_id,
    total_revenue,
    RANK() OVER (PARTITION BY product_category ORDER BY total_revenue DESC) AS rank_in_category
FROM (
    SELECT
        p.product_category,
        f.product_id,
        SUM(f.total_item_value) AS total_revenue
    FROM analytics.fact_order_items f
    JOIN analytics.dim_products p ON f.product_id = p.product_id
    GROUP BY p.product_category, f.product_id
) sub;

-- View: Top Customers by Spend
CREATE OR REPLACE VIEW analytics.vw_top_customers AS
SELECT
    c.customer_id,
    c.customer_city,
    c.customer_state,
    SUM(f.total_item_value) AS total_spend,
    COUNT(DISTINCT f.order_id) AS total_orders,
    RANK() OVER (ORDER BY SUM(f.total_item_value) DESC) AS spend_rank
FROM analytics.fact_order_items f
JOIN analytics.dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_city, c.customer_state;