# Data Dictionary

## commodity/commodity_prices.csv
- date
- steel_price
- iron_ore_price
- scrap_price
- freight_index
- fx_rate

## supplier/supplier_po.csv
- po_id
- supplier_name
- po_date
- promised_date
- actual_delivery_date
- quantity
- status

## logistics/logistics_shipments.csv
- shipment_id
- po_id
- vessel_name
- departure_date
- eta_date
- actual_arrival_date
- port_congestion_index

## inventory/inventory_levels.csv
- material_id
- material_name
- current_stock
- daily_consumption
- safety_stock
- last_updated

## production/bom_consumption.csv
- production_order_id
- material_id
- required_qty
- production_date

