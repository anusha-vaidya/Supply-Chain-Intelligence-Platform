import pandas as pd

df = pd.read_csv("data/commodity/commodity_prices.csv", parse_dates=["date"])
df = df.sort_values("date")

df["pct_change"] = df["steel_price"].pct_change() * 100

spikes = df[df["pct_change"] > 5]  # >5% daily increase

if not spikes.empty:
    print("PRICE SPIKE ALERT:")
    print(spikes[["date", "steel_price", "pct_change"]].tail())
else:
    print("No significant price spikes detected.")

