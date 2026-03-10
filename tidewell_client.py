"""A very small client for the Tidewell Berth API, shared by the examples."""
import os
import sys

import requests

TIMEOUT = 15


class Client:
    def __init__(self, base=None, key=None):
        self.base = (base or os.environ.get("TIDEWELL_API_BASE", "")).rstrip("/")
        self.key = key or os.environ.get("TIDEWELL_API_KEY", "")
        if not self.base or not self.key:
            sys.exit("Set TIDEWELL_API_BASE and TIDEWELL_API_KEY first (see README).")
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": "Bearer " + self.key,
            "Accept": "application/json",
            "User-Agent": "tidewell-examples/0.4",
        })

    def get(self, path, **params):
        r = self.s.get(self.base + path, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    def post(self, path, body):
        r = self.s.post(self.base + path, json=body, timeout=TIMEOUT)
        if r.status_code == 422:
            # The planner explains why it rejected a call; show that instead of a stack trace.
            sys.exit("Rejected: " + r.json().get("detail", r.text))
        r.raise_for_status()
        return r.json()
