import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/commodity/commodity_prices.csv", parse_dates=["date"])

# Basic exploration
print(df.head())
print(df.describe())

# Simple trend plot
plt.figure(figsize=(10, 4))
plt.plot(df["date"], df["steel_price"])
plt.title("Steel Price Trend")
plt.xlabel("Date")
plt.ylabel("Price")
plt.tight_layout()
plt.show()

df.to_csv("data/commodity/commodity_analysis_output.csv", index=False)
print("Exported: data/commodity/commodity_analysis_output.csv")

