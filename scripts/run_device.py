from __future__ import annotations
from feeder.mqtt_client import FeederMQTTClient
from feeder.device import DeviceState
from feeder.handlers import handle_message

def main():
    device = DeviceState()
    feeder = FeederMQTTClient()  # rename variable to avoid confusion

    def on_message(_mqtt_client, userdata, msg):
        payload = msg.payload.decode("utf-8", errors="ignore")
        print(f"[Device] Received on {msg.topic}: {payload}")
        # use the outer FeederMQTTClient instance
        handle_message(payload, device, publish_event=feeder.publish_event)

    feeder.client.on_message = on_message
    print("[Device] Starting device subscriber...")
    feeder.loop_forever()

if __name__ == "__main__":
    main()
