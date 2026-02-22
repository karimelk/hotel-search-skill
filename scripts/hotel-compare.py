#!/usr/bin/env python3
"""
Compare prices for one exact hotel across booking sources using SerpApi property details.

Examples:
  python3 scripts/hotel-compare.py \
    --hotel "Galaxy Iraklio Hotel" --check-in 2026-09-18 --check-out 2026-09-27 \
    --adults 1 --currency EUR
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
class SourcePrice:
    source: str
    price: float | None
    currency: str
    link: str | None


def http_get_json(url: str) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": "openclaw-hotel-compare/1.0"})
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


def find_property_token(api_key: str, hotel: str, check_in: str, check_out: str, adults: int, children: int, children_ages: str, currency: str, gl: str, hl: str) -> str | None:
    params = {
        "engine": "google_hotels",
        "q": hotel,
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
    data = http_get_json(f"{SERP_BASE}?{urlencode(params)}")
    props = data.get("properties", [])
    if props:
        return props[0].get("property_token")
    # property-details responses may expose token at top level
    return data.get("property_token")


def compare_sources(api_key: str, hotel: str, check_in: str, check_out: str, adults: int, children: int, children_ages: str, currency: str, gl: str, hl: str) -> List[SourcePrice]:
    token = find_property_token(api_key, hotel, check_in, check_out, adults, children, children_ages, currency, gl, hl)
    if not token:
        return []

    params = {
        "engine": "google_hotels",
        "q": hotel,
        "property_token": token,
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
    data = http_get_json(f"{SERP_BASE}?{urlencode(params)}")

    out: List[SourcePrice] = []
    for src in data.get("prices", []) or []:
        total = src.get("total_rate", {}) if isinstance(src.get("total_rate"), dict) else {}
        rate = src.get("rate_per_night", {}) if isinstance(src.get("rate_per_night"), dict) else {}
        price = parse_price(
            src.get("price")
            or total.get("lowest")
            or total.get("before_taxes_fees")
            or rate.get("lowest")
            or rate.get("before_taxes_fees")
        )
        out.append(
            SourcePrice(
                source=src.get("source", "(unknown)"),
                price=price,
                currency=currency,
                link=src.get("link"),
            )
        )

    out.sort(key=lambda x: (x.price is None, x.price if x.price is not None else 1e15))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare one hotel across booking sources (SerpApi)")
    ap.add_argument("--hotel", required=True)
    ap.add_argument("--check-in", required=True)
    ap.add_argument("--check-out", required=True)
    ap.add_argument("--adults", type=int, default=1)
    ap.add_argument("--children", type=int, default=0)
    ap.add_argument("--children-ages", default="", help="Comma-separated ages, e.g. 2 or 2,6")
    ap.add_argument("--currency", default="EUR")
    ap.add_argument("--gl", default="de")
    ap.add_argument("--hl", default="en")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    key = get_key()
    acct = account_status(key)
    left = acct.get("total_searches_left")
    hourly = acct.get("account_rate_limit_per_hour")
    if isinstance(left, int) and left <= 2:
        raise RuntimeError(f"Need >=2 searches left for compare. Current: {left}")

    rows = compare_sources(
        key,
        args.hotel,
        args.check_in,
        args.check_out,
        args.adults,
        args.children,
        args.children_ages,
        args.currency,
        args.gl,
        args.hl,
    )
    print(f"SerpApi quota: left={left} hourly_limit={hourly}")

    if not rows:
        print("No comparable sources found.")
        return 1

    for i, r in enumerate(rows, start=1):
        price = f"{args.currency} {r.price:.2f}" if r.price is not None else "n/a"
        print(f"{i:>2}. {price} | {r.source}")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump([asdict(r) for r in rows], f, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
