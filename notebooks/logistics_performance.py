import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load logistics data
df = pd.read_csv(
    "data/logistics/logistics_shipments.csv",
    parse_dates=["departure_date", "eta_date", "actual_arrival_date"]
)
df = df.sort_values("departure_date")

print("Logistics Shipment Data Loaded:")
print(df.head())

# --------------------------------------------------
# Add new common keys if missing (supplier_id, supplier_name, material_id, material_name)
# --------------------------------------------------

# supplier_id + supplier_name
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
# 1. ETA Delay Calculation
# --------------------------------------------------
df["eta_delay_days"] = (df["actual_arrival_date"] - df["eta_date"]).dt.days

print("\nETA Delay Summary:")
print(df["eta_delay_days"].describe())

# --------------------------------------------------
# 2. Congestion Risk Score
# --------------------------------------------------
df["congestion_risk"] = df["port_congestion_index"].apply(
    lambda x: "High" if x > 80 else "Medium" if x > 60 else "Low"
)

print("\nCongestion Risk Distribution:")
print(df["congestion_risk"].value_counts())

# --------------------------------------------------
# 3. Visualization
# --------------------------------------------------
plt.figure(figsize=(10, 5))
plt.hist(df["eta_delay_days"], bins=30, color="steelblue")
plt.title("Distribution of ETA Delays")
plt.xlabel("Delay (Days)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# --------------------------------------------------
# 4. Export for Power BI
# --------------------------------------------------
df.to_csv("data/logistics/logistics_performance_output.csv", index=False)
print("\nExported: data/logistics/logistics_performance_output.csv")
