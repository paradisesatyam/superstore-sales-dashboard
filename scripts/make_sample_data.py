"""
Makes a Superstore-style sample CSV so the app runs without any download.
For the real thing, grab the Superstore dataset from Kaggle and put it in data/ as superstore.csv.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 5000

catalog = {
    "Furniture": {"Chairs": 250, "Tables": 400, "Bookcases": 300, "Furnishings": 60},
    "Office Supplies": {"Binders": 25, "Paper": 20, "Storage": 90, "Art": 15, "Labels": 12},
    "Technology": {"Phones": 300, "Accessories": 50, "Copiers": 900, "Machines": 500},
}
# rough profit margin per sub-category (Tables / Machines run thin or negative)
margin = {"Chairs": 0.10, "Tables": -0.08, "Bookcases": 0.02, "Furnishings": 0.15,
          "Binders": 0.22, "Paper": 0.40, "Storage": 0.10, "Art": 0.25, "Labels": 0.40,
          "Phones": 0.15, "Accessories": 0.25, "Copiers": 0.35, "Machines": 0.03}

regions = {"West": ["California", "Washington", "Oregon"],
           "East": ["New York", "Pennsylvania", "Ohio"],
           "Central": ["Texas", "Illinois", "Michigan"],
           "South": ["Florida", "Georgia", "Virginia"]}
segments = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
first = ["Aarav", "Maya", "John", "Sara", "Liam", "Emma", "Noah", "Olivia", "Ravi", "Priya", "Ethan", "Zoe"]
last = ["Smith", "Patel", "Brown", "Lee", "Garcia", "Khan", "Miller", "Davis", "Wilson", "Clark"]

customers = [(f"CU-{i:04d}", f"{rng.choice(first)} {rng.choice(last)}", rng.choice(segments)) for i in range(1, 701)]

rows = []
order_no = 0
while len(rows) < N:
    order_no += 1
    odate = pd.Timestamp("2022-01-01") + pd.Timedelta(days=int(rng.integers(0, 4 * 365)))
    cust = customers[int(rng.integers(0, len(customers)))]
    region = rng.choice(list(regions))
    state = rng.choice(regions[region])
    mode = rng.choice(ship_modes, p=[0.6, 0.2, 0.15, 0.05])
    ship_gap = {"Standard Class": 5, "Second Class": 3, "First Class": 2, "Same Day": 0}[mode]
    for _ in range(int(rng.integers(1, 5))):
        cat = rng.choice(list(catalog))
        sub = rng.choice(list(catalog[cat]))
        price = catalog[cat][sub] * rng.uniform(0.8, 1.3)
        qty = int(rng.integers(1, 8))
        disc = float(rng.choice([0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5]))
        sales = round(price * qty * (1 - disc), 2)
        # discounts eat into margin, deep ones push it negative
        profit = round(sales * (margin[sub] - disc * 0.55 + rng.normal(0, 0.05)), 2)
        rows.append({
            "Row ID": len(rows) + 1,
            "Order ID": f"US-{odate.year}-{order_no:05d}",
            "Order Date": odate.strftime("%m/%d/%Y"),
            "Ship Date": (odate + pd.Timedelta(days=ship_gap + int(rng.integers(0, 2)))).strftime("%m/%d/%Y"),
            "Ship Mode": mode,
            "Customer ID": cust[0], "Customer Name": cust[1], "Segment": cust[2],
            "Country": "United States", "State": state, "Region": region,
            "Category": cat, "Sub-Category": sub,
            "Sales": sales, "Quantity": qty, "Discount": disc, "Profit": profit,
        })

df = pd.DataFrame(rows[:N])
# sprinkle in a few duplicates so the cleaning step has something to do
df = pd.concat([df, df.sample(15, random_state=1)], ignore_index=True)
df.to_csv("data/sample_superstore.csv", index=False)
print("wrote", len(df), "rows")
