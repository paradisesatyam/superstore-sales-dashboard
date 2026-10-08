"""
Loads the CSV into a MySQL table called `orders`.

Run once after creating the database (see sql/schema.sql):
    set MYSQL_USER=root MYSQL_PASSWORD=... MYSQL_DB=superstore
    python scripts/load_to_mysql.py
"""
import os
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.cleaning import clean

data_dir = Path(__file__).resolve().parent.parent / "data"
csv = data_dir / "superstore.csv"
if not csv.exists():
    csv = data_dir / "sample_superstore.csv"

df = clean(pd.read_csv(csv, encoding="latin-1"))
df = df.drop(columns=["month", "discount_band"])  # derived in pandas, no need to store

url = (f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}"
       f"@{os.environ.get('MYSQL_HOST', 'localhost')}/{os.environ['MYSQL_DB']}")
engine = create_engine(url)
df.to_sql("orders", engine, if_exists="replace", index=False, chunksize=1000)
print(f"loaded {len(df)} rows from {csv.name} into MySQL")
