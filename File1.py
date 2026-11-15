#Data Ingestion
#Step 1: Import Pandas and load the CSV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv("D:/MCA AI&ML SEM1/FRESHFLOW/DATASETS/freshflow_sales.csv")

print("Dataset shape:", data.shape)
print("First 5 rows:")
print(data.head())

print("Total rows:", data.shape[0])
print("Total columns:", data.shape[1])


#Step 2: Extract individual columns
transaction_id = data["transaction_id"]
day = data["day_index"]
outlet = data["outlet_id"]
product = data["product_code"]
category = data["category_code"]
quantity = data["quantity"]
unit_price = data["unit_price"]
unit_cost = data["unit_cost"]
discount_rate = data["discount_rate"]
stock_before = data["stock_before_units"]
payment = data["payment_code"]
rating = data["customer_rating"]

print("Transaction IDs:", transaction_id.head())
print("Quantity:",quantity.head())
print("Unit Price:", unit_price.head())

#Data Audit & Validation
#Step 1:Inspect the dataset
print("Shape:")
print(data.shape)

print("\nColumn names:")
print(data.columns)

print("\nData types:")
print(data.dtypes)

print("\nMissing values:")
print(data.isnull().sum())

print("\nInfinite values:")
print(np.isinf(data.select_dtypes(include="number")).sum())

print("\nDuplicate transaction IDs:")
print(data["transaction_id"].duplicated().sum())

#Step 2:Create validation conditions

valid_day = data["day_index"].between(1, 31)
valid_outlet = data["outlet_id"].isin([1, 2, 3])
valid_product = data["product_code"].isin(
    ["P101", "P102", "P103", "P104", "P105"]
)
valid_category = data["category_code"].isin(["C1", "C2", "C3"])
valid_quantity = (
    (data["quantity"] > 0) &
    (data["quantity"] % 1 == 0)
)
valid_price = data["unit_price"] > 0
valid_cost = data["unit_cost"] >= 0
valid_discount = data["discount_rate"].between(0, 1)
valid_stock = data["stock_before_units"] >= 0
valid_payment = data["payment_code"].isin(["CASH", "CARD", "UPI"])
valid_rating = (
    data["customer_rating"].isna() |
    data["customer_rating"].between(1, 5)
)
# CHECK PRODUCT-CATEGORY MAPPING
product_category = {
    "P101": "C1",
    "P102": "C1",
    "P103": "C2",
    "P104": "C2",
    "P105": "C3"
}
expected_category = data["product_code"].map(product_category)
valid_mapping = data["category_code"] == expected_category

#Step 3:Count invalid records
print("Invalid days:", (~valid_day).sum())
print("Invalid outlets:", (~valid_outlet).sum())
print("Invalid products:", (~valid_product).sum())
print("Invalid categories:", (~valid_category).sum())
print("Invalid quantities:", (~valid_quantity).sum())
print("Invalid prices:", (~valid_price).sum())
print("Invalid costs:", (~valid_cost).sum())
print("Invalid discounts:", (~valid_discount).sum())
print("Invalid stock:", (~valid_stock).sum())
print("Invalid payments:", (~valid_payment).sum())
print("Invalid ratings:", (~valid_rating).sum())


#Data Cleaning & Preparation
#Step 1: Create a clean analytical dataset
# Preserve original data
raw_data = data.copy()
# Create quality flags
quality_flags = pd.DataFrame(index=data.index)

quality_flags["invalid_day"] = ~valid_day
quality_flags["invalid_outlet"] = ~valid_outlet
quality_flags["invalid_product"] = ~valid_product
quality_flags["invalid_category"] = ~valid_category
quality_flags["invalid_quantity"] = ~valid_quantity
quality_flags["invalid_price"] = ~valid_price
quality_flags["invalid_discount"] = ~valid_discount
quality_flags["invalid_cost"] = ~valid_cost
quality_flags["invalid_stock"] = ~valid_stock
quality_flags["invalid_payment"] = ~valid_payment
quality_flags["invalid_rating"] = ~valid_rating
# Create valid record condition
valid_records = (
    valid_day &
    valid_outlet &
    valid_product &
    valid_category &
    valid_quantity &
    valid_price &
    valid_discount &
    valid_stock &
    valid_payment
)
# Clean dataset
clean_data = data[valid_records].copy()
# Excluded records
excluded_records = data[~valid_records].copy()
print("Original rows:", len(raw_data))
print("Clean rows:", len(clean_data))
print("Excluded rows:", len(excluded_records))

