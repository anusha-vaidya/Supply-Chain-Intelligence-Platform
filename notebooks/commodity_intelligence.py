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
# 1A. Add new common keys (supplier_id, supplier_name, material_id, material_name)
# --------------------------------------------------

# supplier_id + supplier_name
if "supplier_id" not in df.columns:
    supplier_map = {
        "SUP001": "AlphaSteel",
        "SUP002": "BetaMetals",
        "SUP003": "CoreSteel",
        "SUP004": "DeltaIron",
        "SUP005": "PrimeSteel"
    }
    supplier_ids = list(supplier_map.keys())
    df["supplier_id"] = np.random.choice(supplier_ids, len(df))
    df["supplier_name"] = df["supplier_id"].map(supplier_map)

# material_id + material_name
if "material_id" not in df.columns:
    material_map = {
        "MAT100": "Steel Coil",
        "MAT101": "Steel Rod",
        "MAT102": "Steel Plate",
        "MAT103": "Steel Bar",
        "MAT104": "Steel Sheet"
    }
    material_ids = list(material_map.keys())
    df["material_id"] = np.random.choice(material_ids, len(df))
    df["material_name"] = df["material_id"].map(material_map)

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

forecast_df["pct_change_predicted"] = (
    forecast_df["steel_price_predicted"].pct_change().fillna(0) * 100
)

forecast_df["predicted_mean"] = forecast_df["steel_price_predicted"].rolling(
    window=7, min_periods=1
).mean()

forecast_df["volatility_score"] = np.where(
    forecast_df["pct_change_predicted"].abs() > 3, "High", "Normal"
)

forecast_df["lower_ci"] = forecast_df["steel_price_predicted"] - 20
forecast_df["upper_ci"] = forecast_df["steel_price_predicted"] + 20

# --------------------------------------------------
# 6A. Add new common keys to forecast_df
# --------------------------------------------------

supplier_map = {
    "SUP001": "AlphaSteel",
    "SUP002": "BetaMetals",
    "SUP003": "CoreSteel",
    "SUP004": "DeltaIron",
    "SUP005": "PrimeSteel"
}
supplier_ids = list(supplier_map.keys())

material_map = {
    "MAT100": "Steel Coil",
    "MAT101": "Steel Rod",
    "MAT102": "Steel Plate",
    "MAT103": "Steel Bar",
    "MAT104": "Steel Sheet"
}
material_ids = list(material_map.keys())

forecast_df["supplier_id"] = np.random.choice(supplier_ids, len(forecast_df))
forecast_df["supplier_name"] = forecast_df["supplier_id"].map(supplier_map)

forecast_df["material_id"] = np.random.choice(material_ids, len(forecast_df))
forecast_df["material_name"] = forecast_df["material_id"].map(material_map)

# --------------------------------------------------
# 7. Export BOTH clean tables
# --------------------------------------------------
actuals_df.to_csv("data/commodity/commodity_actuals.csv", index=False)
forecast_df.to_csv("data/commodity/commodity_forecast.csv", index=False)

print("Exported: commodity_actuals.csv and commodity_forecast.csv")
