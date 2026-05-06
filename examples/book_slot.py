"""Propose a berth call and print what the planner decided.

    python examples/book_slot.py --vessel "MV Example" --loa 118 --draught 6.1 \
        --eta 2026-10-12T06:00Z --hours 14
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse

from tidewell_client import Client


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vessel", required=True)
    ap.add_argument("--loa", type=float, required=True, help="length overall in metres")
    ap.add_argument("--draught", type=float, required=True)
    ap.add_argument("--eta", required=True, help="ISO 8601, UTC")
    ap.add_argument("--hours", type=float, required=True, help="expected time alongside")
    ap.add_argument("--dry-run", action="store_true", help="ask the planner without holding the slot")
    a = ap.parse_args()

    body = {
        "vessel": {"name": a.vessel, "loa_m": a.loa, "draught_m": a.draught},
        "eta": a.eta,
        "duration_h": a.hours,
        "hold": not a.dry_run,
    }
    plan = Client().post("/calls", body)
    print(f"Berth {plan['berth']}  alongside {plan['alongside']}  departs {plan['departs']}")
    for note in plan.get("notes", []):
        print("  -", note)


if __name__ == "__main__":
    main()
