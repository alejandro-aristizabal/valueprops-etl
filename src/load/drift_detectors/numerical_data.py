"""Methods to detect drift in numeric data distributions."""

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy.stats import entropy, ks_2samp, norm


@dataclass
class KSTest:
    """This class implement the Kolmogorov-Smirnov test for drift detection, the
    KS test is a non-parametric test that compares the cumulative distribution
    function (CDF) of two samples to determine if they are drawn from the same.

    Args:
    - historical_data: pd.DataFrame, the historical dataset
    - recent_data: pd.DataFrame, the recent dataset
    - alpha: float, significance level for deciding drift (default is 0.05)
    """

    historical_data: pd.DataFrame
    recent_data: pd.DataFrame
    alpha: float = 0.05

    def detect_drift(self, column_name: str) -> tuple[bool, float]:
        """
        Perform the KS test on the specified column for two data samples.

        Args:
        - column_name: str, the name of the column to perform the KS test on.

        Returns:
        - boolean indicating if drift is detected (True if drift, False otherwise)
        - p-value from the KS test
        """
        # Extract the column data from each sample
        column_data1 = self.historical_data[column_name]
        column_data2 = self.recent_data[column_name]

        # Perform the KS test on the column data
        _, p_value = ks_2samp(column_data1, column_data2)

        # Decide if there is drift based on the p-value
        drift_detected = p_value < self.alpha

        return drift_detected, p_value


@dataclass
class PSICalculator:
    """This class implements the Population Stability Index (PSI) for drift detection.
    The PSI is a measure of the change in the population distribution of a variable between
    a historical dataset and a recent dataset. It is calculated by comparing the distribution
    of a variable in the historical and recent datasets.

    Args:
    - historical_data: pd.DataFrame, the historical dataset
    - recent_data: pd.DataFrame, the recent dataset
    - bins: int, the number of bins to use for discretizing continuous variables.
    - epsilon: float, a small value to add to bin counts to avoid division by zero.
    - threshold: float, the threshold for deciding drift (default is 0.1)
    """

    historical_data: pd.DataFrame
    recent_data: pd.DataFrame
    bins: int = 10
    epsilon: float = 1e-5
    threshold: float = 0.1

    def detect_drift(self, column_name: str) -> tuple[bool, float]:
        """
        Calculate the PSI for the specified column.

        Args:
            - column_name: str, the name of the column to calculate the PSI for.

        Returns:
            - float, the PSI value for the column.
        """
        # Discretize the data into bins
        hist_counts, bin_edges = np.histogram(
            self.historical_data[column_name], bins=self.bins
        )
        recent_counts, _ = np.histogram(self.recent_data[column_name], bins=bin_edges)

        # Add epsilon to avoid division by zero
        hist_counts = hist_counts + self.epsilon
        recent_counts = recent_counts + self.epsilon

        # Normalize the counts to get probabilities
        hist_probs = hist_counts / sum(hist_counts)
        recent_probs = recent_counts / sum(recent_counts)

        # Calculate PSI
        psi_values = (recent_probs - hist_probs) * np.log(recent_probs / hist_probs)
        psi = sum(psi_values)

        drift_detected = psi > self.threshold

        return drift_detected, psi


@dataclass
class ZTest:
    """This class implements the Z test for drift detection, the Z test is a statistical
    test used to determine if there is a significant difference between the means of two
    samples. It is used to compare the means of two samples to determine if they are drawn
    from the same distribution.

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
        Calculate the Z test for comparing two sample means.

        Parameters:
        - sample1: List[float], data points for the first sample
        - sample2: List[float], data points for the second sample
        - confidence: float, confidence level for deciding drift (default is 0.95)

        Returns:
        - Tuple[bool, float, float] indicating if drift is detected, the Z score, and the p-value
        """
        mean1 = self.historical_data[column_name].mean()
        mean2 = self.recent_data[column_name].mean()
        std1 = self.historical_data[column_name].std()
        std2 = self.recent_data[column_name].std()

        n1 = len(self.historical_data)
        n2 = len(self.recent_data)

        # Calculate the pooled standard deviation and Z score
        pooled_std = np.sqrt(std1**2 / n1 + std2**2 / n2)
        z_score = (mean1 - mean2) / pooled_std

        # Determine the critical Z score from the confidence level
        z_critical = norm.ppf(1 - self.alpha / 2)

        # Calculate p-value from Z score
        p_value = 2 * (1 - norm.cdf(abs(z_score)))

        # Decide if there is drift based on the Z score exceeding the critical value
        drift_detected = abs(z_score) > z_critical

        return drift_detected, p_value


@dataclass
class CUSUM:
    """This class implements the Cumulative Sum (CUSUM) algorithm for drift detection.
    The CUSUM algorithm is a statistical method used to detect shifts in the mean value
    of a variable. It calculates the cumulative sum of deviations from a target mean and
    detects a shift when the sum exceeds a threshold.

    Args:
    - historical_data: pd.DataFrame, the historical dataset
    - recent_data: pd.DataFrame, the recent dataset
    - threshold: float, the threshold for detecting a shift
    """

    historical_data: pd.DataFrame
    recent_data: pd.DataFrame
    threshold: float = 0.1

    def detect_drift(self, column_name: str) -> Tuple[bool, List[int]]:
        """
        Detect drift using the CUSUM method.

        Parameters:
        - data: List[float], the data series to monitor for drift.

        Returns:
        - Tuple[bool, List[int]] indicating if drift is detected and the indices where drift occurs.
        """
        s_pos, s_neg = 0, 0
        drift_indices = []
        target_mean = self.historical_data[column_name].mean()
        data = self.recent_data[column_name].concat(self.historical_data[column_name])

        for i, x in enumerate(data):
            deviation = x - target_mean
            s_pos = max(0, s_pos + deviation)
            s_neg = min(0, s_neg + deviation)

            if (s_pos > self.threshold) or (s_neg < -self.threshold):
                drift_indices.append(i)
                # Reset the cumulative sum to avoid detecting the same shift multiple times
                s_pos, s_neg = 0, 0

        drift_detected = len(drift_indices) > 0
        return drift_detected, drift_indices


@dataclass
class KLDivergence:
    """This class implements the Kullback-Leibler Divergence (KLD) for drift detection.
    The KLD is a measure of the difference between two probability distributions. It is
    used to detect changes in the distribution of a variable between a historical dataset
    and a recent dataset.

    Args:
        - historical_data: pd.DataFrame, the historical dataset
        - recent_data: pd.DataFrame, the recent dataset
        - num_bins: int, the number of bins to use for discretizing continuous variables.
        - threshold: float, the threshold for deciding drift (default is 0.1)
    """

    historical_data: pd.DataFrame
    recent_data: pd.DataFrame
    num_bins: int = 10
    threshold: float = 0.1

    def detect_drift(self, column_name: str) -> Tuple[bool, float]:
        """
        Calculate the KLD for the specified column.

        Args:
            - column_name: str, the name of the column to calculate the KLD for.

        Returns:
            - float, the KLD value for the column.
        """
        # Discretize the data into bins
        hist_counts, bin_edges = np.histogram(
            self.historical_data[column_name], bins=self.num_bins
        )
        recent_counts, _ = np.histogram(self.recent_data[column_name], bins=bin_edges)

        # Add epsilon to avoid division by zero
        hist_probs = hist_counts / sum(hist_counts)
        recent_probs = recent_counts / sum(recent_counts)

        # Calculate KLD
        kld = entropy(hist_probs, recent_probs)

        drift_detected = kld > self.threshold

        return drift_detected, kld