#Step 2: Handle missing values
print(clean_data.isnull().sum())
clean_data["customer_rating"] = clean_data["customer_rating"].fillna(clean_data["customer_rating"].median())
missing_cost = clean_data["unit_cost"].isnull()
print("Missing costs:", missing_cost.sum())

clean_data.to_csv(
    "output/clean_data.csv",
    index=False
)
excluded_records.to_csv(
    "output/excluded_records.csv",
    index=False
)
quality_flags.to_csv(
    "output/quality_flags.csv",
    index=False
)

# Fill missing customer ratings
clean_data["customer_rating"] = clean_data["customer_rating"].fillna(
    clean_data["customer_rating"].median()
)

# Fill missing unit costs
clean_data["unit_cost"] = clean_data["unit_cost"].fillna(
    clean_data["unit_cost"].median()
)



#Calculate sales metrics
# Gross sales
clean_data["gross_sales"] = clean_data["quantity"] * clean_data["unit_price"]

# Discount amount
clean_data["discount_amount"] = clean_data["gross_sales"] * clean_data["discount_rate"]

# Net revenue
clean_data["net_revenue"] = clean_data["gross_sales"] - clean_data["discount_amount"]

# Cost of goods sold
clean_data["cost_of_goods_sold"] = clean_data["quantity"] * clean_data["unit_cost"]

# Gross profit
clean_data["gross_profit"] = clean_data["net_revenue"] - clean_data["cost_of_goods_sold"]

# Gross margin percentage
clean_data["gross_margin"] = (
    clean_data["gross_profit"] / clean_data["net_revenue"]
) * 100

# Average selling price
clean_data["average_selling_price"] = (
    clean_data["net_revenue"] / clean_data["quantity"]
)

print(clean_data.head())

#Calculate total business performance

total_gross_sales = clean_data["gross_sales"].sum()

total_discount = clean_data["discount_amount"].sum()

total_revenue = clean_data["net_revenue"].sum()

total_cost = clean_data["cost_of_goods_sold"].sum()

total_profit = clean_data["gross_profit"].sum()

overall_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

print("Total Gross Sales:", total_gross_sales)
print("Total Discount:", total_discount)
print("Total Net Revenue:", total_revenue)
print("Total Cost:", total_cost)
print("Total Gross Profit:", total_profit)
print("Overall Gross Margin:", overall_margin)

#Statistical Analysis
print("Mean Revenue:")
print(clean_data["net_revenue"].mean())

print("Median Revenue:")
print(clean_data["net_revenue"].median())

print("Minimum Revenue:")
print(clean_data["net_revenue"].min())

print("Maximum Revenue:")
print(clean_data["net_revenue"].max())

print("Standard Deviation:")
print(clean_data["net_revenue"].std())

print("Variance:")
print(clean_data["net_revenue"].var())

print("25th Percentile:")
print(clean_data["net_revenue"].quantile(0.25))

print("50th Percentile:")
print(clean_data["net_revenue"].quantile(0.50))

print("75th Percentile:")
print(clean_data["net_revenue"].quantile(0.75))

statistics = clean_data[
    ["net_revenue", "gross_profit", "quantity"]
].describe()

print(statistics)

#outlet comparison
outlet_summary = clean_data.groupby("outlet_id").agg(
    transactions=("transaction_id", "count"),
    units_sold=("quantity", "sum"),
    gross_sales=("gross_sales", "sum"),
    discount=("discount_amount", "sum"),
    net_revenue=("net_revenue", "sum"),
    cost=("cost_of_goods_sold", "sum"),
    gross_profit=("gross_profit", "sum")
)

outlet_summary["gross_margin"] = (
    outlet_summary["gross_profit"] /
    outlet_summary["net_revenue"] * 100
)

print(outlet_summary)

