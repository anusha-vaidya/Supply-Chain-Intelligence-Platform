import pandas as pd

inventory_df = pd.read_csv("data/inventory/inventory_levels.csv")

risk = inventory_df[inventory_df["current_stock"] < inventory_df["safety_stock"]]

if not risk.empty:
    print("INVENTORY STOCKOUT ALERT:")
    print(risk[["material_id", "material_name", "current_stock", "safety_stock"]].head())
else:
    print("No immediate stockout risk detected.")

