""" Main entry point for the application. """

from loguru import logger

from extract.data_extraction import reader_factory
from transform.data_transformer import DataMerger, BusinessMetrics
from load.main import drift_monitoring
from utils.logging.logger import setup_logging

# Initialize the logger
setup_logging()

def main():
    # Define the data sources from config.toml
    data_sources = ['pays', 'prints', 'taps']
    
    # Dictionary to store the loaded dataframes
    dataframes = {}

    for source in data_sources:
        try:
            logger.info(f"Processing data source: {source}")
            # Create the reader using the factory
            reader = reader_factory(source)
            # Read and validate data
            data = reader.read_data()
            # Store the validated data in a dictionary
            dataframes[source] = data
            logger.info(f"Data loaded and validated for {source}: {data.shape[0]} rows and {data.shape[1]} columns")
        except Exception as e:
            logger.error(f"Error processing data source {source}: {e}")
            logger.exception(e)

    for source, df in dataframes.items():
        output_path = f"../data/validated_{source}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Validated data saved to {output_path}")

    # Merge the dataframes
    data_merger = DataMerger(dataframes['prints'], dataframes['taps'], dataframes['pays'])
    merged_df = data_merger.merge()

    # Calculate business metrics
    business_metrics = BusinessMetrics(merged_df)
    metrics_df = business_metrics.calculate_metrics()

    output_path = "../data/business_metrics.csv"
    metrics_df.to_csv(output_path, index=True)

    logger.info(f"Business metrics saved to {output_path}")

    # Start drift monitoring
    drift_monitoring()

if __name__ == "__main__":
    main()
