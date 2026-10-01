-- SQLite. Run: sqlite3 -header -column data/processed/zomato.sqlite < sql/market_analysis.sql
-- Zero source ratings and non-positive costs are already NULL in processed data.
SELECT market, COUNT(*) AS restaurants, COUNT(rating) AS rated_restaurants,
       ROUND(AVG(rating), 3) AS average_rating,
       ROUND(100.0 * AVG(delivery), 1) AS online_delivery_pct,
       ROUND(100.0 * AVG(booking), 1) AS table_booking_pct
FROM restaurants GROUP BY country, market ORDER BY restaurants DESC;

SELECT city, COUNT(*) AS restaurants, ROUND(AVG(rating), 3) AS average_rating,
       SUM(votes) AS total_votes
FROM restaurants WHERE country = 1 GROUP BY city ORDER BY restaurants DESC LIMIT 10;

SELECT c.cuisine, COUNT(DISTINCT r.id) AS restaurants,
       ROUND(AVG(r.rating), 3) AS average_rating
FROM restaurants r JOIN restaurant_cuisines c ON r.id = c.restaurant_id
WHERE r.country = 1 GROUP BY c.cuisine ORDER BY restaurants DESC LIMIT 10;

-- Median price for India only. Never aggregate nominal costs across markets.
WITH ordered AS (
  SELECT cost, ROW_NUMBER() OVER (ORDER BY cost) AS rn, COUNT(*) OVER () AS n
  FROM restaurants WHERE country = 1 AND cost IS NOT NULL
)
SELECT AVG(cost) AS india_median_cost_for_two
FROM ordered WHERE rn IN ((n+1)/2, (n+2)/2);
