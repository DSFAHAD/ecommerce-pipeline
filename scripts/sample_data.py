import pandas as pd
import os

RAW_DIR = "data/raw"
SAMPLE_DIR = "data/sample"
os.makedirs(SAMPLE_DIR, exist_ok=True)

for file_name in os.listdir(RAW_DIR):
    if file_name.endswith(".csv"):
        df = pd.read_csv(os.path.join(RAW_DIR, file_name))
        sample = df.head(50)
        sample.to_csv(os.path.join(SAMPLE_DIR, file_name), index=False)
        print(f"Sampled {file_name}: {len(sample)} rows")

print("Sample data created in data/sample/")