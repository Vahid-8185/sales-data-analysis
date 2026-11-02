"""Generate a realistic synthetic retail sales dataset (data/sales_data.csv).

Skip this step if you have your own dataset (e.g. from Kaggle) -- just make sure
it has the columns: order_id, order_date, customer_id, region, category,
product, quantity, unit_price, discount.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 5000

catalog = {
    "Electronics": {"Laptop": 750, "Smartphone": 520, "Headphones": 90, "Smartwatch": 180},
    "Furniture": {"Office Chair": 140, "Desk": 260, "Bookshelf": 110},
    "Clothing": {"Jacket": 75, "Jeans": 45, "Sneakers": 65},
    "Groceries": {"Coffee Pack": 12, "Snack Box": 18, "Tea Set": 25},
}
regions = ["North", "South", "East", "West"]

dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 730, N), unit="D")
# Seasonal lift in Nov/Dec: duplicate some late-year orders
rows = []
for i, d in enumerate(dates):
    cat = rng.choice(list(catalog), p=[0.3, 0.2, 0.3, 0.2])
    prod = rng.choice(list(catalog[cat]))
    base = catalog[cat][prod]
    rows.append({
        "order_id": 10000 + i,
        "order_date": d,
        "customer_id": f"C{rng.integers(1, 900):04d}",
        "region": rng.choice(regions, p=[0.3, 0.25, 0.2, 0.25]),
        "category": cat,
        "product": prod,
        "quantity": int(rng.integers(1, 6)),
        "unit_price": round(base * rng.uniform(0.95, 1.05), 2),
        "discount": float(rng.choice([0, 0.05, 0.1, 0.2], p=[0.6, 0.2, 0.15, 0.05])),
    })

df = pd.DataFrame(rows)
extra = df[df["order_date"].dt.month.isin([11, 12])].sample(frac=0.6, random_state=1)
df = pd.concat([df, extra], ignore_index=True)
df["order_id"] = range(10000, 10000 + len(df))

# Introduce a few data-quality problems to practise cleaning
df.loc[df.sample(40, random_state=2).index, "region"] = None
df.loc[df.sample(25, random_state=3).index, "unit_price"] = np.nan
df = pd.concat([df, df.sample(30, random_state=4)], ignore_index=True)  # duplicates

df.to_csv("data/sales_data.csv", index=False)
print(f"Saved {len(df)} rows to data/sales_data.csv")
