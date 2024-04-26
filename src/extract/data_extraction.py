import pandas as pd
import json
from typing import Any
import toml

from loguru import logger

# Import dynamic schema creation function
from extract.data_validation import DynamicSchema

# Set up logger
from utils.logging.logger import setup_logging

setup_logging()

# Load configuration
config = toml.load("./extract/config.toml")

class DataReader:
    """Base class for data readers."""
    def __init__(self, file_path: str, schema_name: str, columns: list[str] = None):
        self.file_path = file_path
        self.columns = columns
        # Instantiate the schema using the dynamic schema creator
        self.schema = DynamicSchema.from_config(schema_name)

    def read_data(self) -> pd.DataFrame:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def validate_data(self, data: pd.DataFrame) -> pd.DataFrame:
        logger.info(f"Validating data using {self.schema.__class__.__name__}")
        return self.schema.validate(data, lazy=True)

class CSVReader(DataReader):
    """Reader class for CSV data."""
    def read_data(self) -> pd.DataFrame:
        logger.info(f"Reading CSV data from {self.file_path}")
        data = pd.read_csv(self.file_path)
        return self.validate_data(data)

class JSONLReader(DataReader):
    """Reader class for JSON Lines data."""
    def read_data(self) -> pd.DataFrame:
        logger.info(f"Reading JSONL data from {self.file_path}")
        with open(self.file_path, 'r') as file:
            data = [json.loads(line) for line in file]
            columns = [key for key in data[0].keys()]
            df_data = []
            if self.columns:
                columns = [cols[-1][0] if len(cols) > 1 else cols[-1] for cols in self.columns]
                for element in data:
                    df_data.append([
                        element[col[0][0]][col[1][0]] if len(col) > 1 else element[col[0]] for col in self.columns
                        ])
                data = df_data
        
            df = pd.DataFrame(data, columns=columns)
        return self.validate_data(df)

class JSONReader(DataReader):
    """Reader class for JSON data."""
    def read_data(self) -> pd.DataFrame:
        logger.info(f"Reading JSON data from {self.file_path}")
        with open(self.file_path, 'r') as file:
            data = pd.DataFrame(json.load(file))
        return self.validate_data(data)

def reader_factory(data_source: str) -> DataReader:
    """Factory function to instantiate data readers based on configuration."""
    source_config = config['data_sources'][data_source]
    if source_config['reader'] == 'CSVReader':
        return CSVReader(source_config['path'], source_config['schema'])
    elif source_config['reader'] == 'JSONLReader':
        return JSONLReader(source_config['path'], source_config['schema'], source_config.get('columns'))
    elif source_config['reader'] == 'JSONReader':
        return JSONReader(source_config['path'], source_config['schema'], source_config.get('columns'))
    else:
        raise ValueError(f"Unknown reader type: {source_config['reader']}")
