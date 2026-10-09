"""Minimal receiver for Tidewell plan-changed webhooks.

Tidewell signs each delivery with HMAC-SHA256 over "<timestamp>.<raw body>",
using your webhook secret, and sends the hex digest as X-Tidewell-Signature
and the Unix timestamp as X-Tidewell-Timestamp. Deliveries older than
TIDEWELL_MAX_SKEW seconds (default 300) are rejected, so a captured delivery
can't be replayed later.

    TIDEWELL_WEBHOOK_SECRET=... python examples/webhook_receiver.py
"""
import hashlib
import hmac
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET = os.environ.get("TIDEWELL_WEBHOOK_SECRET", "").encode()
PORT = int(os.environ.get("PORT", "8080"))
MAX_SKEW = int(os.environ.get("TIDEWELL_MAX_SKEW", "300"))


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        sent = self.headers.get("X-Tidewell-Signature", "")
        ts = self.headers.get("X-Tidewell-Timestamp", "")
        if not ts.isdigit() or abs(int(time.time()) - int(ts)) > MAX_SKEW:
            self.send_response(401)
            self.end_headers()
            return
        want = hmac.new(SECRET, ts.encode() + b"." + body, hashlib.sha256).hexdigest()
        if not SECRET or not hmac.compare_digest(sent, want):
            self.send_response(401)
            self.end_headers()
            return
        event = json.loads(body)
        print(f"{event['type']}: call {event['call_id']} -> berth {event.get('berth', '?')}")
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"listening on :{PORT}")
    HTTPServer(("", PORT), Handler).serve_forever()
