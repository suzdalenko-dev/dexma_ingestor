from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str
    poll_interval_seconds: int
    target_url: str
    output_dir: str
    request_timeout_seconds: int


def load_settings() -> Settings:
    return Settings(
        app_name                = os.getenv("APP_NAME", "api-poller"),
        poll_interval_seconds   = int(os.getenv("POLL_INTERVAL_SECONDS", "60")),
        target_url              = os.getenv("TARGET_URL", "https://informes.froxa.net/symfony/suzdalenko/"),
        output_dir              = os.getenv("OUTPUT_DIR", "./data"),
        request_timeout_seconds = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
    )