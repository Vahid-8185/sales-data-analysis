# Sales Data Analysis using Python

End-to-end exploratory analysis of retail sales data using **pandas** and **matplotlib**: data cleaning, feature engineering, KPI calculation, customer analysis and visualisation.

## Business questions answered
- How much revenue, how many orders and customers, and what is the average order value?
- Which months, categories, regions and products drive revenue?
- Is there seasonality (e.g. Nov/Dec peak)?
- Who are the highest-value customers (recency / frequency / monetary view)?
- Do discounts increase the quantity customers buy?

## Project structure
```
sales-data-analysis/
├── generate_data.py     # creates a synthetic dataset (skip if using your own CSV)
├── sales_analysis.py    # cleaning, analysis, charts, report
├── requirements.txt
├── data/sales_data.csv
└── outputs/             # charts, summary_report.txt, cleaned_sales_data.csv
```

## How to run
```bash
pip install -r requirements.txt
python generate_data.py      # optional
python sales_analysis.py
```
To use your own data (e.g. a Kaggle dataset), save it as `data/sales_data.csv` with columns:
`order_id, order_date, customer_id, region, category, product, quantity, unit_price, discount`.

## Methodology
1. **Cleaning:** removed duplicate orders; filled missing regions with "Unknown"; imputed missing prices using the product's median price.
2. **Feature engineering:** `revenue = quantity x unit_price x (1 - discount)`, plus month, year and weekday.
3. **Analysis:** groupby aggregations for time, category, region and product; RFM-style customer table; discount impact.
4. **Visualisation:** monthly trend, category bars, region pie, top products, weekday pattern.

## Sample findings (synthetic data)
- Total revenue about £2.78M across 5,529 orders and 895 customers.
- Electronics generates roughly 69% of revenue; Laptop and Smartphone are the top products.
- December is the best month, showing clear year-end seasonality.
- Discounts barely change the average quantity per order, so deep discounts may reduce margin without lifting volume.

## Skills demonstrated
Python, pandas, matplotlib, data cleaning, EDA, KPI reporting, customer segmentation basics.
