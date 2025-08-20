# IoT Cat Feeder Simulator (MQTT)

A minimal end-to-end simulation of an IoT cat feeder using MQTT **pub/sub** in Python.

## Overview

```
[App (Publisher)] → MQTT Broker → [Device (Subscriber)]
```

- The **app** sends commands like `FEED 50` or `STATUS?` to a command topic.
- The **device** listens, executes logic, appends logs to `data/logs.csv`, and publishes results to an event topic.

## Quick Start

1) Create and activate a virtual environment, then install deps:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) Copy `.env.example` to `.env` and tweak if needed:
```bash
cp .env.example .env
```

3) Run the simulated device (subscriber):
```bash
python3 -m scripts.run_device
```

4) In another terminal, send commands with the app (publisher):
```bash
# Feed 50 grams
python3 -m scripts.run_app feed 50

# Ask for status
python3 -m scripts.run_app status
```

5) (Optional) Plot daily totals:
```bash
python3 -c "from dashboard.charts import plot_daily_totals; plot_daily_totals('data/logs.csv')"
```

## Notes

- Default broker is the public `broker.hivemq.com` (no auth). You can switch to a local Mosquitto or a managed broker by editing `.env`.
- Logs are appended to `data/logs.csv`. You can switch to SQLite by setting `USE_SQLITE=true` in `.env`.
