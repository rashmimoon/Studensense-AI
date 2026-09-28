from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import shap
import joblib

from config import FEATURE_COLUMNS, HUMAN_READABLE_FEATURES, RISK_LEVELS
from src.ml.predict import get_model_and_preprocessor
from src.utils.logging_utils import get_logger

logger = get_logger("shap_explainer")

_cached_explainer = None

def get_shap_explainer(model, X_background: np.ndarray):
    """
    Initializes and caches a SHAP TreeExplainer or KernelExplainer depending on model compatibility.
    """
    global _cached_explainer
    if _cached_explainer is not None:
        return _cached_explainer
        
    try:
        # Try TreeExplainer first (fastest for tree-based models like RandomForest, DecisionTree, GradientBoosting)
        _cached_explainer = shap.TreeExplainer(model)
        logger.info("Initialized SHAP TreeExplainer.")
    except Exception as e:
        logger.warning(f"TreeExplainer failed ({e}). Falling back to SHAP Explainer / KernelExplainer.")
        # Summary background data for KernelExplainer efficiency
        background_summary = shap.kmeans(X_background, k=min(10, len(X_background)))
        _cached_explainer = shap.KernelExplainer(model.predict_proba, background_summary)
        
    return _cached_explainer

def explain_student_prediction(student_input: Union[Dict[str, Any], pd.DataFrame, pd.Series], background_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Generates local SHAP feature importance and directional contributions for an individual student.
    
    Returns:
        Dict with feature contributions, directional impact, positive/negative factor lists, 
        and disclaimer notice.
    """
    model, preprocessor = get_model_and_preprocessor()
    
    if isinstance(student_input, dict):
        df_single = pd.DataFrame([student_input])
    elif isinstance(student_input, pd.Series):
        df_single = pd.DataFrame([student_input.to_dict()])
    else:
        df_single = student_input.copy()
        
    X_raw = df_single[FEATURE_COLUMNS]
    X_scaled = preprocessor.transform(X_raw)
    
    # Predict target risk label
    pred_class_id = int(model.predict(X_scaled)[0])
    pred_label = RISK_LEVELS[pred_class_id]
    
    # Initialize background array
    if background_df is not None:
        X_background = preprocessor.transform(background_df[FEATURE_COLUMNS])
    else:
        # Default synthetic background
        X_background = np.zeros((10, len(FEATURE_COLUMNS)))
        
    explainer = get_shap_explainer(model, X_background)
    
    try:
        shap_values = explainer.shap_values(X_scaled)
        
        # Handle different SHAP output formats (multiclass array vs list of arrays)
        if isinstance(shap_values, list):
            # List of arrays per class -> pick target class array
            cls_shap = shap_values[pred_class_id][0]
        elif isinstance(shap_values, np.ndarray):
            if shap_values.ndim == 3:
                # Shape (samples, features, classes) or (samples, classes, features)
                if shap_values.shape[2] == len(RISK_LEVELS):
                    cls_shap = shap_values[0, :, pred_class_id]
                else:
                    cls_shap = shap_values[0, pred_class_id, :]
            elif shap_values.ndim == 2:
                cls_shap = shap_values[0]
            else:
                cls_shap = np.array(shap_values).flatten()
        else:
            cls_shap = np.array(shap_values).flatten()
            
    except Exception as e:
        logger.error(f"Error computing SHAP values: {e}. Returning heuristic feature contribution fallback.")
        # Robust fallback feature importance
        cls_shap = (X_scaled[0] - np.mean(X_background, axis=0)) * 0.1

    # Format feature contributions
    feature_contributions = []
    positive_factors = []
    negative_factors = []
    
    raw_vals = df_single[FEATURE_COLUMNS].iloc[0].to_dict()
    
    for idx, feature_name in enumerate(FEATURE_COLUMNS):
        val = float(raw_vals[feature_name])
        shap_val = float(cls_shap[idx]) if idx < len(cls_shap) else 0.0
        human_name = HUMAN_READABLE_FEATURES.get(feature_name, feature_name)
        
        item = {
            "feature": feature_name,
            "human_readable_name": human_name,
            "feature_value": val,
            "shap_value": round(shap_val, 4),
            "impact_direction": "Increases Risk" if shap_val > 0 else "Decreases Risk"
        }
        feature_contributions.append(item)
        
        if shap_val > 0.01:
            positive_factors.append(f"{human_name} ({val}) increases predicted risk.")
        elif shap_val < -0.01:
            negative_factors.append(f"{human_name} ({val}) reduces predicted risk.")

    # Sort contributions by absolute SHAP impact
    feature_contributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    
    return {
        "student_id": str(df_single["student_id"].values[0]) if "student_id" in df_single.columns else "N/A",
        "predicted_risk_level": pred_label,
        "feature_contributions": feature_contributions,
        "top_risk_drivers": positive_factors,
        "top_protective_factors": negative_factors,
        "disclaimer": (
            "SHAP explanations reflect the model's numerical feature contributions for this specific prediction "
            "and do not establish causal relationships."
        )
    }

def get_global_feature_importance(df_sample: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Computes global feature importance across a dataset sample.
    """
    model, preprocessor = get_model_and_preprocessor()
    X_scaled = preprocessor.transform(df_sample[FEATURE_COLUMNS])
    
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        importances = np.ones(len(FEATURE_COLUMNS)) / len(FEATURE_COLUMNS)
        
    global_importance = []
    for idx, f_name in enumerate(FEATURE_COLUMNS):
        imp = float(importances[idx])
        human_name = HUMAN_READABLE_FEATURES.get(f_name, f_name)
        global_importance.append({
            "feature": f_name,
            "human_readable_name": human_name,
            "importance": round(imp, 4)
        })
        
    global_importance.sort(key=lambda x: x["importance"], reverse=True)
    return global_importance
