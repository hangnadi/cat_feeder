from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import paho.mqtt.client as mqtt
from config.settings import SETTINGS
import json
from typing import Optional

app = FastAPI(title="Cat Feeder API")

mqtt_client = mqtt.Client(client_id="api-bridge")
if SETTINGS.username and SETTINGS.password:
    mqtt_client.username_pw_set(SETTINGS.username, SETTINGS.password)
mqtt_client.connect(SETTINGS.broker_host, SETTINGS.broker_port, keepalive=60)
mqtt_client.loop_start()

latest_event: Optional[dict] = None

def _on_connect(client, userdata, flags, rc):
    client.subscribe(SETTINGS.topic_event, qos=SETTINGS.qos)

def _on_message(client, userdata, msg):
    global latest_event
    try:
        latest_event = json.loads(msg.payload.decode("utf-8", errors="ignore"))
    except Exception:
        latest_event = {"type": "error", "message": "unable to parse event"}

mqtt_client.on_connect = _on_connect
mqtt_client.on_message = _on_message

class FeedRequest(BaseModel):
    qty: Annotated[int, Field(gt=0, le=5)]

@app.post("/feed")
def feed(req: FeedRequest):
    result = mqtt_client.publish(SETTINGS.topic_command, f"FEED {req.qty}", qos=SETTINGS.qos)
    if result.rc != 0:
        raise HTTPException(status_code=502, detail="Failed to publish to MQTT")
    return {"status": "ok", "queued": True}

@app.get("/status")
def status():
    return latest_event or {"status": "no_events_yet"}
