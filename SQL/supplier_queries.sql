-- Supplier delay summary
SELECT
    supplier_name,
    COUNT(*) AS total_pos,
    SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_pos
FROM supplier_po
GROUP BY supplier_name
ORDER BY delayed_pos DESC;

