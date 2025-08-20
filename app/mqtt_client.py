from __future__ import annotations
import paho.mqtt.client as mqtt
from config.settings import SETTINGS

class AppMQTTClient:
    def __init__(self, client_id: str | None = None):
        self.client = mqtt.Client(client_id=client_id or SETTINGS.client_id_app, clean_session=True)
        if SETTINGS.username and SETTINGS.password:
            self.client.username_pw_set(SETTINGS.username, SETTINGS.password)

    def publish_command(self, payload: str):
        self.client.connect(SETTINGS.broker_host, SETTINGS.broker_port, keepalive=60)
        self.client.loop_start()
        self.client.publish(SETTINGS.topic_command, payload=payload, qos=SETTINGS.qos, retain=False)
        self.client.loop_stop()
        self.client.disconnect()
