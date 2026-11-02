"""Sales Data Analysis using Python (pandas + matplotlib).

Pipeline: load -> clean -> feature engineering -> analysis -> charts -> summary report.
Run:  python sales_analysis.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA = Path("data/sales_data.csv")
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"figure.figsize": (9, 5), "axes.spines.top": False, "axes.spines.right": False})


# 1. LOAD -----------------------------------------------------------------
df = pd.read_csv(DATA, parse_dates=["order_date"])
print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")

# 2. CLEAN ----------------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

print("Missing values:\n", df.isna().sum()[df.isna().sum() > 0])
df["region"] = df["region"].fillna("Unknown")
# Fill missing prices with the median price of the same product
df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))

# 3. FEATURE ENGINEERING --------------------------------------------------
df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
df["month"] = df["order_date"].dt.to_period("M")
df["year"] = df["order_date"].dt.year
df["weekday"] = df["order_date"].dt.day_name()

# 4. ANALYSIS -------------------------------------------------------------
total_revenue = df["revenue"].sum()
kpis = {
    "Total revenue": f"£{total_revenue:,.0f}",
    "Total orders": f"{df['order_id'].nunique():,}",
    "Unique customers": f"{df['customer_id'].nunique():,}",
    "Average order value": f"£{df['revenue'].mean():,.2f}",
    "Units sold": f"{df['quantity'].sum():,}",
}

monthly = df.groupby("month")["revenue"].sum()
by_category = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
top_products = df.groupby("product")["revenue"].sum().nlargest(5)
by_weekday = (df.groupby("weekday")["revenue"].sum()
              .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))
yearly = df.groupby("year")["revenue"].sum()
growth = (yearly.iloc[-1] / yearly.iloc[0] - 1) * 100 if len(yearly) > 1 else float("nan")

# Customer value (simple RFM-style view)
snapshot = df["order_date"].max() + pd.Timedelta(days=1)
customers = df.groupby("customer_id").agg(
    recency=("order_date", lambda s: (snapshot - s.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("revenue", "sum"),
)
top_customers = customers.nlargest(10, "monetary")

# Discount effect
discount_effect = df.groupby("discount").agg(orders=("order_id", "count"), avg_qty=("quantity", "mean"),
                                             revenue=("revenue", "sum")).round(2)

# 5. CHARTS ---------------------------------------------------------------
ax = monthly.plot(marker="o", color="#2563eb")
ax.set_title("Monthly Revenue Trend"); ax.set_xlabel("Month"); ax.set_ylabel("Revenue (£)")
plt.tight_layout(); plt.savefig(OUT / "monthly_revenue.png", dpi=150); plt.close()

ax = by_category.plot(kind="bar", color="#16a34a")
ax.set_title("Revenue by Category"); ax.set_ylabel("Revenue (£)"); plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(OUT / "revenue_by_category.png", dpi=150); plt.close()

ax = by_region.plot(kind="pie", autopct="%1.1f%%", ylabel="", startangle=90)
ax.set_title("Revenue Share by Region")
plt.tight_layout(); plt.savefig(OUT / "revenue_by_region.png", dpi=150); plt.close()

ax = top_products.sort_values().plot(kind="barh", color="#f59e0b")
ax.set_title("Top 5 Products by Revenue"); ax.set_xlabel("Revenue (£)")
plt.tight_layout(); plt.savefig(OUT / "top_products.png", dpi=150); plt.close()

ax = by_weekday.plot(kind="bar", color="#9333ea")
ax.set_title("Revenue by Day of Week"); ax.set_ylabel("Revenue (£)"); plt.xticks(rotation=45)
plt.tight_layout(); plt.savefig(OUT / "revenue_by_weekday.png", dpi=150); plt.close()

# 6. REPORT ---------------------------------------------------------------
best_month = monthly.idxmax()
lines = ["SALES ANALYSIS SUMMARY", "=" * 40]
lines += [f"{k}: {v}" for k, v in kpis.items()]
lines += [
    "",
    f"Best month: {best_month} (£{monthly.max():,.0f})",
    f"Top category: {by_category.index[0]} ({by_category.iloc[0] / total_revenue:.1%} of revenue)",
    f"Top region: {by_region.index[0]} ({by_region.iloc[0] / total_revenue:.1%} of revenue)",
    f"Year-on-year revenue change: {growth:+.1f}%",
    "",
    "Top 5 products:", top_products.round(0).to_string(),
    "",
    "Top 10 customers by spend:", top_customers.round(0).to_string(),
    "",
    "Discount effect:", discount_effect.to_string(),
]
report = "\n".join(lines)
(OUT / "summary_report.txt").write_text(report)
df.to_csv(OUT / "cleaned_sales_data.csv", index=False)
print("\n" + report)
print(f"\nCharts and report saved in '{OUT}/'")
