---
name: hotel-search
description: Search, compare, and shortlist hotels or other short-stay accommodations using user-specified criteria (destination, dates, budget, area, amenities, policies, and trip intent). Use when a user asks for hotel search, recommendations, shortlists, stay comparisons, or “find me a place to stay” planning.
---

# Hotel Search

Find decision-ready hotel shortlists with verified details, clear tradeoffs, and direct booking links.

## Output Standard

- Return 3-6 recommendations by default unless the user asks for a different count.
- Show source-backed facts and a UTC freshness timestamp.
- Avoid claiming real-time availability unless a source explicitly shows availability for the requested dates.

## Core Workflow

1. Capture the user criteria and confirm assumptions.
2. Search broadly, then narrow quickly.
3. Verify each shortlisted option.
4. Rank options by fit and explain tradeoffs.
5. Present a concise shortlist and next-step options.

## 1) Capture Criteria

Collect the minimum required inputs first:
- Destination (city/area)
- Dates (exact check-in/check-out or date window)
- Occupancy (adults, children, child ages when relevant)
- Number of rooms
- Budget target (per night or total)

Collect high-impact preferences when relevant:
- Must-have amenities (Wi-Fi, breakfast, parking, gym, pool, workspace, kitchen)
- Area preferences (walkability, central, near station/event)
- Trip intent (business, family, romantic, nightlife, quiet)
- Policy needs (free cancellation, pay at property, refundable)
- Quality floor (star level, review score threshold)
- Special constraints (accessibility, pet-friendly, late check-in)

If essential inputs are missing, ask concise follow-up questions before heavy searching.
Batch follow-ups in one message (max 4 targeted questions).
If the user declines to provide details, proceed with reasonable assumptions and label them explicitly.

## 2) Search Broadly, Then Narrow

Use `web_search` to discover candidates and `web_fetch` to extract comparable details.
If pages are JS-heavy or blocked, use `browser` as a fallback.

Start with 8-12 candidates, then narrow to 3-6 finalists.

Use query patterns from `references/search-playbook.md`.

Prefer multiple source types for each finalist:
- Official property site (preferred)
- Major OTA listing (Booking/Expedia/Hotels/etc.)
- Review or map context when useful

Avoid listicle-only evidence for final recommendations.

## 3) Verify Finalists

For each shortlisted property, verify core facts from at least two independent sources when possible:
- Price point and currency
- Tax/fee context (pre-tax base vs fee-inclusive total, if visible)
- Cancellation/refund terms
- Breakfast/fees/taxes notes (if visible)
- Review score and source (plus review count when visible)
- Distance/area fit relative to user priority

Record source URLs and a UTC freshness timestamp.

If only one source is available, explicitly label the item as **partially verified**.
If live pricing is unstable or date windows are broad, label prices as **indicative**.
If sources conflict, state the conflict and use the more conservative interpretation.
Never invent missing policy or fee details.

## 4) Rank by Fit

Apply hard constraints first (must-haves, budget ceiling, location constraints).

Then rank finalists with this default weighting:
- Must-have fit: 35%
- Price-to-value: 25%
- Location fit: 20%
- Review quality: 15%
- Policy flexibility: 5%

Adjust weights if the user states a clear priority (for example, “location matters most”).
If two options tie, prefer stronger policy flexibility and higher verification confidence.

## 5) Present Recommendations

Use the structure in `references/response-template.md`.

Always include:
- Best overall pick
- Best value pick
- A context-specific pick (best location, best for work, best for families, etc.)

For each option, include:
- Name and neighborhood/area
- Price snapshot (currency + tax/fee context + pricing caveat)
- Why it matches the criteria
- 1-2 tradeoffs
- Policy highlight
- Verification status and source count
- Booking links

When posting on Discord, avoid markdown tables; use short bullet lists.
Wrap links in `<...>` to suppress noisy embeds when sharing multiple links.

## Edge Cases

If no strong matches exist:
- Explain which constraints are causing low match quality.
- Offer 2-3 relaxation options (date shift, radius expansion, amenity tradeoff, budget increase).
- Re-run with the user’s preferred relaxation strategy.

If dates are missing:
- Offer a preliminary “best candidates by typical value” list.
- Ask for dates before presenting “best price” or availability claims.

If the user asks for only one recommendation:
- Still evaluate at least 3 candidates internally.
- Return one pick plus one backup option.
