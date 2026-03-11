import logging
import sys

"""
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

"""

import logging
from pathlib import Path


def setup_logging() -> None:
    log_dir = Path("log")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "api-poller.log", encoding="utf-8"),
            logging.StreamHandler()
        ],
    )