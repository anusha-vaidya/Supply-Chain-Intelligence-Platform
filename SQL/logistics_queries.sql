-- Logistics delay summary
SELECT
    shipment_id,
    po_id,
    port_congestion_index
FROM logistics_shipments
WHERE port_congestion_index > 80;

