"""Minimal receiver for Tidewell plan-changed webhooks.

Tidewell signs each delivery with HMAC-SHA256 over the raw body, using your
webhook secret, and sends it as the X-Tidewell-Signature header (hex).

    TIDEWELL_WEBHOOK_SECRET=... python examples/webhook_receiver.py
"""
import hashlib
import hmac
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET = os.environ.get("TIDEWELL_WEBHOOK_SECRET", "").encode()
PORT = int(os.environ.get("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        sent = self.headers.get("X-Tidewell-Signature", "")
        want = hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        if not SECRET or sent != want:
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
