-- Basic commodity trend query
SELECT
    date,
    steel_price,
    iron_ore_price,
    scrap_price,
    freight_index,
    fx_rate
FROM commodity_prices
ORDER BY date;

