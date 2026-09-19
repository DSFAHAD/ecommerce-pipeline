🛒 E-Commerce Data Engineering Pipeline

An end-to-end E-Commerce Data Engineering pipeline built with Python, PostgreSQL, SQL, and GitHub Actions.

This project demonstrates how raw e-commerce CSV data can be ingested, transformed through multiple data layers, modeled into analytical fact and dimension tables, and automatically validated using data quality checks in CI.

---

🚀 Project Overview

The pipeline processes a sample of the Olist E-Commerce dataset through a structured data engineering workflow.

The main goal is to demonstrate practical concepts such as:

- Data ingestion
- Relational data handling
- PostgreSQL database design
- Raw → Staging → Analytics architecture
- SQL transformations
- Fact and dimension modeling
- Data quality testing
- Referential integrity
- Automated CI using GitHub Actions

---

🏗️ Pipeline Architecture

                 ┌──────────────────────┐
                 │  Olist CSV Dataset   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Python Sample Data  │
                 │   sample_data.py     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Python Data Loading  │
                 │    load-raw.py       │
                 └──────────┬───────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │      PostgreSQL RAW        │
              │                            │
              │ customers                  │
              │ orders                     │
              │ order_items                │
              │ products                   │
              │ sellers                    │
              │ payments                   │
              │ reviews                    │
              │ geolocation                │
              └──────────────┬─────────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │     STAGING LAYER          │
              │       SQL Transformations  │
              │                            │
              │ Cleaning                   │
              │ Type conversions            │
              │ Null handling               │
              │ Standardization             │
              └──────────────┬─────────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │     ANALYTICS LAYER        │
              │                            │
              │ dim_date                   │
              │ dim_customers              │
              │ dim_products               │
              │ dim_sellers                │
              │ fact_order_items            │
              └──────────────┬─────────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │    Data Quality Checks     │
              │     data-quality.py        │
              │                            │
              │ Row existence              │
              │ NULL checks                │
              │ Referential integrity      │
              │ Negative value checks      │
              └──────────────┬─────────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │   GitHub Actions     │
                 │       CI ✅          │
                 └──────────────────────┘

---

🔄 Data Flow

1. Source Data

The pipeline starts with Olist e-commerce CSV files.

The sample dataset contains relational tables such as:

- Customers
- Orders
- Order Items
- Products
- Sellers
- Payments
- Reviews
- Geolocation
- Product Category Translation

---

2. Relational Sampling

The project uses "sample_data.py" to create a smaller dataset for development and CI testing.

Instead of randomly taking rows independently from every CSV, the sampling process preserves important relationships between tables.

For example:

Orders
   │
   ├── Customer
   │
   └── Order Items
          │
          ├── Product
          └── Seller

This ensures that the sample data can successfully pass relational joins.

---

3. Raw Layer

"load-raw.py" loads the sample CSV files into PostgreSQL.

The raw layer keeps the source data available before transformation.

data/sample/
      ↓
load-raw.py
      ↓
PostgreSQL
      ↓
raw schema

---

4. Staging Layer

The staging layer transforms the raw data using SQL.

Examples of transformations include:

- Timestamp conversion
- Text standardization
- NULL handling
- Duplicate removal
- Basic validation
- Negative value filtering

Example:

INITCAP(customer_city)

and:

UPPER(customer_state)

The staging layer provides cleaner and standardized data for analytics.

---

5. Analytics Layer

The transformed staging data is modeled into analytical tables.

Dimension Tables

dim_date
dim_customers
dim_products
dim_sellers

Fact Table

fact_order_items

The main fact table contains metrics such as:

- Price
- Freight value
- Total item value
- Order date
- Delivery days
- Order status

---

📊 Analytical Views

The project also creates analytical views for common business questions.

Monthly Revenue

vw_monthly_revenue

Provides:

- Year
- Month
- Monthly revenue
- Running total revenue

Top Products by Category

vw_top_products_by_category

Uses SQL window functions to rank products within their categories.

Top Customers

vw_top_customers

Provides:

- Customer
- Location
- Total spending
- Number of orders
- Spending rank

---

🧪 Data Quality

The pipeline includes automated data quality checks.

Current checks include:

Check| Purpose
Fact table has rows| Ensures analytics data exists
Customer dimension has rows| Ensures customer data exists
Product dimension has rows| Ensures product data exists
No NULL order IDs| Validates fact records
No NULL customer IDs| Validates customer relationships
Customer referential integrity| Ensures fact customers exist in the dimension
No negative prices| Validates business data

Current Test Result

[PASS] fact_order_items has rows (value=52)
[PASS] dim_customers has rows (value=50)
[PASS] dim_products has rows (value=51)
[PASS] fact_order_items.order_id has no nulls (value=0)
[PASS] fact_order_items.customer_id has no nulls (value=0)
[PASS] All fact customer_ids exist in dim_customers (value=0)
[PASS] No negative prices in fact_order_items (value=0)

