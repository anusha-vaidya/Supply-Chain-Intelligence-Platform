import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX


# 1. Load data
df = pd.read_csv("data/commodity/commodity_prices.csv", parse_dates=["date"])
df = df.sort_values("date")

print("Data Loaded:")
print(df.head())


# 2. Daily % Change + Volatility Score
df["pct_change"] = df["steel_price"].pct_change() * 100
df["volatility_score"] = np.where(abs(df["pct_change"]) > 3, "High", "Normal")


# 3. Seasonal Decomposition (Trend/Seasonality)
result = seasonal_decompose(df["steel_price"], model="additive", period=30)
result.plot()
plt.show()


# 4. Forecasting (SARIMAX)
train = df.iloc[:-90]
model = SARIMAX(train["steel_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit(disp=False)

forecast = results.get_forecast(steps=90)
pred = forecast.predicted_mean
conf = forecast.conf_int()

# Add forecast columns to df
df.loc[df.index[-90]:, "predicted_mean"] = pred.values
df.loc[df.index[-90]:, "lower_ci"] = conf.iloc[:, 0].values
df.loc[df.index[-90]:, "upper_ci"] = conf.iloc[:, 1].values


# 5. Export enriched dataset for Power BI
df.to_csv("data/commodity/commodity_analysis_output.csv", index=False)
print("Exported: data/commodity/commodity_analysis_output.csv")