import pandas as pd

df = pd.read_csv("data/supplier/supplier_po.csv", parse_dates=["promised_date", "actual_delivery_date"])

df["delay_days"] = (df["actual_delivery_date"] - df["promised_date"]).dt.days
delayed = df[df["delay_days"] > 5]

if not delayed.empty:
    print("SUPPLIER DELAY ALERT:")
    print(delayed[["po_id", "supplier_name", "delay_days"]].head())
else:
    print("No major supplier delays detected.")

