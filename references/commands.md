# SerpApi Command Playbook

Copy/paste templates for the exact process.

## 1) Load env + verify key

```bash
set -a
source /home/clawdbot/.openclaw/.env 2>/dev/null || true
source ~/.openclaw/.env 2>/dev/null || true
set +a

test -n "${SERPAPI_API_KEY:-}" || { echo "SERPAPI_API_KEY missing"; exit 1; }
```

## 2) Destination search (machine-readable)

```bash
python3 scripts/hotel-search.py \
  --query "<destination>" \
  --check-in <YYYY-MM-DD> --check-out <YYYY-MM-DD> \
  --adults <N> --children <N> --children-ages "<ages csv>" \
  --currency EUR --gl de --hl en --limit 12 \
  --json-out /tmp/hotel-search.json
```

Notes:
- If `children=0`, pass `--children 0` and omit `--children-ages`.
- For family trips, provide exact ages (`--children-ages "2,6"`).

## 3) Compare finalists across booking sources

Run once per finalist hotel name:

```bash
python3 scripts/hotel-compare.py \
  --hotel "<hotel name>" \
  --check-in <YYYY-MM-DD> --check-out <YYYY-MM-DD> \
  --adults <N> --children <N> --children-ages "<ages csv>" \
  --currency EUR --gl de --hl en \
  --json-out /tmp/hotel-compare-<slug>.json
```

## 4) Quick terminal-only mode (no JSON files)

```bash
python3 scripts/accom.py search \
  --query "<destination>" \
  --check-in <YYYY-MM-DD> --check-out <YYYY-MM-DD> \
  --adults <N> --currency EUR --limit 10

python3 scripts/accom.py compare \
  --hotel "<hotel name>" \
  --check-in <YYYY-MM-DD> --check-out <YYYY-MM-DD> \
  --adults <N> --currency EUR
```

## 5) Quota errors (expected behaviors)

- Search fails when `total_searches_left <= 1`
- Compare fails when `total_searches_left <= 2`

When this happens, stop and ask whether to wait for quota reset or run manual fallback.
