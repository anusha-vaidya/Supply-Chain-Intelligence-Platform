import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load datasets
inventory_df = pd.read_csv("data/inventory/inventory_levels.csv")
bom_df = pd.read_csv("data/production/bom_consumption.csv", parse_dates=["production_date"])

print("Inventory Data Loaded:")
print(inventory_df.head())

print("\nBOM Consumption Data Loaded:")
print(bom_df.head())

# --------------------------------------------------
# Add new common keys if missing (supplier_name, material_id, material_name)
# --------------------------------------------------

# supplier_name (must exist for cross-filtering)
if "supplier_name" not in inventory_df.columns:
    suppliers = ["AlphaSteel", "BetaMetals", "CoreSteel", "DeltaIron", "PrimeSteel"]
    inventory_df["supplier_name"] = np.random.choice(suppliers, len(inventory_df))

if "supplier_name" not in bom_df.columns:
    suppliers = ["AlphaSteel", "BetaMetals", "CoreSteel", "DeltaIron", "PrimeSteel"]
    bom_df["supplier_name"] = np.random.choice(suppliers, len(bom_df))

# material_id already exists in both tables
# material_name already exists in inventory_df
# If missing in BOM, add it
if "material_name" not in bom_df.columns:
    materials = ["Steel Coil", "Steel Rod", "Steel Plate", "Steel Bar", "Steel Sheet"]
    bom_df["material_name"] = np.random.choice(materials, len(bom_df))

# 1. Basic Stockout Risk (Current Stock vs Safety Stock)
inventory_df["stockout_risk_flag"] = inventory_df["current_stock"] < inventory_df["safety_stock"]

print("\nStockout Risk Summary:")
print(inventory_df["stockout_risk_flag"].value_counts())


# 2. Daily Consumption Forecast (Simple Projection)
inventory_df["days_until_stockout"] = (
    inventory_df["current_stock"] / inventory_df["daily_consumption"]
).round(1)

print("\nDays Until Stockout:")
print(inventory_df[["material_id", "material_name", "days_until_stockout"]].head())


# 3. BOM-Based Consumption Simulation
# Sum required quantities per material
future_consumption = bom_df.groupby("material_id")["required_qty"].sum().reset_index()
future_consumption.columns = ["material_id", "total_future_consumption"]

# Merge with inventory
merged = inventory_df.merge(future_consumption, on="material_id", how="left")
merged["total_future_consumption"] = merged["total_future_consumption"].fillna(0)

# Predict stock after BOM consumption
merged["projected_stock"] = merged["current_stock"] - merged["total_future_consumption"]

# Flag projected stockout
merged["projected_stockout_flag"] = merged["projected_stock"] < merged["safety_stock"]

print("\nProjected Stockout Summary:")
print(merged["projected_stockout_flag"].value_counts())


# 4. Visualization
plt.figure(figsize=(10, 5))
plt.hist(merged["days_until_stockout"], bins=30, color="darkgreen")
plt.title("Distribution of Days Until Stockout")
plt.xlabel("Days")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 5. Export for Power BI
merged.to_csv("data/inventory/inventory_planning_output.csv", index=False)
print("\nExported: data/inventory/inventory_planning_output.csv")
