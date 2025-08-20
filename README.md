# IoT Cat Feeder Simulator (MQTT)

A minimal end-to-end simulation of an IoT cat feeder using MQTT **pub/sub** in Python.

## Overview

```
[App (Publisher)] → MQTT Broker → [Device (Subscriber)]
```

- The **app** sends commands like `FEED 50` or `STATUS?` to a command topic.
- The **device** listens, executes logic, appends logs to `data/logs.csv`, and publishes results to an event topic.

## Quick Start

## 1) Repository Structure

```
iot-cat-feeder/
├─ api/
│  ├─ __init__.py          # marks package (optional if you run with --app-dir)
│  └─ server.py            # FastAPI: POST /feed → publish to MQTT; GET /status ← latest device event
├─ app/                    # CLI publisher (Python)
├─ config/                 # settings loader from .env (with sane defaults)
├─ dashboard/              # optional charts from logs
├─ feeder/                 # simulated device (MQTT subscriber)
├─ scripts/                # entrypoints you run
│  ├─ run_device.py        # device subscriber
│  └─ run_app.py           # command-line publisher
├─ data/                   # logs storage (CSV / optional SQLite)
├─ tests/                  # minimal tests
├─ .env.example            # template config
├─ requirements.txt
└─ README.md
```

---

## 2) Quick Start

### Create a virtual env & install deps
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment
Copy the template and edit as needed:
```bash
# show hidden files if you don't see it: ls -a
cp .env.example .env
```

### Run the simulated device (subscriber)
> Use **module mode** so package imports work from project root.
```bash
python3 -m scripts.run_device
```

### Send commands from the CLI (publisher)
```bash
python3 -m scripts.run_app feed 50
python3 -m scripts.run_app status
```

### View logs / charts
- CSV logs: `data/logs.csv`
- Optional chart:
```bash
python3 -c "from dashboard.charts import plot_daily_totals; plot_daily_totals('data/logs.csv')"
```

---

## 3) Optional: HTTP → MQTT Bridge (FastAPI)

Expose an HTTP API that publishes to the MQTT command topic and reads back the latest device event.

### Run the API
From the **project root** (so `config.settings` resolves):
```bash
uvicorn api.server:app --reload --port 8000
```

### Try it
With the device subscriber running:
```bash
curl -X POST "http://127.0.0.1:8000/feed"   -H "Content-Type: application/json"   -d '{"qty":5}'

curl "http://127.0.0.1:8000/status"
```

---

## 4) Environment Variables (.env)

```
MQTT_BROKER_HOST=broker.hivemq.com
MQTT_BROKER_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=

MQTT_TOPIC_COMMAND=iot/catfeeder/command
MQTT_TOPIC_EVENT=iot/catfeeder/event

LOG_CSV_PATH=data/logs.csv
USE_SQLITE=false
SQLITE_PATH=data/feeder.db

CLIENT_ID_DEVICE=feeder-sim-001
CLIENT_ID_APP=feeder-app-001
QOS=1
```

Notes:
- For production, prefer **TLS (8883)** and authenticated users on a managed broker.
- Topics are shared by the CLI app and the device; keep them consistent.

---

## 5) Roadmap Ideas

- Switch to JSON payloads (e.g., `{ "cmd": "feed", "qty": 5 }`).
- Add SQLite storage and `/events` endpoint (pagination) to the API.
- MQTT over **WebSockets** if your network requires it.
- AuthN/Z for the API; per-device ACLs on the broker.
- Live dashboard (Streamlit or FastAPI+HTMX) to visualize logs.

## 6) References (official docs)

- FastAPI — https://fastapi.tiangolo.com/
- Uvicorn — https://www.uvicorn.org/
- Eclipse Paho MQTT (Python) — https://www.eclipse.org/paho/index.php?page=clients/python/index.php
- MQTT Essentials — https://www.hivemq.com/tags/mqtt-essentials/
