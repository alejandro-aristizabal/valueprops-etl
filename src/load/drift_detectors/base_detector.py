"""Base class for drift detectors."""

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


@dataclass
class BaseDriftDetector(Protocol):
    """Base class for drift detectors."""

    historical_data: pd.DataFrame
    recent_data: pd.DataFrame

    def detect_drift(self, column_name: str) -> tuple[bool, float]:
        """Detect drift in the specified column."""
