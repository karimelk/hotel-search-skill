# Response Template (SerpApi Process)

Use this format for user-facing output.

## Quick Summary
- **Best overall:** <hotel>
- **Best value:** <hotel>
- **Best for <priority>:** <hotel>

## Recommended Options

### 1) <Hotel Name> — <Area>
- **Search price snapshot:** <amount + currency + caveat>
- **Best compared source:** <provider + amount> (or `not compared: quota/other reason`)
- **Why it fits:** <2-3 bullets>
- **Tradeoffs:** <1-2 bullets>
- **Policy note:** <cancellation/refund if visible>
- **Links:** <best source>, <alternate source>

### 2) <Hotel Name> — <Area>
- **Search price snapshot:** <amount + currency + caveat>
- **Best compared source:** <provider + amount> (or `not compared: quota/other reason`)
- **Why it fits:** <2-3 bullets>
- **Tradeoffs:** <1-2 bullets>
- **Policy note:** <cancellation/refund if visible>
- **Links:** <best source>, <alternate source>

### 3) <Hotel Name> — <Area>
- **Search price snapshot:** <amount + currency + caveat>
- **Best compared source:** <provider + amount> (or `not compared: quota/other reason`)
- **Why it fits:** <2-3 bullets>
- **Tradeoffs:** <1-2 bullets>
- **Policy note:** <cancellation/refund if visible>
- **Links:** <best source>, <alternate source>

## Notes
- **Process used:** SerpApi `google_hotels` via `hotel-search.py` + `hotel-compare.py`
- **Quota state at run time:** <left/hourly>
- **Verification:** <which hotels were compare-verified vs search-only>
- **Data freshness:** <UTC timestamp>
- **Assumptions:** <budget/occupancy/area defaults if any>

## If No Good Matches
- State the blocking constraints.
- Offer 2-3 concrete relaxations (dates, radius, budget, policy).
- Ask which relaxation to apply for the next run.
