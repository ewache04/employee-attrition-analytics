import logging
import sys
from pathlib import Path
from datetime import datetime


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    log_dir = Path(__file__).parents[2] / "logs"
    log_dir.mkdir(exist_ok=True)
    fh = logging.FileHandler(
        log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger
