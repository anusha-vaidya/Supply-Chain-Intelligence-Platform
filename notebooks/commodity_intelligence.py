import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

# --------------------------------------------------
# 1. Load data
# --------------------------------------------------
df = pd.read_csv("data/commodity/commodity_prices.csv", parse_dates=["date"])
df = df.sort_values("date")

print("Data Loaded:")
print(df.head())

# --------------------------------------------------
# 2. Daily % Change + Volatility Score
# --------------------------------------------------
df["pct_change"] = df["steel_price"].pct_change() * 100
df["volatility_score"] = np.where(abs(df["pct_change"]) > 3, "High", "Normal")

# --------------------------------------------------
# 3. Seasonal Decomposition
# --------------------------------------------------
result = seasonal_decompose(df["steel_price"], model="additive", period=30)
result.plot()
plt.show()

# --------------------------------------------------
# 4. Forecasting (SARIMAX)
# --------------------------------------------------
train = df.iloc[:-90]
model = SARIMAX(train["steel_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit(disp=False)

forecast_steps = 90
forecast = results.get_forecast(steps=forecast_steps)
pred = forecast.predicted_mean
conf = forecast.conf_int()

last_date = df["date"].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps)

forecast_df = pd.DataFrame({
    "date": future_dates,
    "steel_price": np.nan,
    "iron_ore_price": np.nan,
    "scrap_price": np.nan,
    "freight_index": np.nan,
    "fx_rate": np.nan,
    "pct_change": np.nan,
    "volatility_score": "Forecast",
    "predicted_mean": pred.values,
    "lower_ci": conf.iloc[:, 0].values,
    "upper_ci": conf.iloc[:, 1].values
})

df = pd.concat([df, forecast_df], ignore_index=True)

# --------------------------------------------------
# 5. Export enriched dataset
# --------------------------------------------------
df.to_csv("data/commodity/commodity_analysis_output.csv", index=False)
print("Exported: data/commodity/commodity_analysis_output.csv")
