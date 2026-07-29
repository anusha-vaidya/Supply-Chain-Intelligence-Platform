import pandas as pd
import numpy as np
import os

# Ensure folders exist
os.makedirs("data/commodity", exist_ok=True)
os.makedirs("data/supplier", exist_ok=True)
os.makedirs("data/logistics", exist_ok=True)
os.makedirs("data/inventory", exist_ok=True)
os.makedirs("data/production", exist_ok=True)

# --------------------------------------------------
# 1. Commodity prices (ADD supplier_name + material_id)
# --------------------------------------------------
dates = pd.date_range(start="2022-01-01", end="2024-12-31")

suppliers = ["AlphaSteel", "BetaMetals", "CoreSteel", "DeltaIron", "PrimeSteel"]
materials = ["Steel Coil", "Steel Rod", "Steel Plate", "Steel Bar", "Steel Sheet"]
material_ids = [f"MAT{100+i}" for i in range(len(materials))]

commodity_df = pd.DataFrame({
    "date": dates,
    "steel_price": np.random.normal(700, 40, len(dates)),
    "iron_ore_price": np.random.normal(110, 10, len(dates)),
    "scrap_price": np.random.normal(350, 20, len(dates)),
    "freight_index": np.random.normal(1000, 80, len(dates)),
    "fx_rate": np.random.normal(83, 1, len(dates)),

    # NEW universal keys
    "supplier_name": np.random.choice(suppliers, len(dates)),
    "material_id": np.random.choice(material_ids, len(dates)),
    "material_name": np.random.choice(materials, len(dates))
})

commodity_df.to_csv("data/commodity/commodity_prices.csv", index=False)

# --------------------------------------------------
# 2. Supplier POs (ADD material_id + material_name)
# --------------------------------------------------
rows = 2000
po_dates = pd.date_range("2023-01-01", periods=rows, freq="D")

supplier_df = pd.DataFrame({
    "po_id": [f"PO{1000+i}" for i in range(rows)],
    "supplier_name": np.random.choice(suppliers, rows),
    "po_date": po_dates,
    "promised_date": po_dates + pd.to_timedelta(np.random.randint(10, 20, rows), unit="D"),
    "actual_delivery_date": po_dates + pd.to_timedelta(np.random.randint(10, 30, rows), unit="D"),
    "quantity": np.random.randint(10, 200, rows),
    "status": np.random.choice(["On-Time", "Delayed"], rows, p=[0.7, 0.3]),

    # NEW universal keys
    "material_id": np.random.choice(material_ids, rows),
    "material_name": np.random.choice(materials, rows)
})

supplier_df.to_csv("data/supplier/supplier_po.csv", index=False)

# --------------------------------------------------
# 3. Logistics shipments (ADD supplier_name + material_id)
# --------------------------------------------------
rows = 1500
departure_dates = supplier_df["po_date"].sample(rows).values

shipment_df = pd.DataFrame({
    "shipment_id": [f"SHP{2000+i}" for i in range(rows)],
    "po_id": np.random.choice(supplier_df["po_id"], rows),
    "vessel_name": np.random.choice(["MV Horizon", "MV OceanStar", "MV Titan"], rows),
    "departure_date": departure_dates,
    "eta_date": pd.to_datetime(departure_dates) + pd.to_timedelta(np.random.randint(10, 25, rows), unit="D"),
    "actual_arrival_date": pd.to_datetime(departure_dates) + pd.to_timedelta(np.random.randint(12, 35, rows), unit="D"),
    "port_congestion_index": np.random.randint(40, 95, rows),

    # NEW universal keys
    "supplier_name": np.random.choice(suppliers, rows),
    "material_id": np.random.choice(material_ids, rows),
    "material_name": np.random.choice(materials, rows)
})

shipment_df.to_csv("data/logistics/logistics_shipments.csv", index=False)

# --------------------------------------------------
# 4. Inventory levels (ADD supplier_name)
# --------------------------------------------------
rows = 300

inventory_df = pd.DataFrame({
    "material_id": material_ids[:rows] if rows <= len(material_ids) else np.random.choice(material_ids, rows),
    "material_name": np.random.choice(materials, rows),
    "current_stock": np.random.randint(50, 500, rows),
    "daily_consumption": np.random.randint(5, 40, rows),
    "safety_stock": np.random.randint(80, 200, rows),
    "last_updated": pd.to_datetime("2024-01-15"),

    # NEW universal key
    "supplier_name": np.random.choice(suppliers, rows)
})

inventory_df.to_csv("data/inventory/inventory_levels.csv", index=False)

# --------------------------------------------------
# 5. BOM consumption (ADD supplier_name)
# --------------------------------------------------
rows = 800
prod_dates = pd.date_range("2024-01-01", periods=rows, freq="D")

bom_df = pd.DataFrame({
    "production_order_id": [f"PROD{500+i}" for i in range(rows)],
    "material_id": np.random.choice(inventory_df["material_id"], rows),
    "required_qty": np.random.randint(10, 100, rows),
    "production_date": prod_dates,

    # NEW universal key
    "supplier_name": np.random.choice(suppliers, rows)
})

bom_df.to_csv("data/production/bom_consumption.csv", index=False)
