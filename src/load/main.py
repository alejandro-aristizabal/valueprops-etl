"""Drift monitoring main module."""

import os
from typing import Any

import numpy as np
import pandas as pd
import toml
from loguru import logger


from utils.logging.logger import setup_logging
from load.drift_detectors import get_drift_detector


setup_logging("config.toml", os.path.dirname(__file__))

current_dir = os.path.dirname(__file__)
with open(os.path.join(current_dir, "config.toml"), "r", encoding="utf-8") as f:
    config = toml.load(f)


def drift_monitoring() -> None:
    """Drift monitoring."""
    logger.info("Started drift monitoring")

    drift_status: dict[str, Any] = {}
    tables = []
    columns = []
    status_list = []
    stat_list = []
    for table in config["drift_detection"]["tables"]:
        drift_status[table["current_table"]] = {}
        logger.info(f"Started drift detection for {table['current_table']}")

        initial_table = pd.read_csv(table["current_table"])

        # Split the table into historical and current data at 80%

        historical_data = initial_table.sample(frac=0.8)
        current_data = initial_table.drop(historical_data.index)

        for column in table["columns"]:
            tables.append(table["current_table"])
            drift_detector = get_drift_detector(
                column["method"], historical_data, current_data
            )
            logger.info(f"Started drift detection for {column['name']}")
            drift_detected, stat = drift_detector.detect_drift(column["name"])
            if np.isnan(stat) | np.isinf(stat):
                stat = 0
            drift_status[table["current_table"]].update(
                {column["name"]: (drift_detected, stat)}
            )

            columns.append(column["name"])
            status_list.append(drift_detected)
            stat_list.append(stat)

    logger.info(f"Drift status: {drift_status}")


if __name__ == "__main__":
    drift_monitoring()
