import pandas as pd
import matplotlib.pyplot as plt

# Load logistics data
df = pd.read_csv("data/logistics/logistics_shipments.csv", parse_dates=["departure_date", "eta_date", "actual_arrival_date"])
df = df.sort_values("departure_date")

print("Logistics Shipment Data Loaded:")
print(df.head())


# 1. ETA Delay Calculation
df["eta_delay_days"] = (df["actual_arrival_date"] - df["eta_date"]).dt.days

print("\nETA Delay Summary:")
print(df["eta_delay_days"].describe())


# 2. Congestion Risk Score
df["congestion_risk"] = df["port_congestion_index"].apply(
    lambda x: "High" if x > 80 else "Medium" if x > 60 else "Low"
)

print("\nCongestion Risk Distribution:")
print(df["congestion_risk"].value_counts())

# 3. Visualization
plt.figure(figsize=(10, 5))
plt.hist(df["eta_delay_days"], bins=30, color="steelblue")
plt.title("Distribution of ETA Delays")
plt.xlabel("Delay (Days)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()


# 4. Export for Power BI
df.to_csv("data/logistics/logistics_performance_output.csv", index=False)
print("\nExported: data/logistics/logistics_performance_output.csv")