All checks passed!

---

⚙️ GitHub Actions CI

The project uses GitHub Actions to automatically test the pipeline.

On every push or pull request to "main", the workflow:

1. Checkout repository
        ↓
2. Setup Python 3.11
        ↓
3. Install dependencies
        ↓
4. Start PostgreSQL 16
        ↓
5. Create RAW schema
        ↓
6. Load sample data
        ↓
7. Run STAGING transformations
        ↓
8. Verify staging data
        ↓
9. Verify staging relationships
        ↓
10. Run ANALYTICS transformations
        ↓
11. Verify analytical tables
        ↓
12. Run data quality checks
        ↓
13. Pipeline passes ✅

This allows the pipeline to be tested automatically instead of relying only on local execution.

---

🛠️ Technologies Used

Technology| Purpose
🐍 Python| Data ingestion and quality checks
🐘 PostgreSQL| Database and data warehouse
SQL| Data transformation and analytical modeling
Pandas| CSV/data processing
SQLAlchemy| Python → PostgreSQL connection
python-dotenv| Environment configuration
Git| Version control
GitHub| Source code repository
GitHub Actions| Continuous Integration

---

📁 Project Structure

e-commerce-pipeline/
│
├── .github/
│   └── workflows/
│       └── data-pipeline.yml
│
├── data/
│   ├── raw/
│   │   └── Olist source datasets
│   │
│   └── sample/
│       └── Sample relational datasets
│
├── scripts/
│   ├── load-raw.py
│   └── sample_data.py
│
├── sql/
│   ├── raw-schema.sql
│   ├── staging-schema.sql
│   └── analytical-schema.sql
│
├── tests/
│   └── data-quality.py
│
├── requirements.txt
├── .gitignore
└── README.md

---

💻 Local Setup

1. Clone the repository

git clone https://github.com/DSFAHAD/ecommerce-pipeline.git

cd ecommerce-pipeline

---

2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

---

3. Install dependencies

pip install -r requirements.txt

---

4. Configure PostgreSQL

Create a PostgreSQL database:

Database: ecommerce_pipeline
User: postgres

Then configure your environment variables:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_pipeline
DB_USER=postgres
DB_PASSWORD=your_password

---

5. Create the raw schema

Using "psql":

psql -h localhost -U postgres -d ecommerce_pipeline -f sql/raw-schema.sql

---

6. Generate sample data

python scripts/sample_data.py

---

7. Load raw data

python scripts/load-raw.py data/sample

---

8. Run staging transformations

psql -h localhost -U postgres -d ecommerce_pipeline -f sql/staging-schema.sql

---

9. Run analytics transformations

psql -h localhost -U postgres -d ecommerce_pipeline -f sql/analytical-schema.sql

---

10. Run data quality tests

python tests/data-quality.py

Expected result:

All checks passed!

---

🔍 Key Engineering Challenge

One important issue encountered during development was maintaining relationships while creating sample data.

Initially, taking the first rows independently from each CSV caused relationships such as:

order_items.order_id
        ↓
orders.order_id

to break.

This resulted in an empty analytical fact table.

The solution was to implement relational sampling:

Select Orders
     ↓
Select their Order Items
     ↓
Select related Customers
     ↓
Select related Products
     ↓
Select related Sellers

After the fix:

Orders          → 50
Order Items     → 52
Customers       → 50
Products        → 51
Sellers         → 48

The staging join then successfully produced:

52 matching rows

and the analytics fact table contained:

52 rows

This was a practical lesson in why data sampling must preserve primary-key / foreign-key relationships.

---

🎯 What This Project Demonstrates

This project demonstrates practical understanding of:

- ETL / ELT concepts
- Data ingestion
- Relational databases
- PostgreSQL
- SQL transformations
- Data cleaning
- Data modeling
- Fact and dimension tables
- Star-schema concepts
- SQL joins
- Window functions
- Referential integrity
- Data validation
- Python automation
- Git/GitHub
- CI with GitHub Actions

---

📈 Future Improvements

Possible future extensions include:

- Add Apache Airflow orchestration
- Add Docker containerization
- Add dbt transformations
- Add incremental data loading
- Add more comprehensive data quality tests
- Add data lineage
- Add a BI dashboard
- Add automated deployment
- Add monitoring and pipeline logging
- Process the complete Olist dataset

---

👨‍💻 Author

Fahad

Computer Science Student | Aspiring Data Engineer / Data Scientist

Focused on:

Python
SQL
PostgreSQL
Data Engineering
Data Science
Machine Learning

---

🔗 Repository

GitHub:
https://github.com/DSFAHAD/ecommerce-pipeline

---

⭐ If you find this project useful

Feel free to explore the repository and follow the development of the project.

#DataEngineering #Python #PostgreSQL #SQL #ETL #DataPipeline #GitHubActions #DataQuality #DataModeling #CI #LearningByDoing
