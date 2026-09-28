import json
from datetime import datetime
from pathlib import Path
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

from config import (
    MODEL_FILE_PATH, TRAINED_MODEL_DIR, MODEL_METADATA_PATH, RANDOM_SEED
)
from src.data.load_data import load_raw_data
from src.data.validate import validate_student_data
from src.data.preprocess import prepare_train_test_data
from src.ml.evaluate import evaluate_model_performance, format_evaluation_markdown
from src.utils.logging_utils import get_logger

logger = get_logger("train")

def train_and_select_best_model(data_path=None) -> dict:
    """
    Trains baseline and candidate classifiers, evaluates them, selects the optimal model,
    and saves model binary + metadata.
    """
    # 1. Load Data
    df = load_raw_data(data_path)
    
    # 2. Validate Data
    is_valid, report = validate_student_data(df)
    if not is_valid:
        raise ValueError(f"Data validation failed: {report['errors']}")
        
    # 3. Preprocess and Split Data
    X_train, X_test, y_train, y_test, preprocessor, raw_test_df = prepare_train_test_data(df)
    
    # 4. Define Candidate Models
    candidates = {
        "DecisionTree": DecisionTreeClassifier(random_state=RANDOM_SEED, max_depth=5),
        "RandomForest": RandomForestClassifier(random_state=RANDOM_SEED, n_estimators=100, max_depth=6),
        "GradientBoosting": GradientBoostingClassifier(random_state=RANDOM_SEED, n_estimators=100, learning_rate=0.1),
        "LogisticRegression": LogisticRegression(random_state=RANDOM_SEED, max_iter=500)
    }
    
    eval_results = {}
    fitted_models = {}
    
    logger.info("Training and evaluating candidate classifiers...")
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = evaluate_model_performance(y_test, y_pred, model_name=name)
        eval_results[name] = metrics
        fitted_models[name] = model
        
    # 5. Model Selection Criterion: Highest Macro F1-score
    best_model_name = max(eval_results, key=lambda k: eval_results[k]["macro_f1"])
    best_model = fitted_models[best_model_name]
    best_metrics = eval_results[best_model_name]
    
    logger.info(f"==> Selected Best Model: '{best_model_name}' (Macro F1: {best_metrics['macro_f1']:.4f}, Accuracy: {best_metrics['accuracy']:.4f})")
    
    # 6. Save Model Artifact
    TRAINED_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_FILE_PATH)
    logger.info(f"Model saved to '{MODEL_FILE_PATH}'")
    
    # 7. Save Metadata JSON
    metadata = {
        "model_name": best_model_name,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "random_seed": RANDOM_SEED,
        "evaluation_metrics": best_metrics,
        "all_candidates": {k: {"accuracy": v["accuracy"], "macro_f1": v["macro_f1"]} for k, v in eval_results.items()}
    }
    
    with open(MODEL_METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)
    logger.info(f"Model metadata saved to '{MODEL_METADATA_PATH}'")
    
    return metadata

if __name__ == "__main__":
    train_and_select_best_model()
