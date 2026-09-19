import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Accept data directory as command-line argument, default to data/raw
RAW_DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else "data/raw"

FILE_TABLE_MAP = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "category_translation",
}

def load_csv_to_raw(file_name, table_name):
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    print(f"Loading {file_name} -> raw.{table_name} ...")
    df = pd.read_csv(file_path)
    df.to_sql(
        table_name,
        engine,
        schema="raw",
        if_exists="replace",
        index=False,
    )
    print(f"  Loaded {len(df)} rows.")

def main():
    print(f"Loading data from: {RAW_DATA_DIR}")
    for file_name, table_name in FILE_TABLE_MAP.items():
        load_csv_to_raw(file_name, table_name)
    print("Raw load complete.")

if __name__ == "__main__":
    main()