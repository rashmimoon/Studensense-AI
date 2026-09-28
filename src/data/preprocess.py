from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from config import (
    ID_COLUMN, TARGET_COLUMN, FEATURE_COLUMNS, 
    PREPROCESSOR_FILE_PATH, PREPROCESSOR_DIR, RANDOM_SEED, TEST_SIZE
)
from src.utils.logging_utils import get_logger

logger = get_logger("preprocess")

TARGET_MAPPING = {"Low": 0, "Medium": 1, "High": 2}
REVERSE_TARGET_MAPPING = {0: "Low", 1: "Medium", 2: "High"}

def create_preprocessing_pipeline() -> ColumnTransformer:
    """
    Creates scikit-learn ColumnTransformer pipeline for imputing and scaling features.
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, FEATURE_COLUMNS)
        ],
        remainder="drop"
    )
    return preprocessor

def prepare_train_test_data(
    df: pd.DataFrame, 
    test_size: float = TEST_SIZE, 
    random_state: int = RANDOM_SEED
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, ColumnTransformer, pd.DataFrame]:
    """
    Preprocesses dataset and splits into reproducible train/test sets.
    
    Returns:
        Tuple: (X_train_scaled, X_test_scaled, y_train, y_test, preprocessor, raw_test_df)
    """
    logger.info("Preparing train/test split and fitting preprocessor...")
    
    # Filter features and target
    X = df[FEATURE_COLUMNS].copy()
    
    # Clean out of bound values if any
    percentage_cols = [
        "attendance_percentage", "assignment_average", "internal_marks", 
        "exam_average", "participation_score", "previous_semester_score"
    ]
    for col in percentage_cols:
        if col in X.columns:
            X[col] = X[col].clip(0.0, 100.0)
    if "study_hours_per_week" in X.columns:
        X["study_hours_per_week"] = X["study_hours_per_week"].clip(0.0, 168.0)

    # Encode target
    y = df[TARGET_COLUMN].map(TARGET_MAPPING).values
    
    # Train / Test split
    X_train_raw, X_test_raw, y_train, y_test, _, test_indices = train_test_split(
        X, y, df.index, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Fit preprocessor on training data
    preprocessor = create_preprocessing_pipeline()
    X_train_scaled = preprocessor.fit_transform(X_train_raw)
    X_test_scaled = preprocessor.transform(X_test_raw)
    
    # Save preprocessor artifact
    save_preprocessor(preprocessor)
    
    raw_test_df = df.loc[test_indices].copy()
    
    logger.info(f"Preprocessed train shape: {X_train_scaled.shape}, test shape: {X_test_scaled.shape}")
    return X_train_scaled, X_test_scaled, y_train, y_test, preprocessor, raw_test_df

def save_preprocessor(preprocessor: ColumnTransformer, path=None):
    """Saves fitted preprocessor pipeline to disk."""
    save_path = path or PREPROCESSOR_FILE_PATH
    PREPROCESSOR_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, save_path)
    logger.info(f"Preprocessor saved to '{save_path}'")

def load_preprocessor(path=None) -> ColumnTransformer:
    """Loads saved preprocessor pipeline from disk."""
    load_path = path or PREPROCESSOR_FILE_PATH
    if not load_path.exists():
        raise FileNotFoundError(f"Preprocessor file not found at '{load_path}'. Please run training first.")
    logger.info(f"Loading preprocessor from '{load_path}'...")
    return joblib.load(load_path)
