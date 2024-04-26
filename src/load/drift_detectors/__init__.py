"""This module contains the drift detectors for categorical and numerical data.

The drift detectors are used to detect drift between two datasets."""

import pandas as pd
from load.drift_detectors.base_detector import BaseDriftDetector
from load.drift_detectors.categorical_data import (
    ChiSquaredTest,
    CramersVTest,
)
from load.drift_detectors.numerical_data import (
    CUSUM,
    KLDivergence,
    KSTest,
    PSICalculator,
    ZTest,
)


def get_drift_detector(
    detector_name: str, historical_data: pd.DataFrame, recent_data: pd.DataFrame
) -> BaseDriftDetector:
    """Get the drift detector handler based on the name.

    Args:
    - detector_name: str, the name of the drift detector.
    - historical_data: pd.DataFrame, the historical dataset.
    - recent_data: pd.DataFrame, the recent dataset.

    Returns:
    - object: the drift detector handler.
    """
    detectors = {
        "z_test": ZTest,
        "psi_calculator": PSICalculator,
        "chi_squared_test": ChiSquaredTest,
        "cramers_v_test": CramersVTest,
        "ks_test": KSTest,
        "cusum": CUSUM,
        "kl_divergence": KLDivergence,
    }

    detector_class = detectors.get(detector_name)
    if not detector_class:
        raise ValueError(f"Handler does not exist: {detector_name}")
    return detector_class(historical_data, recent_data)