#product comparison
product_summary = clean_data.groupby("product_code").agg(
    transactions=("transaction_id", "count"),
    units_sold=("quantity", "sum"),
    gross_sales=("gross_sales", "sum"),
    discount=("discount_amount", "sum"),
    net_revenue=("net_revenue", "sum"),
    cost=("cost_of_goods_sold", "sum"),
    gross_profit=("gross_profit", "sum")
)

product_summary["gross_margin"] = (
    product_summary["gross_profit"] /
    product_summary["net_revenue"] * 100
)

print(product_summary)

#Rank outlets and products
print("Outlet ranking by revenue:")
print(outlet_summary.sort_values(
    "net_revenue",
    ascending=False
))

print("Product ranking by revenue:")
print(product_summary.sort_values(
    "net_revenue",
    ascending=False
))


#Trend & Anomaly Analysis
#Calculate daily revenue for 30 days

daily_revenue = clean_data.groupby(
    "day_index"
)["net_revenue"].sum()

daily_revenue = daily_revenue.reindex(
    range(1, 31),
    fill_value=0
)

print("Daily Revenue:")
print(daily_revenue)

daily_change = daily_revenue.diff()

print("Daily Revenue Change:")
print(daily_change)

daily_percentage_change = (
    daily_revenue.pct_change() * 100
)

print("Daily Percentage Change:")
print(daily_percentage_change)

moving_average = daily_revenue.rolling(
    window=3
).mean()

print("3-Day Moving Average:")
print(moving_average)

daily_table = pd.DataFrame({
    "day": daily_revenue.index,
    "daily_revenue": daily_revenue.values
})

daily_table["daily_change"] = (
    daily_table["daily_revenue"].diff()
)

daily_table["daily_percentage_change"] = (
    daily_table["daily_revenue"].pct_change() * 100
)

daily_table["moving_average_3day"] = (
    daily_table["daily_revenue"].rolling(3).mean()
)

print(daily_table)

plt.figure(figsize=(12, 5))

plt.plot(
    daily_table["day"],
    daily_table["daily_revenue"],
    marker="o",
    label="Daily Revenue"
)

plt.plot(
    daily_table["day"],
    daily_table["moving_average_3day"],
    label="3-Day Moving Average"
)

plt.xlabel("Day")
plt.ylabel("Revenue")

plt.title("FreshFlow Daily Revenue Trend")

plt.legend()

plt.show()

#Detect anomalies
#IQR method
q1 = clean_data["net_revenue"].quantile(0.25)

q3 = clean_data["net_revenue"].quantile(0.75)

iqr = q3 - q1

lower_limit = q1 - 1.5 * iqr

upper_limit = q3 + 1.5 * iqr

clean_data["iqr_anomaly"] = (
    (clean_data["net_revenue"] < lower_limit) |
    (clean_data["net_revenue"] > upper_limit)
)

print("IQR anomalies:")
print(clean_data["iqr_anomaly"].sum())

#Z score method
mean_revenue = clean_data["net_revenue"].mean()

std_revenue = clean_data["net_revenue"].std(ddof=0)

clean_data["z_score"] = (
    clean_data["net_revenue"] - mean_revenue
) / std_revenue

clean_data["z_anomaly"] = (
    clean_data["z_score"].abs() > 3
)

print("Z-score anomalies:")
print(clean_data["z_anomaly"].sum())

#Anomaly Register
clean_data["high_discount"] = (
    clean_data["discount_rate"] > 0.30
)

clean_data["zero_stock"] = (
    clean_data["stock_before_units"] == 0
)

clean_data["high_price"] = (
    clean_data["unit_price"] >
    clean_data["unit_price"].quantile(0.99)
)

anomaly_register = clean_data[
    clean_data["iqr_anomaly"] |
    clean_data["z_anomaly"] |
    clean_data["high_discount"] |
    clean_data["zero_stock"] |
    clean_data["high_price"]
].copy()

print(anomaly_register[[
    "transaction_id",
    "net_revenue",
    "discount_rate",
    "iqr_anomaly",
    "z_anomaly",
    "high_discount",
    "zero_stock",
    "high_price"
]])

