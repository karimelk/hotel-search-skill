# 🏨 Hotel Search Skill
### SerpAPI-first • VPS-friendly • built from real-world trial and error

> A practical hotel-search workflow for AI agents.
> 
> This repo is meant to help people **skip setup pain** and get straight to a working process.

---

## ✨ At a glance

- **What it does:** Finds hotel options, compares shortlisted hotels across booking sources, and returns clear recommendations.
- **Who it’s for:** People using an AI assistant/agent (especially on a VPS).
- **Why this exists:** Browser-based scraping and “click around” flows are often fragile on VPS. This script-first approach is more stable.

---

## ✅ Easiest way to use it (no terminal needed)

If you’re using an assistant like me, you normally just ask in plain English:

- “Find me hotel options in Mallorca for these dates.”
- “Compare this hotel across booking sources.”
- “Give me best overall + best value.”

That’s it. The assistant runs the underlying scripts for you.

---

## 🔑 You need a SerpAPI key (one-time setup)

This skill uses `SERPAPI_API_KEY`.

### Good news
SerpAPI usually has free/trial usage that works well for testing and lighter personal usage.

- Pricing/limits: <https://serpapi.com/pricing>
- Sign up: <https://serpapi.com/users/sign_up>

> Pricing can change, so always check the current plan details on SerpAPI.

---

## 🖥️ Why this works well on VPS

Browser-heavy workflows on VPS can be painful:
- dynamic pages fail to load
- captchas/session issues break automation
- results become inconsistent

This skill is **script-first** (API-driven), so it is typically more reliable for unattended agent workflows.

---

## 🧠 What process this follows

1. Search destination + dates (`hotel-search.py`)
2. Pick finalists (usually top 3–5)
3. Compare each finalist across sources (`hotel-compare.py`)
4. Return shortlist with tradeoffs and links

This is the same process that was refined through real use.

---

## 📦 Repo contents

- `SKILL.md` → agent instructions
- `scripts/hotel-search.py` → broad hotel search
- `scripts/hotel-compare.py` → source-by-source compare for one hotel
- `scripts/accom.py` → convenience wrapper
- `references/commands.md` → command cookbook
- `references/response-template.md` → response format

---

## ⚡ Manual mode (optional, for power users)

If you are not running this via an assistant, you can run it directly.

<details>
<summary><strong>Step 1 — Save API key</strong></summary>

Put this in one of:
- `/home/clawdbot/.openclaw/.env` (preferred)
- `~/.openclaw/.env`

```bash
SERPAPI_API_KEY=your_real_key_here
```
</details>

<details>
<summary><strong>Step 2 — Run search</strong></summary>

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
</details>

<details>
<summary><strong>Step 3 — Compare one hotel across sources</strong></summary>

```bash
python3 scripts/hotel-compare.py \
  --hotel "Hotel Saratoga" \
  --check-in 2026-09-18 --check-out 2026-09-27 \
  --adults 1 --currency EUR \
  --json-out /tmp/hotel-compare-saratoga.json
```
</details>

---

## 💡 Simple troubleshooting

- **“SERPAPI_API_KEY is not set”**
  - Key missing or `.env` not loaded.
- **“Not enough SerpApi quota left”**
  - Free/trial limit reached. Wait for reset or reduce compare calls.
- **No results found**
  - Try broader location terms, flexible dates, or fewer constraints.

---

## 🚫 Intentionally not included

- Airbnb support
- Browser-clicking as primary workflow

These were excluded to keep the flow stable on VPS.

---

If you’re non-technical: **use assistant mode** and just ask in normal language.
