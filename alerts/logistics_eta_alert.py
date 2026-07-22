import pandas as pd

df = pd.read_csv("data/logistics/logistics_shipments.csv", parse_dates=["eta_date", "actual_arrival_date"])

df["delay_days"] = (df["actual_arrival_date"] - df["eta_date"]).dt.days
delayed = df[df["delay_days"] > 3]

if not delayed.empty:
    print("LOGISTICS ETA ALERT:")
    print(delayed[["shipment_id", "po_id", "delay_days", "port_congestion_index"]].head())
else:
    print("No major ETA delays detected.")

