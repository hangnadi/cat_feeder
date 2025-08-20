from __future__ import annotations
import time
import paho.mqtt.client as mqtt
from config.settings import SETTINGS

class FeederMQTTClient:
    def __init__(self, client_id: str | None = None):
        self.client = mqtt.Client(client_id=client_id or SETTINGS.client_id_device, clean_session=True)
        if SETTINGS.username and SETTINGS.password:
            self.client.username_pw_set(SETTINGS.username, SETTINGS.password)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = None  # set by caller
        self._connected = False

    def _on_connect(self, client, userdata, flags, rc):
        self._connected = True
        print(f"[Device MQTT] Connected with result code {rc}")
        # Subscribe to command topic
        client.subscribe(SETTINGS.topic_command, qos=SETTINGS.qos)

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        print(f"[Device MQTT] Disconnected (rc={rc})")

    def loop_forever(self):
        self.client.connect(SETTINGS.broker_host, SETTINGS.broker_port, keepalive=60)
        self.client.loop_forever(retry_first_connection=True)

    def publish_event(self, payload: str):
        if not self._connected:
            # best-effort connect
            try:
                self.client.reconnect()
            except Exception:
                pass
        self.client.publish(SETTINGS.topic_event, payload=payload, qos=SETTINGS.qos, retain=False)
