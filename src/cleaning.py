import numpy as np
import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # snake_case column names: "Sub-Category" -> "sub_category"
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace("-", "_").str.replace(" ", "_"))

    df = df.drop_duplicates(subset=["order_id", "customer_id", "sub_category", "sales", "quantity"])

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
    df = df.dropna(subset=["order_date", "sales"])

    for col in ["segment", "region", "category", "sub_category", "ship_mode"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    # extra columns used in the charts
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["ship_days"] = (df["ship_date"] - df["order_date"]).dt.days
    df["profit_margin"] = np.where(df["sales"] != 0, df["profit"] / df["sales"], 0.0)
    df["discount_band"] = pd.cut(df["discount"], bins=[-0.01, 0, 0.2, 0.4, 1.0],
                                 labels=["No discount", "1-20%", "21-40%", "40%+"])
    return df.reset_index(drop=True)
