# 🏨 Hotel Search Skill (SerpAPI-First)

A practical, **real-world-tested** hotel search workflow for AI agents.

This is not a generic demo skill. It reflects a setup that was hardened through trial and error so others can skip the pain and get a working solution fast.

---

## What this skill does

It helps an agent:

1. Search hotels for your destination and dates
2. Find solid options by price + quality
3. Compare the same hotel across booking sources
4. Return a clean shortlist with tradeoffs and links

So instead of random web browsing, you get a repeatable process.

---

## Why this is great for VPS agents

On VPS/cloud servers, browser-heavy workflows can be annoying:
- pages block automation
- dynamic content loads inconsistently
- sessions/cookies/captchas break flows

This skill is **script-first** and uses SerpAPI data directly, which is usually more stable for unattended agent workflows on VPS.

---

## Important: you need a SerpAPI key

This skill expects `SERPAPI_API_KEY`.

### Good news
SerpAPI typically offers free/trial usage that is enough for testing and light personal use.

> Pricing and limits can change, so always check current details here:  
> <https://serpapi.com/pricing>

Create account here:  
<https://serpapi.com/users/sign_up>

---

## 5-minute setup (non-technical version)

### Step 1) Create SerpAPI account
- Sign up
- Copy your API key from your SerpAPI dashboard

### Step 2) Save key in an `.env` file
Put this line in one of these files:
- `/home/clawdbot/.openclaw/.env` (preferred for this workflow)
- or `~/.openclaw/.env`

Line to add:

```bash
SERPAPI_API_KEY=your_real_key_here
```

### Step 3) Run the search
From the repo folder:

```bash
cd ~/publish/hotel-search-skill

set -a
source /home/clawdbot/.openclaw/.env 2>/dev/null || true
source ~/.openclaw/.env 2>/dev/null || true
set +a

python3 scripts/hotel-search.py \
  --query "Mallorca" \
  --check-in 2026-09-18 --check-out 2026-09-27 \
  --adults 1 --currency EUR --limit 10 \
  --json-out /tmp/hotel-search.json
```

That gives you initial hotel candidates.

### Step 4) Compare one hotel across booking sources

```bash
python3 scripts/hotel-compare.py \
  --hotel "Hotel Saratoga" \
  --check-in 2026-09-18 --check-out 2026-09-27 \
  --adults 1 --currency EUR \
  --json-out /tmp/hotel-compare-saratoga.json
```

---

## Quick mode (simpler commands)

If you don’t care about JSON files and just want terminal output:

```bash
python3 scripts/accom.py search --query "Mallorca" --check-in 2026-09-18 --check-out 2026-09-27 --adults 1 --currency EUR --limit 10
python3 scripts/accom.py compare --hotel "Hotel Saratoga" --check-in 2026-09-18 --check-out 2026-09-27 --adults 1 --currency EUR
```

---

## How the workflow thinks

- `hotel-search.py` = broad search (destination/date)
- `hotel-compare.py` = verify finalists across providers
- `accom.py` = wrapper command for convenience

Recommended pattern:
1. Search first
2. Pick top 3–5
3. Compare those finalists
4. Recommend with confidence notes

---

## Quota behavior (built in)

The scripts check SerpAPI quota before spending requests:
- Search stops early if quota is very low
- Compare stops early if quota is too low for a safe compare run

This protects free-tier users from burning credits accidentally.

---

## Troubleshooting (simple)

### “SERPAPI_API_KEY is not set”
Your key is missing or `.env` was not loaded. Re-check Step 2 + Step 3.

### “Not enough SerpApi quota left”
You hit free-tier limits. Wait for reset or reduce compare calls.

### “No results found”
Try broader query terms (city only first), flexible dates, or fewer constraints.

---

## What this skill intentionally does NOT include

- Airbnb integration
- Browser-clicking as primary path

Those were intentionally excluded to keep VPS automation stable.

---

## Repo contents

- `SKILL.md` — instructions for the agent
- `scripts/` — the executable SerpAPI workflow
- `references/commands.md` — copy/paste command cookbook
- `references/response-template.md` — output format
- `references/search-playbook.md` — fallback guidance

---

If you are non-technical: start with the **5-minute setup** above and copy/paste exactly.  
You do not need to understand everything to get value from it.
