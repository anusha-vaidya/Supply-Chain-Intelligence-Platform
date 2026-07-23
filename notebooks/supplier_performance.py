import pandas as pd
import matplotlib.pyplot as plt

# Load supplier PO data
df = pd.read_csv("data/supplier/supplier_po.csv", parse_dates=["po_date", "promised_date", "actual_delivery_date"])
df = df.sort_values("po_date")

print("Supplier PO Data Loaded:")
print(df.head())


# 1. Delay Days Calculation
df["delay_days"] = (df["actual_delivery_date"] - df["promised_date"]).dt.days

# Basic summary
print("\nDelay Summary:")
print(df["delay_days"].describe())


# 2. Supplier Reliability Score
supplier_summary = df.groupby("supplier_name").agg({
    "delay_days": ["mean", "max"],
    "po_id": "count"
})

supplier_summary.columns = ["avg_delay", "max_delay", "total_pos"]
supplier_summary["reliability_score"] = 100 - supplier_summary["avg_delay"]

print("\nSupplier Reliability Score:")
print(supplier_summary)

# 3. Visualization
plt.figure(figsize=(10, 5))
plt.bar(supplier_summary.index, supplier_summary["avg_delay"], color="tomato")
plt.title("Average Supplier Delay (Days)")
plt.xlabel("Supplier")
plt.ylabel("Avg Delay")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 4. Export for Power BI
supplier_summary.to_csv("data/supplier/supplier_performance_output.csv")
print("\nExported: data/supplier/supplier_performance_output.csv")
