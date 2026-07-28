#!/usr/bin/env python3
"""
Friday helper: roll Beanie Day week meta forward.

Usage:
  python3 scripts/new-week.py
  python3 scripts/new-week.py --start 2026-08-01

Does not invent activities — only updates meta dates so you can paste fresh curation into activities[].
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "week.json"


def next_friday(from_day: date) -> date:
    # Friday = 4
    delta = (4 - from_day.weekday()) % 7
    if delta == 0 and from_day == date.today():
        return from_day
    return from_day + timedelta(days=delta or 7)


def format_label(start: date, end: date) -> str:
    if start.month == end.month:
        return f"{start.day} {start.strftime('%b')} – {end.day} {end.strftime('%b %Y')}"
    return f"{start.day} {start.strftime('%b')} – {end.day} {end.strftime('%b %Y')}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Roll Beanie Day week meta forward")
    parser.add_argument(
        "--start",
        help="Week start date (Friday) YYYY-MM-DD. Default: next Friday from today.",
    )
    args = parser.parse_args()

    if args.start:
        start = datetime.strptime(args.start, "%Y-%m-%d").date()
    else:
        start = next_friday(date.today())

    end = start + timedelta(days=6)
    next_refresh = start + timedelta(days=7)

    with DATA.open(encoding="utf-8") as f:
        data = json.load(f)

    meta = data.setdefault("meta", {})
    meta["weekLabel"] = format_label(start, end)
    meta["weekStart"] = start.isoformat()
    meta["weekEnd"] = end.isoformat()
    meta["refreshedOn"] = start.isoformat()
    meta["nextRefresh"] = next_refresh.isoformat()

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Updated {DATA}")
    print(f"  Week: {meta['weekLabel']}")
    print(f"  Refresh: {meta['refreshedOn']} → next {meta['nextRefresh']}")
    print("  Next: curate activities[] for quality & relevance, then redeploy.")


if __name__ == "__main__":
    main()
