import os
from pathlib import Path

import pandas as pd

from src.cleaning import clean

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _from_mysql() -> pd.DataFrame:
    from sqlalchemy import create_engine
    url = (f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}"
           f"@{os.environ.get('MYSQL_HOST', 'localhost')}/{os.environ['MYSQL_DB']}")
    engine = create_engine(url)
    return pd.read_sql("SELECT * FROM orders", engine)


def _from_csv() -> pd.DataFrame:
    # use the real Kaggle file if it's there, otherwise fall back to the sample
    for name in ("superstore.csv", "sample_superstore.csv"):
        path = DATA_DIR / name
        if path.exists():
            return pd.read_csv(path, encoding="latin-1")
    raise FileNotFoundError("No CSV found in data/")


def load_data() -> tuple[pd.DataFrame, str]:
    """Returns (clean dataframe, source label). Uses MySQL when MYSQL_* env vars are set."""
    if os.environ.get("MYSQL_USER") and os.environ.get("MYSQL_DB"):
        try:
            return clean(_from_mysql()), "MySQL"
        except Exception as e:
            print("MySQL failed, using CSV instead:", e)
    return clean(_from_csv()), "CSV"
