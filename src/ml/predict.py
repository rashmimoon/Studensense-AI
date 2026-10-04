from typing import Dict, Any, Union
import numpy as np
import pandas as pd
import joblib

from config import MODEL_FILE_PATH, FEATURE_COLUMNS, RISK_LEVELS
from src.data.preprocess import load_preprocessor, REVERSE_TARGET_MAPPING
from src.utils.logging_utils import get_logger

logger = get_logger("predict")

_cached_model = None
_cached_preprocessor = None

def get_model_and_preprocessor():
    """Lazy loader for model and preprocessor artifacts with caching."""
    global _cached_model, _cached_preprocessor
    if _cached_model is None or _cached_preprocessor is None:
        if not MODEL_FILE_PATH.exists():
            logger.info("Model file missing. Running automatic model training on startup...")
            from src.ml.train import train_and_select_best_model
            train_and_select_best_model()
            
        _cached_model = joblib.load(MODEL_FILE_PATH)
        _cached_preprocessor = load_preprocessor()
        
    return _cached_model, _cached_preprocessor

def predict_student_risk(student_input: Union[Dict[str, Any], pd.DataFrame, pd.Series]) -> Dict[str, Any]:
    """
    Predicts academic risk level and class probabilities for a single student record.
    
    Args:
        student_input: Dict or DataFrame row containing student features.
        
    Returns:
        Dict containing risk_level, confidence, probabilities dict, and input feature values.
    """
    model, preprocessor = get_model_and_preprocessor()
    
    if isinstance(student_input, dict):
        df_single = pd.DataFrame([student_input])
    elif isinstance(student_input, pd.Series):
        df_single = pd.DataFrame([student_input.to_dict()])
    elif isinstance(student_input, pd.DataFrame):
        df_single = student_input.copy()
    else:
        raise TypeError(f"Unsupported student_input type: {type(student_input)}")
        
    # Ensure feature alignment
    missing_feats = [col for col in FEATURE_COLUMNS if col not in df_single.columns]
    if missing_feats:
        raise ValueError(f"Missing required feature columns for prediction: {missing_feats}")
        
    X_raw = df_single[FEATURE_COLUMNS]
    X_scaled = preprocessor.transform(X_raw)
    
    pred_class_id = int(model.predict(X_scaled)[0])
    pred_label = REVERSE_TARGET_MAPPING.get(pred_class_id, "Unknown")
    
    if hasattr(model, "predict_proba"):
        probs_arr = model.predict_proba(X_scaled)[0]
        probs_dict = {
            RISK_LEVELS[i]: round(float(probs_arr[i]), 4)
            for i in range(len(probs_arr))
        }
        confidence = round(float(np.max(probs_arr)), 4)
    else:
        probs_dict = {label: (1.0 if label == pred_label else 0.0) for label in RISK_LEVELS}
        confidence = 1.0

    student_id = str(df_single["student_id"].values[0]) if "student_id" in df_single.columns else "N/A"
    
    return {
        "student_id": student_id,
        "risk_level": pred_label,
        "predicted_class_id": pred_class_id,
        "confidence": confidence,
        "probabilities": probs_dict,
        "feature_values": df_single[FEATURE_COLUMNS].iloc[0].to_dict(),
        "scaled_features": X_scaled[0]
    }

def predict_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Predicts risk levels and probabilities for an entire batch DataFrame."""
    model, preprocessor = get_model_and_preprocessor()
    X_raw = df[FEATURE_COLUMNS]
    X_scaled = preprocessor.transform(X_raw)
    
    preds = model.predict(X_scaled)
    df_out = df.copy()
    df_out["predicted_risk_level"] = [REVERSE_TARGET_MAPPING[p] for p in preds]
    
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_scaled)
        for idx, label in enumerate(RISK_LEVELS):
            if idx < probs.shape[1]:
                df_out[f"prob_{label.lower()}"] = np.round(probs[:, idx], 4)
                
    return df_out
