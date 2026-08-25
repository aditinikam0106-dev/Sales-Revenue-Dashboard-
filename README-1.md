# Sales & Revenue Analysis Dashboard

## Project Overview
This project builds an interactive dashboard to analyze sales, revenue, and profit data. It supports Excel and CSV input and provides KPI cards, product charts, filters, and a revenue trend.

## Key Features
- Import data from Excel or CSV
- Track Total Sales, Total Revenue, and Total Profit
- Revenue by Product visualization
- Profit by Product visualization
- Revenue trend over time
- Product, Category, and Region filters
- Identify the top-performing product by revenue
- Display filtered source data

## Expected Outcome
The project demonstrates:
- Data visualization
- KPI tracking
- Interactive filtering
- Business insight generation
- Basic sales and revenue analysis

## Required Data Columns
The uploaded file should contain:
- Date (recommended for the revenue trend)
- Product
- Category (optional for the filter)
- Region (optional for the filter)
- Quantity (optional)
- Sales
- Revenue
- Profit

## How to Run

1. Install Python.
2. Open a terminal in this project folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the dashboard:

```bash
streamlit run app.py
```

5. Upload the Excel or CSV sales dataset in the browser.

## Project Structure

```text
sales_revenue_dashboard/
├── app.py
├── requirements.txt
└── README.md
```
