import pandas as pd
import os

RAW_DIR = "data/raw"
SAMPLE_DIR = "data/sample"

os.makedirs(SAMPLE_DIR, exist_ok=True)

# --------------------------------
# 1. Load original datasets
# --------------------------------

orders = pd.read_csv(
    os.path.join(RAW_DIR, "olist_orders_dataset.csv")
)

order_items = pd.read_csv(
    os.path.join(RAW_DIR, "olist_order_items_dataset.csv")
)

customers = pd.read_csv(
    os.path.join(RAW_DIR, "olist_customers_dataset.csv")
)

products = pd.read_csv(
    os.path.join(RAW_DIR, "olist_products_dataset.csv")
)

sellers = pd.read_csv(
    os.path.join(RAW_DIR, "olist_sellers_dataset.csv")
)

category_translation = pd.read_csv(
    os.path.join(RAW_DIR, "product_category_name_translation.csv")
)

# --------------------------------
# 2. Select 50 orders
# --------------------------------

sample_orders = orders.head(50)

order_ids = sample_orders["order_id"]

# --------------------------------
# 3. Select matching order items
# --------------------------------

sample_order_items = order_items[
    order_items["order_id"].isin(order_ids)
]

# --------------------------------
# 4. Select matching customers
# --------------------------------

customer_ids = sample_orders["customer_id"]

sample_customers = customers[
    customers["customer_id"].isin(customer_ids)
]

# --------------------------------
# 5. Select matching products
# --------------------------------

product_ids = sample_order_items["product_id"].unique()

sample_products = products[
    products["product_id"].isin(product_ids)
]

# --------------------------------
# 6. Select matching sellers
# --------------------------------

seller_ids = sample_order_items["seller_id"].unique()

sample_sellers = sellers[
    sellers["seller_id"].isin(seller_ids)
]

# --------------------------------
# 7. Save using YOUR pipeline names
# --------------------------------

sample_orders.to_csv(
    os.path.join(SAMPLE_DIR, "olist_orders_dataset.csv"),
    index=False
)

sample_order_items.to_csv(
    os.path.join(SAMPLE_DIR, "olist_order_items_dataset.csv"),
    index=False
)

sample_customers.to_csv(
    os.path.join(SAMPLE_DIR, "olist_customers_dataset.csv"),
    index=False
)

sample_products.to_csv(
    os.path.join(SAMPLE_DIR, "olist_products_dataset.csv"),
    index=False
)

sample_sellers.to_csv(
    os.path.join(SAMPLE_DIR, "olist_sellers_dataset.csv"),
    index=False
)

# Keep all category translations
category_translation.to_csv(
    os.path.join(SAMPLE_DIR, "product_category_name_translation.csv"),
    index=False
)

# --------------------------------
# 8. Show results
# --------------------------------

print("\nSample data created successfully!\n")

print(f"Orders: {len(sample_orders)}")
print(f"Order items: {len(sample_order_items)}")
print(f"Customers: {len(sample_customers)}")
print(f"Products: {len(sample_products)}")
print(f"Sellers: {len(sample_sellers)}")
print(f"Category translations: {len(category_translation)}")