
import pandas as pd
import numpy as np

np.random.seed(42)

# STEP 1: CREATE DATASET

rows = 5000

data = pd.DataFrame({
    "transaction_id": np.arange(100001, 100001 + rows, dtype=np.int64),
    "day_index": np.random.randint(1, 31, rows).astype("int64"),
    "outlet_id": np.random.randint(1, 4, rows).astype("int64"),
    "product_code": np.random.choice(["P101", "P102", "P103", "P104", "P105"], rows),
    "category_code": "",
    "quantity": np.random.randint(1, 11, rows).astype("int64"),
    "unit_price": np.round(np.random.uniform(20, 200, rows), 2),
    "unit_cost": np.round(np.random.uniform(10, 150, rows), 2),
    "discount_rate": np.round(np.random.uniform(0, 0.30, rows), 2),
    "stock_before_units": np.random.randint(1, 100, rows).astype("int64"),
    "payment_code": np.random.choice(["CASH", "CARD", "UPI"], rows),
    "customer_rating": np.random.randint(1, 6, rows).astype("float64")
})

# STEP 2: PRODUCT CATEGORY MAPPING

product_category = {
    "P101": "C1",
    "P102": "C1",
    "P103": "C2",
    "P104": "C2",
    "P105": "C3"
}

data["category_code"] = data["product_code"].map(product_category)

# STEP 3: INSERT DATA QUALITY CASES

# Missing unit price - 4
data.loc[0:3, "unit_price"] = np.nan

# Missing unit cost - 4
data.loc[4:7, "unit_cost"] = np.nan

# Missing customer rating - 20
data.loc[8:27, "customer_rating"] = np.nan

# Duplicate transaction IDs - 5 records involved
data.loc[28:31, "transaction_id"] = data.loc[27, "transaction_id"]

# Zero or negative quantity - 4
data.loc[32:35, "quantity"] = np.array([0, -1, 0, -2], dtype="int64")

# Negative unit price - 2
data.loc[36:37, "unit_price"] = np.array([-10, -25], dtype="float64")

# Negative unit cost - 2
data.loc[38:39, "unit_cost"] = np.array([-5, -15], dtype="float64")

# Discount rate above 1 - 2
data.loc[40:41, "discount_rate"] = np.array([1.2, 1.5], dtype="float64")

# Invalid customer rating - 3
data.loc[42:44, "customer_rating"] = np.array([0, 6, 8], dtype="float64")

# Inconsistent product/category mapping - 4
data.loc[45:48, "category_code"] = ["C3", "C3", "C1", "C3"]

# Unknown outlet code - 2
data.loc[49:50, "outlet_id"] = np.array([99, 100], dtype="int64")

# Unusually high but valid price - 3
data.loc[51:53, "unit_price"] = np.array([500, 750, 1000], dtype="float64")

# Unusually high but valid discount - 5
data.loc[54:58, "discount_rate"] = np.array([0.70, 0.80, 0.85, 0.90, 0.95], dtype="float64")

# Zero stock before transaction - 5
data.loc[59:63, "stock_before_units"] = np.array([0, 0, 0, 0, 0], dtype="int64")

# STEP 4: SAVE DATASET

data.to_csv("freshflow_sales.csv", index=False)

# STEP 5: DISPLAY RESULTS

print("Dataset generated successfully!")
print("Dataset shape:", data.shape)

print("\nFirst 5 rows:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate transaction IDs:")
print(data["transaction_id"].duplicated().sum())

print("\nCSV saved as freshflow_sales.csv")
