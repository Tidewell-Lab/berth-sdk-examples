# Tidewell Berth API: examples

Small, runnable examples for the Tidewell Berth API. Each one does one job and
fits on a screen, so you can read it before you run it.

| Example | What it does |
|---|---|
| `examples/list_berths.py` | Lists the berths at your port with their depth and length. |
| `examples/tide_windows.py` | Prints the next tide windows for a vessel draught. |
| `examples/book_slot.py` | Proposes a berth call and prints what the planner decided. |
| `examples/webhook_receiver.py` | A minimal receiver for plan-changed webhooks, with signature check. |

## Setup

```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export TIDEWELL_API_BASE=<the sandbox URL from your onboarding email>
export TIDEWELL_API_KEY=<your sandbox key>
python examples/list_berths.py
```

Sandbox keys start with `tw_test_`. Never commit a key: `.env` is ignored for a reason.

## Support

Questions about the examples or the API: open an issue here, or use the contact
form on our website. Planners, not just developers, are welcome to ask.

## Licence

MIT. See `LICENSE`.
