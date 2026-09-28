import os
from pathlib import Path
import pandas as pd
from config import RAW_DATA_PATH
from src.utils.logging_utils import get_logger

logger = get_logger("load_data")

def load_raw_data(data_path=None) -> pd.DataFrame:
    """
    Loads student raw dataset from CSV.
    
    Args:
        data_path: Optional path to raw dataset CSV file.
        
    Returns:
        pd.DataFrame containing raw student records.
    """
    path = Path(data_path) if data_path else RAW_DATA_PATH
    
    if not path.exists():
        logger.error(f"Dataset file not found at: {path}")
        raise FileNotFoundError(f"Student dataset not found at '{path}'. Please ensure data file exists.")
        
    logger.info(f"Loading raw student data from '{path}'...")
    try:
        df = pd.read_csv(path)
        logger.info(f"Successfully loaded dataset with {len(df)} records and {len(df.columns)} columns.")
        return df
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        raise ValueError(f"Could not parse CSV file at '{path}': {e}")
