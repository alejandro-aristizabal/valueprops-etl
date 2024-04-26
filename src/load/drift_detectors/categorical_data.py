"""Methods to detect drift in categorical data distributions."""

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


@dataclass
class ChiSquaredTest:
    """This class implements the chi-squared test for drift detection, the
    chi-squared test is a statistical test that compares the observed
    distribution of categorical data to an expected distribution to determine
    if they are different.

    Args:
    - historical_data: pd.DataFrame, the historical dataset
    - recent_data: pd.DataFrame, the recent dataset
    - alpha: float, significance level for deciding drift (default is 0.05)
    """

    historical_data: pd.DataFrame
    recent_data: pd.DataFrame
    alpha: float = 0.05

    def detect_drift(self, column_name: str) -> Tuple[bool, float]:
        """
        Perform the chi-squared test on the specified column for two data samples.

        Args:
        - column_name: str, the name of the column to perform the chi-squared test on.

        Returns:
        - boolean indicating if drift is detected (True if drift, False otherwise)
        - p-value from the chi-squared test
        """
        # Create a contingency table from the column data
        contingency_table = pd.crosstab(
            self.historical_data[column_name], self.recent_data[column_name]
        )

        # Perform the chi-squared test on the contingency table
        _, p_value, _, _ = chi2_contingency(contingency_table)

        # Decide if there is drift based on the p-value
        drift_detected = p_value < self.alpha

        return drift_detected, p_value


@dataclass
class CramersVTest:
    """This class implements the Cramer's V test for drift detection, the
    Cramer's V test is a statistical test that measures the strength of association
    between two categorical variables.

    Args:
    - historical_data: pd.DataFrame, the historical dataset
    - recent_data: pd.DataFrame, the recent dataset
    - alpha: float, significance level for deciding drift (default is 0.05)
    """

    historical_data: pd.DataFrame
    recent_data: pd.DataFrame
    alpha: float = 0.05

    def detect_drift(self, column_name: str) -> Tuple[bool, float]:
        """
        Perform the Cramer's V test on the specified column for two data samples.

        Args:
        - column_name: str, the name of the column to perform the Cramer's V test on.

        Returns:
        - boolean indicating if drift is detected (True if drift, False otherwise)
        - p-value from the Cramer's V test
        """
        # Create a contingency table from the column data
        contingency_table = pd.crosstab(
            self.historical_data[column_name], self.recent_data[column_name]
        )

        # Perform the chi-squared test on the contingency table
        chi2, p_value, _, _ = chi2_contingency(contingency_table)

        # Calculate the Cramer's V statistic
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape)
        cramer_v = np.sqrt(chi2 / (n * (min_dim - 1)))

        # Decide if there is drift based on the p-value
        drift_detected = p_value < self.alpha

        return drift_detected, cramer_v
