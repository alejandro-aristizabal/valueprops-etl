"""Module to merge and transform data for analysis."""

import pandas as pd
from loguru import logger

from utils.logging.logger import setup_logging

# Initialize the logger
setup_logging()

class DataMerger:
    """Class to merge the prints, taps, and pays dataframes."""
    def __init__(self, prints: pd.DataFrame, taps: pd.DataFrame, pays: pd.DataFrame) -> None:
        """Initialize the DataMerger class.

        Args:
            prints_df (pd.DataFrame): The prints dataframe.
            taps_df (pd.DataFrame): The taps dataframe.
            pays_df (pd.DataFrame): The pays dataframe.
        """
        self.prints_df = prints
        self.taps_df = taps
        self.pays_df = pays

    def merge(self) -> pd.DataFrame:
        """Merge the prints, taps, and pays dataframes.

        Returns:
            pd.DataFrame: The merged dataframe.
        """
        logger.info("Adding 'clicked' column to taps dataframe")
        self.taps_df['clicked'] = 1
        logger.info("Adding 'showed' column to prints dataframe")
        self.prints_df["showed"] = 1

        # Merge prints and taps dataframes
        logger.info("Merging prints and taps dataframes")
        merged_df = pd.merge(self.prints_df, self.taps_df, on=[
            'day', 'position', 'value_prop', 'user_id'], how='outer')
        
        # Merge the previous merged dataframe with the pays dataframe
        logger.info("Merging the previous merged dataframe with the pays dataframe")
        merged_df = pd.merge(merged_df, self.pays_df, 
                            left_on=['day', 'user_id', 'value_prop'],
                            right_on=['pay_date', 'user_id', 'value_prop'],
            how='outer')
        

        return merged_df
    


class BusinessMetrics:
    """Class to calculate business metrics."""
    def __init__(self, merged_df: pd.DataFrame) -> None:
        """Initialize the BusinessMetrics class.

        Args:
            merged_df (pd.DataFrame): The merged dataframe.
        """
        self.merged_df = merged_df

    def calculate_metrics(self) -> pd.DataFrame:
        """Calculate the business metrics.

        Returns:
            pd.DataFrame: The calculated metrics.
        """

        # Replace NaN values in 'clicked' column with 0
        self.merged_df['clicked'] = self.merged_df['clicked'].fillna(0)

        # Create a column to indicate if 'day' is NaN
        self.merged_df['is_day_nan'] = self.merged_df['day'].isna()
        
        # Replace NaN values in 'day' with corresponding 'pay_date' values
        self.merged_df['day'] = self.merged_df['day'].fillna(self.merged_df['pay_date'])
        
        # Sort DataFrame by 'day' in ascending order
        self.merged_df.sort_values(by='day', inplace=True, ascending=True)
        
        # Set 'day' as the index of the DataFrame
        self.merged_df.set_index('day', inplace=True)
        
        # Replace NaN values in 'clicked', 'showed', 'pay_date', and 'total' with 0
        logger.info("Replacing NaN values in 'clicked', 'showed', 'pay_date', and 'total' with 0")
        self.merged_df['clicked'] = self.merged_df['clicked'].fillna(0)
        self.merged_df['showed'] = self.merged_df['showed'].fillna(0)
        self.merged_df['pay_date'] = self.merged_df['pay_date'].fillna(0)
        self.merged_df['total'] = self.merged_df['total'].fillna(0)
        
        # Group data by 'user_id' and 'value_prop'
        grouped = self.merged_df.groupby(['user_id', 'value_prop'])
        
        # Create a new DataFrame to hold the results
        result = pd.DataFrame()

        logger.info("Calculating business metrics")
        
        # Calculate rolling count of 'showed' over the past 3 weeks
        result['3_week_showed_count'] = grouped['showed'].rolling(window="21D").sum()
        
        # Calculate rolling count of 'clicked' over the past 3 weeks
        result['3_week_clicked_count'] = grouped['clicked'].rolling(window="21D").sum()
        
        # Calculate rolling count of 'pay_date' over the past 3 weeks
        result['3_week_pay_count'] = grouped['pay_date'].rolling(window="21D").count()
        
        # Calculate rolling sum of 'total' over the past 3 weeks
        result['3_week_pay_amount'] = grouped['total'].rolling(window="21D").sum()
        
        # Reset index to default
        self.merged_df.reset_index(inplace=True)
        
        return result
