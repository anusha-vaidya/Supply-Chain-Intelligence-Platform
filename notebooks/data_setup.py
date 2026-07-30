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
# FIXED MATERIAL MAPPING (1-to-1 mapping)
# --------------------------------------------------
material_map = {
    "MAT100": "Steel Coil",
    "MAT101": "Steel Rod",
    "MAT102": "Steel Plate",
    "MAT103": "Steel Bar",
    "MAT104": "Steel Sheet"
}

material_ids = list(material_map.keys())
materials = list(material_map.values())

# --------------------------------------------------
# FIXED SUPPLIER MAPPING (1-to-1 mapping)
# --------------------------------------------------
supplier_map = {
    "SUP001": "AlphaSteel",
    "SUP002": "BetaMetals",
    "SUP003": "CoreSteel",
    "SUP004": "DeltaIron",
    "SUP005": "PrimeSteel"
}

supplier_ids = list(supplier_map.keys())
suppliers = list(supplier_map.values())

# --------------------------------------------------
# 1. Commodity prices
# --------------------------------------------------
dates = pd.date_range(start="2022-01-01", end="2024-12-31")

commodity_supplier_ids = np.random.choice(supplier_ids, len(dates))
commodity_material_ids = np.random.choice(material_ids, len(dates))

commodity_df = pd.DataFrame({
    "date": dates,
    "steel_price": np.random.normal(700, 40, len(dates)),
    "iron_ore_price": np.random.normal(110, 10, len(dates)),
    "scrap_price": np.random.normal(350, 20, len(dates)),
    "freight_index": np.random.normal(1000, 80, len(dates)),
    "fx_rate": np.random.normal(83, 1, len(dates)),

    "supplier_id": commodity_supplier_ids,
    "supplier_name": [supplier_map[sid] for sid in commodity_supplier_ids],

    "material_id": commodity_material_ids,
    "material_name": [material_map[mid] for mid in commodity_material_ids]
})

commodity_df.to_csv("data/commodity/commodity_prices.csv", index=False)

# --------------------------------------------------
# 2. Supplier POs
# --------------------------------------------------
rows = 2000
po_dates = pd.date_range("2023-01-01", periods=rows, freq="D")

supplier_supplier_ids = np.random.choice(supplier_ids, rows)
supplier_material_ids = np.random.choice(material_ids, rows)

supplier_df = pd.DataFrame({
    "po_id": [f"PO{1000+i}" for i in range(rows)],
    "supplier_id": supplier_supplier_ids,
    "supplier_name": [supplier_map[sid] for sid in supplier_supplier_ids],

    "po_date": po_dates,
    "promised_date": po_dates + pd.to_timedelta(np.random.randint(10, 20, rows), unit="D"),
    "actual_delivery_date": po_dates + pd.to_timedelta(np.random.randint(10, 30, rows), unit="D"),
    "quantity": np.random.randint(10, 200, rows),
    "status": np.random.choice(["On-Time", "Delayed"], rows, p=[0.7, 0.3]),

    "material_id": supplier_material_ids,
    "material_name": [material_map[mid] for mid in supplier_material_ids]
})

supplier_df.to_csv("data/supplier/supplier_po.csv", index=False)

# --------------------------------------------------
# 3. Logistics shipments
# --------------------------------------------------
rows = 1500
departure_dates = supplier_df["po_date"].sample(rows).values

log_supplier_ids = np.random.choice(supplier_ids, rows)
log_material_ids = np.random.choice(material_ids, rows)

shipment_df = pd.DataFrame({
    "shipment_id": [f"SHP{2000+i}" for i in range(rows)],
    "po_id": np.random.choice(supplier_df["po_id"], rows),

    "supplier_id": log_supplier_ids,
    "supplier_name": [supplier_map[sid] for sid in log_supplier_ids],

    "material_id": log_material_ids,
    "material_name": [material_map[mid] for mid in log_material_ids],

    "vessel_name": np.random.choice(["MV Horizon", "MV OceanStar", "MV Titan"], rows),
    "departure_date": departure_dates,
    "eta_date": pd.to_datetime(departure_dates) + pd.to_timedelta(np.random.randint(10, 25, rows), unit="D"),
    "actual_arrival_date": pd.to_datetime(departure_dates) + pd.to_timedelta(np.random.randint(12, 35, rows), unit="D"),
    "port_congestion_index": np.random.randint(40, 95, rows)
})

shipment_df.to_csv("data/logistics/logistics_shipments.csv", index=False)

# --------------------------------------------------
# 4. Inventory levels
# --------------------------------------------------
rows = 300

inv_supplier_ids = np.random.choice(supplier_ids, rows)
inv_material_ids = np.random.choice(material_ids, rows)

inventory_df = pd.DataFrame({
    "supplier_id": inv_supplier_ids,
    "supplier_name": [supplier_map[sid] for sid in inv_supplier_ids],

    "material_id": inv_material_ids,
    "material_name": [material_map[mid] for mid in inv_material_ids],

    "current_stock": np.random.randint(50, 500, rows),
    "daily_consumption": np.random.randint(5, 40, rows),
    "safety_stock": np.random.randint(80, 200, rows),
    "last_updated": pd.to_datetime("2024-01-15")
})

inventory_df.to_csv("data/inventory/inventory_levels.csv", index=False)

# --------------------------------------------------
# 5. BOM consumption
# --------------------------------------------------
rows = 800
prod_dates = pd.date_range("2024-01-01", periods=rows, freq="D")

bom_supplier_ids = np.random.choice(supplier_ids, rows)
bom_material_ids = np.random.choice(material_ids, rows)

bom_df = pd.DataFrame({
    "production_order_id": [f"PROD{500+i}" for i in range(rows)],

    "supplier_id": bom_supplier_ids,
    "supplier_name": [supplier_map[sid] for sid in bom_supplier_ids],

    "material_id": bom_material_ids,
    "material_name": [material_map[mid] for mid in bom_material_ids],

    "required_qty": np.random.randint(10, 100, rows),
    "production_date": prod_dates
})

bom_df.to_csv("data/production/bom_consumption.csv", index=False)
