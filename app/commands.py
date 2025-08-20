from __future__ import annotations
from config.settings import SETTINGS
from app.mqtt_client import AppMQTTClient

def feed(grams: int):
    payload = f"FEED {grams}"
    AppMQTTClient().publish_command(payload)

def status():
    payload = "STATUS?"
    AppMQTTClient().publish_command(payload)
