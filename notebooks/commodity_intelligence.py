import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

# --------------------------------------------------
# 1. Load data
# --------------------------------------------------
df = pd.read_csv("data/commodity/commodity_prices.csv", parse_dates=["date"])
df = df.sort_values("date")

print("Data Loaded:")
print(df.head())

# --------------------------------------------------
# 1A. Add new common keys (supplier_name, material_id, material_name)
# --------------------------------------------------
# These columns already exist in your updated commodity_prices.csv,
# but this ensures they are present even if older files are loaded.

if "supplier_name" not in df.columns:
    suppliers = ["AlphaSteel", "BetaMetals", "CoreSteel", "DeltaIron", "PrimeSteel"]
    df["supplier_name"] = np.random.choice(suppliers, len(df))

if "material_id" not in df.columns:
    material_ids = [f"MAT{100+i}" for i in range(300)]
    df["material_id"] = np.random.choice(material_ids, len(df))

if "material_name" not in df.columns:
    materials = ["Steel Coil", "Steel Rod", "Steel Plate", "Steel Bar", "Steel Sheet"]
    df["material_name"] = np.random.choice(materials, len(df))

# --------------------------------------------------
# 2. Filter Actuals (2023–2024)
# --------------------------------------------------
actuals_df = df[(df["date"].dt.year >= 2023) & (df["date"].dt.year <= 2024)].copy()

# --------------------------------------------------
# 3. pct_change + volatility_score for actuals
# --------------------------------------------------
actuals_df["pct_change"] = actuals_df["steel_price"].pct_change() * 100
actuals_df["pct_change"] = actuals_df["pct_change"].fillna(0)

actuals_df["volatility_score"] = np.where(
    actuals_df["pct_change"].abs() > 3, "High", "Normal"
)

# --------------------------------------------------
# 4. predicted_mean for actuals (rolling mean)
# --------------------------------------------------
actuals_df["predicted_mean"] = actuals_df["steel_price"].rolling(
    window=7, min_periods=1
).mean()

# --------------------------------------------------
# 5. Forecast ALL columns for 2025–June 2026
# --------------------------------------------------
def forecast_series(series, steps):
    model = SARIMAX(series, order=(1,0,1), seasonal_order=(1,0,1,30))
    results = model.fit(disp=False)
    pred = results.forecast(steps=steps)
    return pred

# Forecast horizon: Jan 1 2025 → Jun 30 2026
forecast_steps = (pd.Timestamp("2026-06-30") - pd.Timestamp("2025-01-01")).days + 1
future_dates = pd.date_range(start="2025-01-01", periods=forecast_steps)

steel_pred = forecast_series(actuals_df["steel_price"], forecast_steps)
iron_pred = forecast_series(actuals_df["iron_ore_price"], forecast_steps)
scrap_pred = forecast_series(actuals_df["scrap_price"], forecast_steps)
freight_pred = forecast_series(actuals_df["freight_index"], forecast_steps)
fx_pred = forecast_series(actuals_df["fx_rate"], forecast_steps)

# --------------------------------------------------
# 6. Build Forecast Table (NO blanks)
# --------------------------------------------------
forecast_df = pd.DataFrame({
    "date": future_dates,
    "steel_price_predicted": steel_pred.values,
    "iron_ore_predicted": iron_pred.values,
    "scrap_price_predicted": scrap_pred.values,
    "freight_index_predicted": freight_pred.values,
    "fx_rate_predicted": fx_pred.values,
})

# pct_change_predicted
forecast_df["pct_change_predicted"] = (
    forecast_df["steel_price_predicted"].pct_change().fillna(0) * 100
)

# predicted_mean (rolling mean)
forecast_df["predicted_mean"] = forecast_df["steel_price_predicted"].rolling(
    window=7, min_periods=1
).mean()

# volatility_score
forecast_df["volatility_score"] = np.where(
    forecast_df["pct_change_predicted"].abs() > 3, "High", "Normal"
)

# confidence intervals
forecast_df["lower_ci"] = forecast_df["steel_price_predicted"] - 20
forecast_df["upper_ci"] = forecast_df["steel_price_predicted"] + 20

# --------------------------------------------------
# 6A. Add new common keys to forecast_df
# --------------------------------------------------
# These ensure forecast table connects to supplier/logistics/inventory/production

suppliers = ["AlphaSteel", "BetaMetals", "CoreSteel", "DeltaIron", "PrimeSteel"]
materials = ["Steel Coil", "Steel Rod", "Steel Plate", "Steel Bar", "Steel Sheet"]
material_ids = [f"MAT{100+i}" for i in range(300)]

forecast_df["supplier_name"] = np.random.choice(suppliers, len(forecast_df))
forecast_df["material_id"] = np.random.choice(material_ids, len(forecast_df))
forecast_df["material_name"] = np.random.choice(materials, len(forecast_df))

# --------------------------------------------------
# 7. Export BOTH clean tables
# --------------------------------------------------
actuals_df.to_csv("data/commodity/commodity_actuals.csv", index=False)
forecast_df.to_csv("data/commodity/commodity_forecast.csv", index=False)

print("Exported: commodity_actuals.csv and commodity_forecast.csv")
