import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sales & Revenue Analysis Dashboard", layout="wide")

st.title("Sales & Revenue Analysis Dashboard")
st.caption("Interactive dashboard for KPI tracking, product analysis, and business insights.")

uploaded_file = st.file_uploader(
    "Upload sales data (Excel or CSV)",
    type=["xlsx", "csv"]
)

if uploaded_file is None:
    st.info("Upload an Excel or CSV file to view the dashboard.")
    st.stop()

try:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

df.columns = [str(c).strip() for c in df.columns]

required_columns = ["Product", "Sales", "Revenue", "Profit"]
missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.write("Required columns:", required_columns)
    st.stop()

for col in ["Sales", "Revenue", "Profit"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Sidebar filters
st.sidebar.header("Filters")

if "Product" in df.columns:
    products = sorted(df["Product"].dropna().astype(str).unique())
    selected_products = st.sidebar.multiselect(
        "Product", products, default=products
    )
    df_filtered = df[df["Product"].astype(str).isin(selected_products)]
else:
    df_filtered = df.copy()

if "Category" in df_filtered.columns:
    categories = sorted(df_filtered["Category"].dropna().astype(str).unique())
    selected_categories = st.sidebar.multiselect(
        "Category", categories, default=categories
    )
    df_filtered = df_filtered[
        df_filtered["Category"].astype(str).isin(selected_categories)
    ]

if "Region" in df_filtered.columns:
    regions = sorted(df_filtered["Region"].dropna().astype(str).unique())
    selected_regions = st.sidebar.multiselect(
        "Region", regions, default=regions
    )
    df_filtered = df_filtered[
        df_filtered["Region"].astype(str).isin(selected_regions)
    ]

# KPIs
total_sales = df_filtered["Sales"].sum()
total_revenue = df_filtered["Revenue"].sum()
total_profit = df_filtered["Profit"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", f"{total_sales:,.0f}")
c2.metric("Total Revenue", f"{total_revenue:,.0f}")
c3.metric("Total Profit", f"{total_profit:,.0f}")

# Product analysis
product_summary = (
    df_filtered.groupby("Product", as_index=False)[["Sales", "Revenue", "Profit"]]
    .sum()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")
    fig_revenue = px.bar(
        product_summary,
        x="Product",
        y="Revenue",
        title="Revenue by Product",
        text_auto=True
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    st.subheader("Profit by Product")
    fig_profit = px.bar(
        product_summary,
        x="Product",
        y="Profit",
        title="Profit by Product",
        text_auto=True
    )
    st.plotly_chart(fig_profit, use_container_width=True)

# Revenue trend
if "Date" in df_filtered.columns:
    df_filtered["Date"] = pd.to_datetime(df_filtered["Date"], errors="coerce")
    trend = (
        df_filtered.dropna(subset=["Date"])
        .groupby("Date", as_index=False)["Revenue"]
        .sum()
        .sort_values("Date")
    )

    st.subheader("Revenue Trend")
    if not trend.empty:
        fig_trend = px.line(
            trend,
            x="Date",
            y="Revenue",
            markers=True,
            title="Revenue Trend Over Time"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("No valid dates were found for the revenue trend.")

# Top product
if not product_summary.empty:
    top_product = product_summary.loc[
        product_summary["Revenue"].idxmax(), "Product"
    ]
    st.success(f"Top-performing product by revenue: {top_product}")

st.subheader("Filtered Data")
st.dataframe(df_filtered, use_container_width=True)
