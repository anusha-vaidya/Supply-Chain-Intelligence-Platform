-- Inventory risk view
SELECT
    material_id,
    material_name,
    current_stock,
    safety_stock
FROM inventory_levels
WHERE current_stock < safety_stock;

