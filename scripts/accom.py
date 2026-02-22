#!/usr/bin/env python3
"""Accommodation wrapper router.

Routes subcommands to the underlying scripts so the assistant can use one entrypoint.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SEARCH = os.path.join(ROOT, "hotel-search.py")
COMPARE = os.path.join(ROOT, "hotel-compare.py")


def run(cmd: list[str]) -> int:
    env = os.environ.copy()
    return subprocess.call(cmd, env=env)


def main() -> int:
    ap = argparse.ArgumentParser(description="Accommodation router")
    sub = ap.add_subparsers(dest="mode", required=True)

    s = sub.add_parser("search", help="Destination/date hotel search")
    s.add_argument("--query", required=True)
    s.add_argument("--check-in", required=True)
    s.add_argument("--check-out", required=True)
    s.add_argument("--adults", type=int, default=1)
    s.add_argument("--children", type=int, default=0)
    s.add_argument("--children-ages", default="")
    s.add_argument("--currency", default="EUR")
    s.add_argument("--gl", default="de")
    s.add_argument("--hl", default="en")
    s.add_argument("--limit", type=int, default=10)

    c = sub.add_parser("compare", help="Exact hotel source price compare")
    c.add_argument("--hotel", required=True)
    c.add_argument("--check-in", required=True)
    c.add_argument("--check-out", required=True)
    c.add_argument("--adults", type=int, default=1)
    c.add_argument("--children", type=int, default=0)
    c.add_argument("--children-ages", default="")
    c.add_argument("--currency", default="EUR")
    c.add_argument("--gl", default="de")
    c.add_argument("--hl", default="en")

    args = ap.parse_args()

    if args.mode == "search":
        cmd = [
            sys.executable,
            SEARCH,
            "--query", args.query,
            "--check-in", args.check_in,
            "--check-out", args.check_out,
            "--adults", str(args.adults),
            "--children", str(args.children),
            "--children-ages", args.children_ages,
            "--currency", args.currency,
            "--gl", args.gl,
            "--hl", args.hl,
            "--limit", str(args.limit),
        ]
        return run(cmd)

    cmd = [
        sys.executable,
        COMPARE,
        "--hotel", args.hotel,
        "--check-in", args.check_in,
        "--check-out", args.check_out,
        "--adults", str(args.adults),
        "--children", str(args.children),
        "--children-ages", args.children_ages,
        "--currency", args.currency,
        "--gl", args.gl,
        "--hl", args.hl,
    ]
    return run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
