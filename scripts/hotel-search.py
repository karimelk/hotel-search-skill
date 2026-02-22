#!/usr/bin/env python3
"""
Search hotels via SerpApi Google Hotels with quota-aware behavior for free plans.

Examples:
  python3 scripts/hotel-search.py \
    --query "Heraklion" --check-in 2026-09-18 --check-out 2026-09-27 \
    --adults 1 --currency EUR --limit 10
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from typing import Any, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SERP_BASE = "https://serpapi.com/search.json"
ACCOUNT_URL = "https://serpapi.com/account.json"


@dataclass
class HotelResult:
    name: str
    source: str | None
    total_rate: float | None
    currency: str
    rating: float | None
    reviews: int | None
    check_in: str
    check_out: str
    link: str | None


def http_get_json(url: str) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": "openclaw-hotel-search/1.0"})
    with urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_key() -> str:
    key = os.getenv("SERPAPI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("SERPAPI_API_KEY is not set")
    return key


def account_status(api_key: str) -> dict[str, Any]:
    url = f"{ACCOUNT_URL}?{urlencode({'api_key': api_key})}"
    return http_get_json(url)


def parse_price(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = "".join(ch for ch in v if (ch.isdigit() or ch == "."))
        return float(s) if s else None
    return None


def search_hotels(
    api_key: str,
    query: str,
    check_in: str,
    check_out: str,
    adults: int,
    children: int,
    children_ages: str,
    currency: str,
    gl: str,
    hl: str,
    limit: int,
) -> List[HotelResult]:
    params = {
        "engine": "google_hotels",
        "q": query,
        "check_in_date": check_in,
        "check_out_date": check_out,
        "adults": adults,
        "children": children,
        "currency": currency,
        "gl": gl,
        "hl": hl,
        "api_key": api_key,
    }
    if children > 0 and children_ages:
        params["children_ages"] = children_ages
    url = f"{SERP_BASE}?{urlencode(params)}"
    data = http_get_json(url)

    props = data.get("properties", [])
    if not props and data.get("name") and data.get("total_rate"):
        # Google sometimes returns property-details shape directly
        props = [data]

    out: List[HotelResult] = []
    for p in props[:limit * 3]:
        rate = p.get("rate_per_night", {})
        total = p.get("total_rate", {})
        total_price = parse_price(total.get("lowest") or total.get("before_taxes_fees") or rate.get("lowest"))
        source_name = None
        source_link = None
        if p.get("sources"):
            source_name = (p.get("sources", [{}])[0] or {}).get("name")
            source_link = (p.get("sources", [{}])[0] or {}).get("link")
        elif p.get("prices"):
            source_name = (p.get("prices", [{}])[0] or {}).get("source")
            source_link = (p.get("prices", [{}])[0] or {}).get("link")
        out.append(
            HotelResult(
                name=p.get("name", "(unknown)"),
                source=source_name,
                total_rate=total_price,
                currency=currency,
                rating=p.get("overall_rating"),
                reviews=p.get("reviews"),
                check_in=check_in,
                check_out=check_out,
                link=source_link,
            )
        )

    out.sort(key=lambda x: (x.total_rate is None, x.total_rate if x.total_rate is not None else 1e15))
    return out[:limit]


def main() -> int:
    ap = argparse.ArgumentParser(description="SerpApi Google Hotels search (quota-aware)")
    ap.add_argument("--query", required=True)
    ap.add_argument("--check-in", required=True)
    ap.add_argument("--check-out", required=True)
    ap.add_argument("--adults", type=int, default=1)
    ap.add_argument("--children", type=int, default=0)
    ap.add_argument("--children-ages", default="", help="Comma-separated ages, e.g. 2 or 2,6")
    ap.add_argument("--currency", default="EUR")
    ap.add_argument("--gl", default="de")
    ap.add_argument("--hl", default="en")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--json-out")
    args = ap.parse_args()

    key = get_key()
    acct = account_status(key)
    left = acct.get("total_searches_left")
    hourly = acct.get("account_rate_limit_per_hour")
    if isinstance(left, int) and left <= 1:
        raise RuntimeError(f"Not enough SerpApi quota left: {left}")

    results = search_hotels(
        api_key=key,
        query=args.query,
        check_in=args.check_in,
        check_out=args.check_out,
        adults=args.adults,
        children=args.children,
        children_ages=args.children_ages,
        currency=args.currency,
        gl=args.gl,
        hl=args.hl,
        limit=max(1, min(args.limit, 20)),
    )

    print(f"SerpApi quota: left={left} hourly_limit={hourly}")
    if not results:
        print("No results found.")
        return 1

    for i, r in enumerate(results, start=1):
        price = f"{args.currency} {r.total_rate:.2f}" if r.total_rate is not None else "n/a"
        print(f"{i:>2}. {price} | {r.name} | source={r.source or '-'} | rating={r.rating or '-'}")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump([asdict(r) for r in results], f, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
