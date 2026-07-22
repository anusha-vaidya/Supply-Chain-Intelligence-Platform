import pandas as pd

# Load supplier PO data
df = pd.read_csv("data/supplier/supplier_po.csv", parse_dates=["po_date", "promised_date", "actual_delivery_date"])

# Basic exploration
print(df.head())
print(df["status"].value_counts())

# Simple delay flag
df["delay_days"] = (df["actual_delivery_date"] - df["promised_date"]).dt.days
print(df[["supplier_name", "delay_days"]].head())


