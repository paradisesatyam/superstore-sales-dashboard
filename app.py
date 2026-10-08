import matplotlib.pyplot as plt
import streamlit as st

from src import charts
from src.data_loader import load_data

st.set_page_config(page_title="Superstore Sales Dashboard", page_icon="📊", layout="wide")


@st.cache_data
def get_data():
    return load_data()


df, source = get_data()

st.title("Superstore Sales Analytics Dashboard")
st.caption(f"Data source: {source} | {len(df):,} order lines")

# ---- sidebar filters ----
st.sidebar.header("Filters")
years = sorted(df["year"].unique())
sel_years = st.sidebar.multiselect("Year", years, default=years)
sel_regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
sel_cats = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))

view = df[df["year"].isin(sel_years) & df["region"].isin(sel_regions) & df["category"].isin(sel_cats)]

if view.empty:
    st.warning("No data for these filters. Try selecting more options.")
    st.stop()

# ---- KPIs ----
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total sales", f"${view['sales'].sum():,.0f}")
k2.metric("Total profit", f"${view['profit'].sum():,.0f}")
k3.metric("Profit margin", f"{view['profit'].sum() / view['sales'].sum():.1%}")
k4.metric("Customers", f"{view['customer_id'].nunique():,}")

st.divider()


def show(fig):
    st.pyplot(fig)
    plt.close(fig)


show(charts.monthly_sales(view))

c1, c2 = st.columns([3, 2])
with c1:
    show(charts.profit_by_subcategory(view))
with c2:
    show(charts.discount_vs_margin(view))

c3, c4 = st.columns(2)
with c3:
    show(charts.sales_by_region(view))
with c4:
    show(charts.segment_split(view))

# ---- top customers ----
st.subheader("Top 10 customers by sales")
top = (view.groupby(["customer_id", "customer_name"])[["sales", "profit"]].sum()
       .sort_values("sales", ascending=False).head(10).round(2).reset_index())
st.dataframe(top, use_container_width=True, hide_index=True)

with st.expander("Look at the raw data"):
    st.dataframe(view.head(200), use_container_width=True)
