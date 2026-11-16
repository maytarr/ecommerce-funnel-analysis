-- Funnel by traffic source (how the visitor first arrived: organic search, paid ads, referral, direct)
SELECT
  traffic_source.medium AS medium,
  COUNT(DISTINCT IF(event_name = 'session_start',    user_pseudo_id, NULL)) AS visited,
  COUNT(DISTINCT IF(event_name = 'view_item',        user_pseudo_id, NULL)) AS viewed_item,
  COUNT(DISTINCT IF(event_name = 'add_to_cart',      user_pseudo_id, NULL)) AS added_to_cart,
  COUNT(DISTINCT IF(event_name = 'begin_checkout',   user_pseudo_id, NULL)) AS began_checkout,
  COUNT(DISTINCT IF(event_name = 'add_payment_info', user_pseudo_id, NULL)) AS added_payment,
  COUNT(DISTINCT IF(event_name = 'purchase',         user_pseudo_id, NULL)) AS purchased
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY medium
ORDER BY visited DESC;
