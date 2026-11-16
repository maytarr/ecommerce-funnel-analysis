-- Overall funnel: how many distinct visitors reached each step of the buying journey
-- Data: Google Merchandise Store GA4 sample, 1 Nov 2020 - 31 Jan 2021
SELECT
  event_name,
  COUNT(DISTINCT user_pseudo_id) AS users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name IN ('session_start', 'view_item', 'add_to_cart',
                     'begin_checkout', 'add_payment_info', 'purchase')
GROUP BY event_name
ORDER BY users DESC;
