# E-commerce Funnel Analysis

**Where does an online shop lose its shoppers?** A funnel and conversion analysis of three months of real GA4 data from the Google Merchandise Store, written in SQL on BigQuery.

![Funnel](images/01_funnel.png)

## The data

Google's public [GA4 e-commerce sample](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset) (`bigquery-public-data.ga4_obfuscated_sample_ecommerce`): every page view, add-to-cart and purchase on the Google Merchandise Store from **1 November 2020 to 31 January 2021**, stored as one table per day. Google has anonymised ("obfuscated") parts of it, which affects some results (see *Limitations*).

## Questions

1. Of everyone who visits, how many view a product, add it to the cart, check out and buy? Where is the biggest drop?
2. Does that change by device or by how visitors arrived (search, ads, referral, direct)?
3. What happened over the holiday season?

## Key findings

**1. Most shoppers are lost before the cart, not at checkout.** 77% of visitors never view a product, and 80% of product viewers never add anything to their cart. Once someone adds to cart, 77% start checkout. Overall, **1.65% of visitors bought something**.

**2. One leak inside checkout.** 41% of people who start checkout leave before entering payment details. That step is where shipping costs and delivery details usually appear, which makes it the first candidate for an A/B test.

**3. Device makes no clear difference.** Mobile converted at 1.71% and desktop at 1.62%. A two-proportion z-test gives p = 0.056, just above the usual 0.05 threshold, so the honest conclusion is "no clear difference" ([`significance_check.py`](significance_check.py)).

**4. Paid-ad visitors buy about half as often as referred visitors** (0.98% vs 1.89%). The dataset has no ad spend, so this can't say whether the ads pay for themselves; joining ad-platform cost data would be the next step.

![Purchase rate by source](images/02_purchase_rate_by_source.png)

**5. The peak was early December, not Black Friday.** The week of 7 December had the most visitors, buyers and revenue, most likely the last safe week to order before Christmas. After 21 December sales collapse, and early January is busy (24,000+ visitors a week) but only 0.66% buy.

![Weekly trend](images/03_weekly_trend.png)

## Data quality check

In the last week of January, revenue per buyer fell from about $75 to $18. A day-by-day check ([`05_revenue_tracking_check.sql`](sql/05_revenue_tracking_check.sql)) showed that purchases kept happening at the normal rate, but from **26 January** more and more were recorded with **$0 revenue**, reaching 100% on 31 January. This is a tracking problem, not a change in shopper behaviour, so revenue from 26 January onwards is excluded from conclusions. Buyer counts and purchase rates are unaffected.

## Limitations

- **Funnel steps are counted independently.** Each step counts everyone who did it at any point in the three months, not people moving through the steps in strict order.
- **Anonymised traffic sources.** About a fifth of visitors are labelled `<Other>` or `(data deleted)`, and visitors per source add up to more than the total, so some visitors appear under more than one source. These rows are reported but not interpreted.
- **Observational, not experimental.** Differences between devices or sources show association, not cause. Testing a fix (for example, showing shipping costs earlier) would need an A/B test.

## Repository

| Folder / file | What's in it |
|---|---|
| [`sql/`](sql/) | The five BigQuery queries, numbered in the order they were run |
| [`results/`](results/) | Each query's output as CSV |
| [`images/`](images/) | Charts |
| [`make_charts.py`](make_charts.py) | Builds the charts from `results/` |
| [`significance_check.py`](significance_check.py) | Mobile vs desktop significance test |

## Reproduce it

1. Open the free [BigQuery sandbox](https://console.cloud.google.com/bigquery) and create a project.
2. Run the queries in `sql/` in order. The dataset is public, so nothing needs to be uploaded.
3. Rebuild the charts: `pip install pandas matplotlib`, then `python make_charts.py`.

**Tools:** SQL (BigQuery), Python (pandas, matplotlib), GA4 event data.
