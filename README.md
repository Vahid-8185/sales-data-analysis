# Sales Data Analysis Using Python

An end-to-end exploratory data analysis (EDA) project using **Python, Pandas and Matplotlib** to explore retail sales data, identify business trends and generate useful insights.

This project demonstrates data cleaning, feature engineering, KPI reporting, customer analysis and data visualisation using a synthetic retail dataset.

## Business Questions

- What are the total revenue, orders, customers and average order value?
- Which months, categories, regions and products generate the most revenue?
- Are there seasonal sales trends?
- Who are the highest-value customers?
- How do discounts affect customer purchasing behaviour?

## Project Structure

```text
sales-data-analysis/
├── data/
│   └── sales_data.csv
├── outputs/
│   ├── cleaned_sales_data.csv
│   ├── monthly_revenue.png
│   ├── revenue_by_category.png
│   ├── revenue_by_region.png
│   ├── revenue_by_weekday.png
│   ├── summary_report.txt
│   └── top_products.png
├── generate_data.py
├── sales_analysis.py
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- Pandas
- Matplotlib
- NumPy

## How to Run

```bash
pip install -r requirements.txt
python generate_data.py
python sales_analysis.py
```

If you already have `data/sales_data.csv`, you can skip `generate_data.py`.

## Data Cleaning and Methodology

1. Removed duplicate records.
2. Handled missing region and unit price values.
3. Created revenue, month, year and weekday features.
4. Analysed revenue by category, region, product and month.
5. Performed RFM-style customer analysis.
6. Evaluated discount patterns.
7. Generated charts and a summary report.

## Key Findings

Results from the synthetic sample dataset:

| Metric | Result |
|---|---:|
| Total Revenue | £2,775,366 |
| Total Orders | 5,529 |
| Unique Customers | 895 |
| Average Order Value | £501.97 |
| Units Sold | 16,513 |
| Best Month | December 2024 |
| Top Category | Electronics |
| Top Region | North |

### Business Insights

- Electronics contributed approximately 68.8% of total revenue.
- Laptop and Smartphone were the highest-revenue products.
- December recorded the highest monthly revenue.
- The North region contributed approximately 28.8% of revenue.
- Average order quantities were similar across discount levels in this sample.

## Skills Demonstrated

Python, Pandas, NumPy, Matplotlib, Data Cleaning, Exploratory Data Analysis, Feature Engineering, KPI Reporting, Data Visualisation and RFM Analysis.

## Dataset Disclaimer

This project uses synthetic sample data for educational and portfolio purposes. The results do not represent a real company's sales or business performance.
