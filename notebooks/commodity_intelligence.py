import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.statespace.sarimax import SARIMAX


# --------------------------------------------------
# 4. Forecasting (SARIMAX)
# --------------------------------------------------
train = df.iloc[:-90]
model = SARIMAX(train["steel_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit(disp=False)

# Forecast next 90 days beyond last date
forecast_steps = 90
forecast = results.get_forecast(steps=forecast_steps)
pred = forecast.predicted_mean
conf = forecast.conf_int()

# Create future date range
last_date = df["date"].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps)

# Build forecast dataframe
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

# Append forecast rows to original data
df = pd.concat([df, forecast_df], ignore_index=True)

# --------------------------------------------------
# 5. Export enriched dataset for Power BI
# --------------------------------------------------
df.to_csv("data/commodity/commodity_analysis_output.csv", index=False)
print("Exported: data/commodity/commodity_analysis_output.csv")
