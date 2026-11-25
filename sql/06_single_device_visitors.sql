-- Robustness check for the mobile vs desktop test.
-- The z-test assumes the two groups are independent, but a visitor who used both
-- a phone and a computer is counted in both. Here each visitor appears once:
-- single-device visitors under their device, everyone else under 'multiple'.
WITH per_visitor AS (
  SELECT
    user_pseudo_id,
    COUNT(DISTINCT device.category)       AS n_devices,
    ANY_VALUE(device.category)            AS device,
    MAX(IF(event_name = 'session_start', 1, 0)) AS visited,
    MAX(IF(event_name = 'purchase', 1, 0))      AS bought
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  GROUP BY user_pseudo_id
)
SELECT
  IF(n_devices = 1, device, 'multiple') AS device_group,
  COUNT(*)    AS visitors,
  SUM(bought) AS buyers
FROM per_visitor
WHERE visited = 1
GROUP BY device_group
ORDER BY visitors DESC;
