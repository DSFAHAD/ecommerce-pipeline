import os
from sqlalchemy import create_engine, text
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

failures = []

def check(description, query, expected_pass_condition):
    with engine.connect() as conn:
        result = conn.execute(text(query)).scalar()
        passed = expected_pass_condition(result)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {description} (value={result})")
        if not passed:
            failures.append(description)

def main():
    print("Running data quality checks...\n")

    # Row count checks — tables should not be empty
    check(
        "fact_order_items has rows",
        "SELECT COUNT(*) FROM analytics.fact_order_items",
        lambda v: v > 0
    )
    check(
        "dim_customers has rows",
        "SELECT COUNT(*) FROM analytics.dim_customers",
        lambda v: v > 0
    )
    check(
        "dim_products has rows",
        "SELECT COUNT(*) FROM analytics.dim_products",
        lambda v: v > 0
    )

    # Null checks — key columns should never be null
    check(
        "fact_order_items.order_id has no nulls",
        "SELECT COUNT(*) FROM analytics.fact_order_items WHERE order_id IS NULL",
        lambda v: v == 0
    )
    check(
        "fact_order_items.customer_id has no nulls",
        "SELECT COUNT(*) FROM analytics.fact_order_items WHERE customer_id IS NULL",
        lambda v: v == 0
    )

    # Referential integrity — every customer_id in fact should exist in dim_customers
    check(
        "All fact customer_ids exist in dim_customers",
        """
        SELECT COUNT(*) FROM analytics.fact_order_items f
        LEFT JOIN analytics.dim_customers c ON f.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """,
        lambda v: v == 0
    )

    # Value sanity checks — no negative prices
    check(
        "No negative prices in fact_order_items",
        "SELECT COUNT(*) FROM analytics.fact_order_items WHERE price < 0",
        lambda v: v == 0
    )

    print("\n--- Summary ---")
    if failures:
        print(f"{len(failures)} check(s) FAILED:")
        for f in failures:
            print(f"  - {f}")
        exit(1)
    else:
        print("All checks passed!")

if __name__ == "__main__":
    main()