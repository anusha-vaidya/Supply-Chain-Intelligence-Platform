import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA


# 1. Load data
df = pd.read_csv("data/commodity/commodity_prices.csv", parse_dates=["date"])
df = df.sort_values("date")

print("Data Loaded:")
print(df.head())


# 2. Daily % Change + Volatility Score
df["pct_change"] = df["steel_price"].pct_change() * 100
df["volatility_score"] = np.where(abs(df["pct_change"]) > 3, "High", "Normal")


# 3. Seasonal Decomposition (for visualization only)
result = seasonal_decompose(df["steel_price"], model="additive", period=30)
result.plot()
plt.show()


# 4. Forecasting (ARIMA — stable for daily data)
print("Running ARIMA forecast block...")

train = df["steel_price"]

# ARIMA model (non-seasonal)
model = ARIMA(train, order=(5, 1, 2))
results = model.fit()

forecast_steps = 90
pred = results.forecast(steps=forecast_steps)

# Simple confidence intervals
lower_ci = pred - 20
upper_ci = pred + 20


# 5. Build future date range
last_date = df["date"].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps)


# 6. Build forecast dataframe with EXACT matching columns
forecast_df = pd.DataFrame({
    "date": future_dates,
    "steel_price": [np.nan] * forecast_steps,
    "iron_ore_price": [np.nan] * forecast_steps,
    "scrap_price": [np.nan] * forecast_steps,
    "freight_index": [np.nan] * forecast_steps,
    "fx_rate": [np.nan] * forecast_steps,
    "pct_change": [np.nan] * forecast_steps,
    "volatility_score": ["Forecast"] * forecast_steps,
    "predicted_mean": pred.values,
    "lower_ci": lower_ci.values,
    "upper_ci": upper_ci.values
})


# 7. Append forecast rows to original data
df = pd.concat([df, forecast_df], ignore_index=True)

print("Last 10 rows:")
print(df.tail(10))


# 8. Export enriched dataset
df.to_csv("data/commodity/commodity_analysis_output.csv", index=False)
print("Exported: data/commodity/commodity_analysis_output.csv")
