-- Data quality check: are late-January purchases missing their revenue?
SELECT
  event_date,
  COUNTIF(event_name = 'purchase') AS purchases,
  COUNTIF(event_name = 'purchase' AND ecommerce.purchase_revenue_in_usd IS NULL) AS missing_revenue,
  COUNTIF(event_name = 'purchase' AND ecommerce.purchase_revenue_in_usd = 0) AS zero_revenue,
  ROUND(SUM(IF(event_name = 'purchase', ecommerce.purchase_revenue_in_usd, 0))) AS revenue_usd
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20210118' AND '20210131'
GROUP BY event_date
ORDER BY event_date;
