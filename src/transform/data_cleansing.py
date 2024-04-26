"""Module to handle all data-clensing operations."""

import pandas as pd

class DataCleansing:
    @staticmethod
    def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows from a DataFrame."""
        return data.drop_duplicates()

    @staticmethod
    def remove_nulls(data: pd.DataFrame) -> pd.DataFrame:
        """Remove rows with null values from a DataFrame."""
        return data.dropna()

    @staticmethod
    def remove_outliers(data: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.DataFrame:
        """Remove outliers from a DataFrame based on the Z-score of a column."""
        z_scores = (data[column] - data[column].mean()) / data[column].std()
        return data[(z_scores.abs() < threshold)]

    @staticmethod
    def remove_negatives(data: pd.DataFrame, column: str) -> pd.DataFrame:
        """Remove rows with negative values from a DataFrame."""
        return data[data[column] >= 0]

    @staticmethod
    def clean_data(data: pd.DataFrame) -> pd.DataFrame:
        """Clean the data by removing duplicates, nulls, and outliers."""
        cleaned_data = DataCleansing.remove_duplicates(data)
        cleaned_data = DataCleansing.remove_nulls(cleaned_data)
        for column in cleaned_data.select_dtypes(include='number').columns:
            cleaned_data = DataCleansing.remove_outliers(cleaned_data, column)
            cleaned_data = DataCleansing.remove_negatives(cleaned_data, column)
        return cleaned_data