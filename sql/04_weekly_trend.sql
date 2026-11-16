-- Weekly visitors, buyers and revenue across the holiday season
SELECT
  DATE_TRUNC(PARSE_DATE('%Y%m%d', event_date), WEEK(MONDAY)) AS week_start,
  COUNT(DISTINCT IF(event_name = 'session_start', user_pseudo_id, NULL)) AS visitors,
  COUNT(DISTINCT IF(event_name = 'purchase',      user_pseudo_id, NULL)) AS buyers,
  ROUND(SUM(IF(event_name = 'purchase', ecommerce.purchase_revenue_in_usd, 0))) AS revenue_usd
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY week_start
ORDER BY week_start;
