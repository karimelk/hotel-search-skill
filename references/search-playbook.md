# Hotel Search Playbook

Use these patterns to quickly discover and verify hotel candidates.

## Query Patterns

Replace placeholders:
- `<city>`
- `<dates>` (optional in query text)
- `<area>`
- `<intent>` (business/family/quiet/etc.)
- `<amenity>`
- `<budget>`
- `<landmark>`

### Broad Discovery
- `best hotels in <city> <dates>`
- `<city> hotel deals <dates>`
- `<city> accommodation near <area>`
- `aparthotel in <city> <area>`

### Intent-Focused
- `best business hotel <city> near <area>`
- `family friendly hotel <city> pool breakfast`
- `quiet boutique hotel <city> <area>`

### Constraint-Focused
- `<city> hotel free cancellation`
- `<city> hotel with <amenity>`
- `<city> hotels under <budget> per night`
- `accessible hotel <city> <area>`
- `pet friendly hotel <city> <area>`

### Verification Queries
- `<hotel name> official site`
- `<hotel name> cancellation policy`
- `<hotel name> resort fee OR city tax`
- `<hotel name> reviews`
- `<hotel name> distance to <landmark>`

## Source Strategy

For each finalist, aim for:
1. Official property page (rate/policy/room details)
2. One major OTA listing (pricing/comparability)
3. Optional map/review context when the user cares about neighborhood quality

Avoid relying only on generic listicles or SEO roundups for final claims.

## Quality Filters

Drop candidates that fail any hard constraints:
- Wrong area with no clear transport upside
- Missing required amenity
- Strong policy mismatch (if policy is a must-have)
- Price clearly out of budget unless explicitly marked as stretch

Also deprioritize candidates when:
- Source data is stale or undated
- Policy/fee details are unavailable across all sources

## Price Notes

Always clarify whether shown numbers are:
- Pre-tax base rates
- Tax/fee-inclusive totals
- Date-specific quotes or indicative snapshots

If comparing properties with mixed currencies, normalize to the user’s preferred currency and note the conversion date/context.
