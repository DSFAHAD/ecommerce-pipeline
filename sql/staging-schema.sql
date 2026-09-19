CREATE SCHEMA IF NOT EXISTS staging;

-- Orders
DROP TABLE IF EXISTS staging.orders;
CREATE TABLE staging.orders AS
SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp::timestamp AS order_purchase_ts,
    order_approved_at::timestamp AS order_approved_ts,
    order_delivered_carrier_date::timestamp AS order_delivered_carrier_ts,
    order_delivered_customer_date::timestamp AS order_delivered_customer_ts,
    order_estimated_delivery_date::timestamp AS order_estimated_delivery_ts
FROM raw.orders
WHERE order_id IS NOT NULL;

-- Customers
DROP TABLE IF EXISTS staging.customers;
CREATE TABLE staging.customers AS
SELECT DISTINCT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    INITCAP(customer_city) AS customer_city,
    UPPER(customer_state) AS customer_state
FROM raw.customers
WHERE customer_id IS NOT NULL;

-- Order Items
DROP TABLE IF EXISTS staging.order_items;
CREATE TABLE staging.order_items AS
SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date::timestamp AS shipping_limit_ts,
    price,
    freight_value
FROM raw.order_items
WHERE order_id IS NOT NULL
  AND price >= 0
  AND freight_value >= 0;

-- Products
DROP TABLE IF EXISTS staging.products;
CREATE TABLE staging.products AS
SELECT
    product_id,
    COALESCE(product_category_name, 'unknown') AS product_category_name,
    product_name_lenght AS product_name_length,
    product_description_lenght AS product_description_length,
    COALESCE(product_photos_qty, 0) AS product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM raw.products
WHERE product_id IS NOT NULL;

-- Sellers
DROP TABLE IF EXISTS staging.sellers;
CREATE TABLE staging.sellers AS
SELECT DISTINCT
    seller_id,
    seller_zip_code_prefix,
    INITCAP(seller_city) AS seller_city,
    UPPER(seller_state) AS seller_state
FROM raw.sellers
WHERE seller_id IS NOT NULL;

-- Order Payments
DROP TABLE IF EXISTS staging.order_payments;
CREATE TABLE staging.order_payments AS
SELECT
    order_id,
    payment_sequential,
    LOWER(payment_type) AS payment_type,
    payment_installments,
    payment_value
FROM raw.order_payments
WHERE order_id IS NOT NULL
  AND payment_value >= 0;

-- Order Reviews
DROP TABLE IF EXISTS staging.order_reviews;
CREATE TABLE staging.order_reviews AS
SELECT
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date::timestamp AS review_creation_ts,
    review_answer_timestamp::timestamp AS review_answer_ts
FROM raw.order_reviews
WHERE review_id IS NOT NULL
  AND order_id IS NOT NULL;

-- Category Translation
DROP TABLE IF EXISTS staging.category_translation;
CREATE TABLE staging.category_translation AS
SELECT DISTINCT
    product_category_name,
    product_category_name_english
FROM raw.category_translation
WHERE product_category_name IS NOT NULL;