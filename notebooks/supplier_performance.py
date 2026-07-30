import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load supplier PO data
df = pd.read_csv(
    "data/supplier/supplier_po.csv",
    parse_dates=["po_date", "promised_date", "actual_delivery_date"]
)
df = df.sort_values("po_date")

print("Supplier PO Data Loaded:")
print(df.head())

# --------------------------------------------------
# Add new common keys if missing (supplier_id, material_id, material_name)
# --------------------------------------------------

# supplier_id
if "supplier_id" not in df.columns:
    supplier_map = {
        "SUP001": "AlphaSteel",
        "SUP002": "BetaMetals",
        "SUP003": "CoreSteel",
        "SUP004": "DeltaIron",
        "SUP005": "PrimeSteel"
    }
    supplier_ids = list(supplier_map.keys())
    df["supplier_id"] = np.random.choice(supplier_ids, len(df))
    df["supplier_name"] = df["supplier_id"].map(supplier_map)

# material_id + material_name
if "material_id" not in df.columns:
    material_map = {
        "MAT100": "Steel Coil",
        "MAT101": "Steel Rod",
        "MAT102": "Steel Plate",
        "MAT103": "Steel Bar",
        "MAT104": "Steel Sheet"
    }
    material_ids = list(material_map.keys())
    df["material_id"] = np.random.choice(material_ids, len(df))
    df["material_name"] = df["material_id"].map(material_map)

# --------------------------------------------------
# 1. Delay Days Calculation
# --------------------------------------------------
df["delay_days"] = (df["actual_delivery_date"] - df["promised_date"]).dt.days

print("\nDelay Summary:")
print(df["delay_days"].describe())

# --------------------------------------------------
# 2. Supplier Reliability Score
# --------------------------------------------------
supplier_summary = df.groupby("supplier_name").agg({
    "delay_days": ["mean", "max"],
    "po_id": "count"
})

supplier_summary.columns = ["avg_delay", "max_delay", "total_pos"]
supplier_summary["reliability_score"] = 100 - supplier_summary["avg_delay"]

print("\nSupplier Reliability Score:")
print(supplier_summary)

# --------------------------------------------------
# 3. Visualization
# --------------------------------------------------
plt.figure(figsize=(10, 5))
plt.bar(supplier_summary.index, supplier_summary["avg_delay"], color="tomato")
plt.title("Average Supplier Delay (Days)")
plt.xlabel("Supplier")
plt.ylabel("Avg Delay")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --------------------------------------------------
# 4. Export for Power BI
# --------------------------------------------------
supplier_summary.to_csv("data/supplier/supplier_performance_output.csv")
print("\nExported: data/supplier/supplier_performance_output.csv")
