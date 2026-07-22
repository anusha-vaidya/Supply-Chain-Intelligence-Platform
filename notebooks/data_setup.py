import pandas as pd
import numpy as np
import os

# Ensure folders exist
os.makedirs("data/commodity", exist_ok=True)
os.makedirs("data/supplier", exist_ok=True)
os.makedirs("data/logistics", exist_ok=True)
os.makedirs("data/inventory", exist_ok=True)
os.makedirs("data/production", exist_ok=True)

# 1. Commodity prices
dates = pd.date_range(start="2022-01-01", end="2024-12-31")

commodity_df = pd.DataFrame({
    "date": dates,
    "steel_price": np.random.normal(700, 40, len(dates)),
    "iron_ore_price": np.random.normal(110, 10, len(dates)),
    "scrap_price": np.random.normal(350, 20, len(dates)),
    "freight_index": np.random.normal(1000, 80, len(dates)),
    "fx_rate": np.random.normal(83, 1, len(dates))
})

commodity_df.to_csv("data/commodity/commodity_prices.csv", index=False)

# 2. Supplier POs
suppliers = ["AlphaSteel", "BetaMetals", "CoreSteel", "DeltaIron", "PrimeSteel"]
rows = 2000
po_dates = pd.date_range("2023-01-01", periods=rows, freq="D")

supplier_df = pd.DataFrame({
    "po_id": [f"PO{1000+i}" for i in range(rows)],
    "supplier_name": np.random.choice(suppliers, rows),
    "po_date": po_dates,
    "promised_date": po_dates + pd.to_timedelta(np.random.randint(10, 20, rows), unit="D"),
    "actual_delivery_date": po_dates + pd.to_timedelta(np.random.randint(10, 30, rows), unit="D"),
    "quantity": np.random.randint(10, 200, rows),
    "status": np.random.choice(["On-Time", "Delayed"], rows, p=[0.7, 0.3])
})

supplier_df.to_csv("data/supplier/supplier_po.csv", index=False)

# 3. Logistics shipments
rows = 1500
shipment_df = pd.DataFrame({
    "shipment_id": [f"SHP{2000+i}" for i in range(rows)],
    "po_id": np.random.choice(supplier_df["po_id"], rows),
    "vessel_name": np.random.choice(["MV Horizon", "MV OceanStar", "MV Titan"], rows),
    "departure_date": supplier_df["po_date"].sample(rows).values,
    "eta_date": pd.to_datetime(supplier_df["po_date"].sample(rows).values) + pd.to_timedelta(np.random.randint(10, 25, rows), unit="D"),
    "actual_arrival_date": pd.to_datetime(supplier_df["po_date"].sample(rows).values) + pd.to_timedelta(np.random.randint(12, 35, rows), unit="D"),
    "port_congestion_index": np.random.randint(40, 95, rows)
})

shipment_df.to_csv("data/logistics/logistics_shipments.csv", index=False)

# 4. Inventory levels
materials = ["Steel Coil", "Steel Rod", "Steel Plate", "Steel Bar", "Steel Sheet"]
rows = 300

inventory_df = pd.DataFrame({
    "material_id": [f"MAT{100+i}" for i in range(rows)],
    "material_name": np.random.choice(materials, rows),
    "current_stock": np.random.randint(50, 500, rows),
    "daily_consumption": np.random.randint(5, 40, rows),
    "safety_stock": np.random.randint(80, 200, rows),
    "last_updated": pd.to_datetime("2024-01-15")
})

inventory_df.to_csv("data/inventory/inventory_levels.csv", index=False)

# 5. BOM consumption
rows = 800

bom_df = pd.DataFrame({
    "production_order_id": [f"PROD{500+i}" for i in range(rows)],
    "material_id": np.random.choice(inventory_df["material_id"], rows),
    "required_qty": np.random.randint(10, 100, rows),
    "production_date": pd.date_range("2024-01-01", periods=rows, freq="D")
})

bom_df.to_csv("data/production/bom_consumption.csv", index=False)
