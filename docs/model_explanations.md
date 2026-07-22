# Model Explanations

## Commodity Intelligence
- Uses time-series forecasting (e.g., Prophet/SARIMAX) on steel_price.
- Adds volatility and risk scores based on recent price movements.

## Supplier & Logistics Performance
- Uses classification models (e.g., RandomForest/XGBoost) to predict delay risk.
- Features include supplier_name, promised_date vs actual_delivery_date, quantity, and congestion.

## Inventory & Production Planning
- Uses safety stock formulas and Monte Carlo simulation to estimate stockout risk.
- Combines inventory_levels with bom_consumption to simulate future consumption.

