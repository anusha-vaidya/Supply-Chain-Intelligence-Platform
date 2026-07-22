# Supply-Chain-Intelligence-Platform

This project is a simple, end‑to‑end analytics platform that shows how data flows through the supply chain. It contains three modules:

- Commodity Intelligence — commodity price trends, forecasts, and risk signals
- Supplier & Logistics Performance — supplier delays, reliability scoring, and shipment risks
- Inventory & Production Planning — inventory levels, safety stock, and stockout risk

Problems it solves:
It solves real problems supply chain teams face every day:
- Steel price volatility
- Supplier delays
- Logistics uncertainty
- Inventory shortages
- Manual reporting


How this project helps:
- It brings all supply chain data together instead of scattered Excel files, ERP screens, and emails.
- It shows trends and risks clearly through Power BI dashboards.
- It predicts issues early (price spikes, supplier delays, inventory shortages) and sends simple AI alerts.
- It mirrors their real business flow on how supply chains actually work.

Technical Stack:

- Python notebooks for data exploration, forecasting, and predictive modeling
- SQL scripts for cleaning, joining, and preparing ERP‑style datasets
- Python modules for price forecasting, delay prediction, and inventory risk simulation
- Power BI dashboards to visualize KPIs, trends, and risk indicators
- AI-driven alert scripts (Python) that flag price spikes, supplier delays, and low inventory
- GitHub Actions to run alerts automatically inside GitHub

I built the platform end‑to‑end by first cleaning and modeling mock supply chain datasets using SQL and Python. For forecasting steel prices, I used time‑series models like Prophet/SARIMAX to capture trends and volatility. Supplier delay prediction uses simple ML algorithms (RandomForest/XGBoost) trained on PO and logistics features. Inventory risk is modeled using safety‑stock formulas and Monte Carlo simulations to estimate stockout probability. All outputs feed into Power BI dashboards for clear business storytelling, while Python scripts generate automated alerts through GitHub Actions to highlight risks such as price spikes, supplier delays, or low inventory — creating a complete loop from data → model → dashboard → alert → decision.


