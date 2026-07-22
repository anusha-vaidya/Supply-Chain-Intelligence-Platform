import pandas as pd

inventory_df = pd.read_csv("data/inventory/inventory_levels.csv")
bom_df = pd.read_csv("data/production/bom_consumption.csv")

print(inventory_df.head())
print(bom_df.head())

# Simple stockout risk flag
inventory_df["stockout_risk"] = inventory_df["current_stock"] < inventory_df["safety_stock"]
print(inventory_df[["material_id", "material_name", "current_stock", "safety_stock", "stockout_risk"]].head())


