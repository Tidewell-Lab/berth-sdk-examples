"""List the berths at your port."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tidewell_client import Client


def main():
    c = Client()
    berths = c.get("/berths")["items"]
    print(f"{'Berth':<10} {'Length m':>9} {'Depth m':>8}  Notes")
    for b in berths:
        print(f"{b['code']:<10} {b['length_m']:>9.0f} {b['depth_cd_m']:>8.1f}  {b.get('notes', '')}")


if __name__ == "__main__":
    main()
