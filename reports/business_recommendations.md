# RFM Segmentation — Tactical Business Recommendations

Based on `data/processed/rfm_segments.csv` (4,334 customers, 10 RFM segments).
Numbers below are pulled directly from the segmentation output — swap in your
own cost/conversion assumptions where marked *(assumption)*.

| Segment | Customers | % of Base | Avg. Recency (days) | Avg. Frequency | Avg. Monetary | Total Revenue | % of Revenue |
|---|---|---|---|---|---|---|---|
| Champions | 633 | 14.6% | 5.9 | 12.3 | £6,769.2 | £4,284,919 | 49.0% |
| Loyal Customers | 817 | 18.9% | 33.0 | 6.4 | £2,781.3 | £2,272,362 | 26.0% |
| At Risk | 591 | 13.6% | 152.5 | 2.9 | £1,072.5 | £633,821 | 7.3% |
| Hibernating | 1,078 | 24.9% | 217.0 | 1.1 | £478.5 | £515,845 | 5.9% |
| Can't Lose Them | 65 | 1.5% | 132.8 | 8.3 | £2,717.1 | £176,612 | 2.0% |

---

## 1. Protect at-risk revenue: reactivate "At Risk" and "Can't Lose Them"

**Business problem.** These two segments (656 customers, 15.1% of the base)
were historically valuable — "Can't Lose Them" still averages **£2,717/customer**,
close to a Loyal Customer — but haven't purchased in **132–153 days on
average**. Without intervention, they are on a trajectory toward Hibernating.

**Recommended action.** A time-boxed win-back campaign (personal email/call
for "Can't Lose Them" given their high historical value; automated
discount-triggered email for the larger "At Risk" group) before Recency
crosses the point of no return.

**Expected impact.** *(Assumption: winning back 20% of "At Risk" customers to
Loyal-level spend.)* 0.20 × 591 × (£2,781 − £1,073) ≈ **£202,000** in
recovered annual revenue — from one segment alone.

**KPI to track:** reactivation rate (% who purchase within 60 days of
campaign), Recency trend for the targeted cohort, revenue recovered vs.
campaign cost.

---

## 2. Grow revenue from the base that already drives it: upsell Champions & Loyal Customers

**Business problem.** Just **33.5% of customers (Champions + Loyal) generate
75.0% of total revenue.** This is the segment with the least acquisition
risk and the highest leverage per marketing dollar — yet is often
under-invested because "they'll buy anyway."

**Recommended action.** VIP tier / early access to new stock, volume-based
loyalty rewards, and a referral incentive (Champions have the highest
purchase frequency at 12.3 — they're also the most credible referrers).

**Expected impact.** *(Assumption: a 10% frequency-driven monetary lift on
Loyal Customers, 5% on Champions since they're already near-saturated.)*
0.10 × £2,272,362 + 0.05 × £4,284,919 ≈ **£441,000** in incremental revenue.

**KPI to track:** repeat purchase rate, average order value, referral
conversion rate, migration rate from Loyal → Champions.

---

## 3. Stop overspending on a segment that won't return it: cap Hibernating outreach cost

**Business problem.** "Hibernating" is the **largest segment by customer
count (24.9%)** but contributes only **5.9% of revenue** (£478.5/customer
average, no purchase in ~217 days). Broad, high-cost campaigns (catalogs,
outbound calls) aimed at this group have a structurally weak ROI ceiling.

**Recommended action.** Move this segment to low-cost automated channels
only (single re-engagement email + small voucher), cap acquisition cost per
customer well below their historical average value, and reallocate the
freed budget to Recommendation #1 (At Risk / Can't Lose Them) where the
revenue-per-dollar-spent is materially higher.

**Expected impact.** Not a revenue-growth play — a **cost-avoidance /
budget-reallocation** argument: redirecting spend from a segment worth
£478/customer to one worth £1,073–2,717/customer improves overall campaign
ROI without increasing total marketing spend.

**KPI to track:** cost per contact, reactivation rate vs. cost, and %
marketing budget reallocated to higher-value segments.

---

## How to use this template for other datasets

1. Pull the segment summary table (`rfm.groupby("Segment").agg(...)` from
   `02_rfm_segmentation.py`).
2. Pick 2-3 segments that map to a C-level priority: **Protect** (high value,
   slipping away), **Grow** (high value, already engaged), **Optimize/Cut**
   (low value, high cost-to-serve).
3. Quantify the "why now" with the segment's own Recency/Frequency/Monetary
   averages — avoid generic advice ("send them an email") without a number
   attached to the opportunity size.
