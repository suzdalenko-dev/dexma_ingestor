import logging
import time
import json
from pathlib import Path
from datetime import datetime, timezone
import requests
from config import load_settings
from logger_setup import setup_logging


logger = logging.getLogger("api-poller")

def utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def save_response(output_dir: str, response_text: str, content_type: str | None) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = utc_now_compact()

    # Si parece JSON, guardamos como .json, si no como .txt
    if content_type and "application/json" in content_type.lower():
        filename = f"response_{timestamp}.json"
    else:
        filename = f"response_{timestamp}.txt"

    file_path = out_dir / filename
    file_path.write_text(response_text, encoding="utf-8")
    return file_path


def run_once(url: str, output_dir: str, timeout_seconds: int) -> None:
    logger.info("Haciendo GET a %s", url)

    response = requests.get(url, timeout=timeout_seconds)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    text = response.text

    # Si es JSON válido, lo reescribimos bonito
    if "application/json" in content_type.lower():
        try:
            parsed = response.json()
            text = json.dumps(parsed, indent=2, ensure_ascii=False)
        except Exception:
            pass

    saved_file = save_response(output_dir, text, content_type)
    logger.info("Respuesta guardada en %s", saved_file)


def main() -> None:
    setup_logging()
    settings = load_settings()

    logger.info("Arrancando servicio %s", settings.app_name)

    while True:
        try:
            run_once(
                url=settings.target_url,
                output_dir=settings.output_dir,
                timeout_seconds=settings.request_timeout_seconds,
            )
        except Exception as e:
            logger.exception("Error en ciclo principal: %s", e)
            time.sleep(10)

        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    main()