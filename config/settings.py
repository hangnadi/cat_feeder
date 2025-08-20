import os
from dataclasses import dataclass
from dotenv import load_dotenv

def _to_bool(v: str) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}

load_dotenv()

@dataclass(frozen=True)
class Settings:
    broker_host: str = os.getenv("MQTT_BROKER_HOST", "broker.hivemq.com")
    broker_port: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    username: str | None = os.getenv("MQTT_USERNAME") or None
    password: str | None = os.getenv("MQTT_PASSWORD") or None

    topic_command: str = os.getenv("MQTT_TOPIC_COMMAND", "iot/catfeeder/command")
    topic_event: str = os.getenv("MQTT_TOPIC_EVENT", "iot/catfeeder/event")

    log_csv_path: str = os.getenv("LOG_CSV_PATH", "data/logs.csv")
    use_sqlite: bool = _to_bool(os.getenv("USE_SQLITE", "false"))
    sqlite_path: str = os.getenv("SQLITE_PATH", "data/feeder.db")

    client_id_device: str = os.getenv("CLIENT_ID_DEVICE", "feeder-sim-001")
    client_id_app: str = os.getenv("CLIENT_ID_APP", "feeder-app-001")
    qos: int = int(os.getenv("QOS", "1"))

SETTINGS = Settings()
