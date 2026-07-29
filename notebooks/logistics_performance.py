import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load logistics data
df = pd.read_csv("data/logistics/logistics_shipments.csv",
                 parse_dates=["departure_date", "eta_date", "actual_arrival_date"])
df = df.sort_values("departure_date")

print("Logistics Shipment Data Loaded:")
print(df.head())

# --------------------------------------------------
# Add new common keys if missing (supplier_name, material_id, material_name)
# --------------------------------------------------

# supplier_name (must exist for cross-filtering)
if "supplier_name" not in df.columns:
    suppliers = ["AlphaSteel", "BetaMetals", "CoreSteel", "DeltaIron", "PrimeSteel"]
    df["supplier_name"] = np.random.choice(suppliers, len(df))

# material_id
if "material_id" not in df.columns:
    material_ids = [f"MAT{100+i}" for i in range(300)]
    df["material_id"] = np.random.choice(material_ids, len(df))

# material_name
if "material_name" not in df.columns:
    materials = ["Steel Coil", "Steel Rod", "Steel Plate", "Steel Bar", "Steel Sheet"]
    df["material_name"] = np.random.choice(materials, len(df))

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
