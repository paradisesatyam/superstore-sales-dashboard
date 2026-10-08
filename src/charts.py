import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

BLUE, RED, GREY = "#1f77b4", "#d62728", "#9aa5b1"


def _style(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)


def monthly_sales(df):
    m = df.groupby("month")[["sales", "profit"]].sum()
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(m.index, m["sales"], color=BLUE, label="Sales")
    ax.plot(m.index, m["profit"], color="green", label="Profit")
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
    ax.legend(frameon=False)
    _style(ax, "Monthly sales and profit")
    fig.tight_layout()
    return fig


def profit_by_subcategory(df):
    p = df.groupby("sub_category")["profit"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(p.index, p.values, color=[RED if v < 0 else BLUE for v in p.values])
    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
    _style(ax, "Profit by sub-category")
    fig.tight_layout()
    return fig


def sales_by_region(df):
    r = df.groupby("region")["sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 3.8))
    ax.bar(r.index, r.values, color=BLUE)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
    _style(ax, "Sales by region")
    fig.tight_layout()
    return fig


def discount_vs_margin(df):
    d = df.groupby("discount_band", observed=True)["profit_margin"].mean() * 100
    fig, ax = plt.subplots(figsize=(5, 3.8))
    ax.bar(d.index.astype(str), d.values, color=[RED if v < 0 else GREY for v in d.values])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    _style(ax, "Average profit margin by discount")
    fig.tight_layout()
    return fig


def segment_split(df):
    s = df.groupby("segment")["sales"].sum()
    fig, ax = plt.subplots(figsize=(4.5, 3.8))
    ax.pie(s.values, labels=s.index, autopct="%1.0f%%", startangle=90,
           colors=[BLUE, "#ff7f0e", GREY], wedgeprops={"edgecolor": "white"})
    ax.set_title("Sales by customer segment", fontsize=12, fontweight="bold", loc="left")
    fig.tight_layout()
    return fig
