"""Print the next tide windows for a vessel.

A tide window is a stretch of time when there is enough water over the sill
or at the berth for a given draught plus under-keel clearance.

    python examples/tide_windows.py --draught 6.4 --hours 48
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from datetime import datetime

from tidewell_client import Client


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draught", type=float, required=True, help="vessel draught in metres")
    ap.add_argument("--ukc", type=float, default=0.5, help="under-keel clearance in metres")
    ap.add_argument("--hours", type=int, default=24)
    a = ap.parse_args()

    c = Client()
    res = c.get("/tide-windows", draught_m=a.draught, ukc_m=a.ukc, hours=a.hours)
    if not res["windows"]:
        print("No window in the next %d h for %.1f m + %.1f m UKC." % (a.hours, a.draught, a.ukc))
        return
    for w in res["windows"]:
        start = datetime.fromisoformat(w["opens"])
        end = datetime.fromisoformat(w["closes"])
        mins = int((end - start).total_seconds() // 60)
        print(f"{start:%a %d %b %H:%M} -> {end:%H:%M}  ({mins} min, peak {w['peak_height_m']:.2f} m)")


if __name__ == "__main__":
    main()
