---
name: hotel-search
description: Run the script-first SerpApi Google Hotels workflow used in this workspace. Use when a user asks for hotel options, accommodation shortlists, or booking-source price comparison. Execute bundled scripts (`scripts/hotel-search.py`, `scripts/hotel-compare.py`, or `scripts/accom.py`) with `SERPAPI_API_KEY`, quota-aware checks, and finalist comparison before recommending.
---

# Hotel Search (SerpApi Script-First)

Use the exact process that was hardened through real usage: search with SerpApi first, compare finalists across sources second, then present a concise shortlist.

## Non-Negotiables

- Use bundled scripts first; do not default to generic `web_search`/`web_fetch`.
- Load `SERPAPI_API_KEY` before every run.
- Respect quota checks built into scripts.
- Run source comparison on finalists before final recommendations whenever quota allows.
- If key/quota blocks execution, tell the user and ask before switching to a non-SerpApi fallback.

## Inputs to Collect

- Destination/query string
- Check-in/check-out dates
- Adults
- Children count and ages (required when children > 0)
- Currency (default `EUR`)

Optional: `gl`, `hl`, result limit, area/intent constraints.

## Command Workflow

Follow the command templates in `references/commands.md`.

Default flow:
1. Load env and verify key.
2. Run `scripts/hotel-search.py` with `--json-out` for machine-readable results.
3. Pick 3-5 finalists with usable prices.
4. Run `scripts/hotel-compare.py` for each finalist.
5. Build recommendation output using `references/response-template.md`.

Use `scripts/accom.py` only for quick terminal runs when JSON artifacts are not needed.

## Ranking Rules

- Apply hard constraints first (budget ceiling, dates, occupancy, must-have policy/amenity).
- Prefer lower total price when quality is similar.
- Break ties with stronger rating/review depth and better cancellation flexibility.
- Mark missing prices/policies explicitly; do not infer.

## Quota + Failure Handling

- `hotel-search.py` fails early when quota is too low (`<=1` searches left).
- `hotel-compare.py` fails early when quota is too low (`<=2` searches left).
- If quota is insufficient, return the exact quota message and ask whether to continue later or run a manual fallback.
- If SerpApi returns no properties, broaden query (city only, then district), relax constraints, and retry once.

## Output Requirements

- Provide 3-6 options by default unless user requests another count.
- Include: price snapshot, source, rating/review context, key tradeoff, and booking links.
- Include verification note: which options were comparison-verified vs search-only.
- Include data freshness timestamp in UTC.

When posting on Discord, use bullets (no markdown tables) and wrap multiple links in `<...>`.