anomaly_register.to_csv(
    "output/anomaly_register.csv",
    index=False
)

#Scenario Analysis
#Scenario 1 — 5% discount
scenario_5 = (
    clean_data["gross_sales"] * (1 - 0.05)
)

profit_5 = (
    scenario_5 -
    clean_data["cost_of_goods_sold"]
)

scenario_10 = (
    clean_data["gross_sales"] * (1 - 0.10)
)

#Scenario 2 — 10% discount
profit_10 = (
    scenario_10 -
    clean_data["cost_of_goods_sold"]
)

#Scenario 3 — 15% discount
scenario_15 = (
    clean_data["gross_sales"] * (1 - 0.15)
)

profit_15 = (
    scenario_15 -
    clean_data["cost_of_goods_sold"]
)

#Scenario Comparison
print("5% Revenue:", scenario_5.sum())

print("10% Revenue:", scenario_10.sum())

print("15% Revenue:", scenario_15.sum())

print("5% Gross Profit:", profit_5.sum())

print("10% Gross Profit:", profit_10.sum())

print("15% Gross Profit:", profit_15.sum())

#Scanerio Table
scenario_summary = pd.DataFrame({
    "discount_rate": [0.05, 0.10, 0.15],
    "net_revenue": [
        scenario_5.sum(),
        scenario_10.sum(),
        scenario_15.sum()
    ],
    "gross_profit": [
        profit_5.sum(),
        profit_10.sum(),
        profit_15.sum()
    ]
})

scenario_summary["gross_margin"] = (
    scenario_summary["gross_profit"] /
    scenario_summary["net_revenue"] * 100
)

print(scenario_summary)

#Insight Generation
# Outlet with highest revenue
top_outlet_revenue = outlet_summary["net_revenue"].idxmax()

# Outlet with highest gross profit
top_outlet_profit = outlet_summary["gross_profit"].idxmax()

# Outlet with highest gross margin
top_outlet_margin = outlet_summary["gross_margin"].idxmax()

# Product with highest units sold
top_product_units = product_summary["units_sold"].idxmax()

# Product with highest revenue
top_product_revenue = product_summary["net_revenue"].idxmax()

# Product with highest gross profit
top_product_profit = product_summary["gross_profit"].idxmax()

# Highest and lowest revenue days
highest_day = daily_revenue.idxmax()

lowest_day = daily_revenue.idxmin()

print("Highest Revenue Outlet:", top_outlet_revenue)

print("Highest Profit Outlet:", top_outlet_profit)

print("Highest Margin Outlet:", top_outlet_margin)

print("Highest Units Product:", top_product_units)

print("Highest Revenue Product:", top_product_revenue)

print("Highest Profit Product:", top_product_profit)

print("Highest Revenue Day:", highest_day)

print("Lowest Revenue Day:", lowest_day)

data_dictionary = pd.DataFrame({
    "column": data.columns,
    "data_type": data.dtypes.astype(str).values
})

print(data_dictionary)
# Data dictionary
data_dictionary.to_csv(
    "output/D1_data_dictionary.csv",
    index=False
)
audit_summary = pd.DataFrame({
    "validation_rule": quality_flags.columns,
    "invalid_records": quality_flags.sum().values
})

print(audit_summary)
# Audit summary
audit_summary.to_csv(
    "output/D2_audit_summary.csv",
    index=False
)

# Clean data
clean_data.to_csv(
    "output/D3_clean_data.csv",
    index=False
)

# Transaction metrics
clean_data.to_csv(
    "output/D4_transaction_metrics.csv",
    index=False
)

# Statistics
statistics.to_csv(
    "output/D5_statistics.csv"
)

# Outlet comparison
outlet_summary.to_csv(
    "output/D5_outlet_comparison.csv"
)

# Product comparison
product_summary.to_csv(
    "output/D5_product_comparison.csv"
)

# Daily trends
daily_table.to_csv(
    "output/D6_daily_trends.csv",
    index=False
)

# Anomaly register
anomaly_register.to_csv(
    "output/D6_anomaly_register.csv",
    index=False
)

# Scenario analysis
scenario_summary.to_csv(
    "output/D7_scenario_analysis.csv",
    index=False
)