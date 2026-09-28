from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from config import RISK_LEVELS
from src.utils.logging_utils import get_logger

logger = get_logger("evaluate")

def evaluate_model_performance(y_true: np.ndarray, y_pred: np.ndarray, model_name: str = "Model") -> Dict[str, Any]:
    """
    Evaluates classification performance across multiple metrics.
    
    Returns:
        Dict containing accuracy, macro/weighted precision, recall, f1, confusion matrix, 
        and class-wise breakdown.
    """
    acc = float(accuracy_score(y_true, y_pred))
    
    # Macro metrics
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    
    # Weighted metrics
    p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    
    # Class-wise metrics
    p_class, r_class, f1_class, support_class = precision_recall_fscore_support(y_true, y_pred, average=None, zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred)
    
    class_report_dict = {}
    for idx, label in enumerate(RISK_LEVELS):
        if idx < len(p_class):
            class_report_dict[label] = {
                "precision": round(float(p_class[idx]), 4),
                "recall": round(float(r_class[idx]), 4),
                "f1_score": round(float(f1_class[idx]), 4),
                "support": int(support_class[idx])
            }
            
    metrics = {
        "model_name": model_name,
        "accuracy": round(acc, 4),
        "macro_precision": round(float(p_macro), 4),
        "macro_recall": round(float(r_macro), 4),
        "macro_f1": round(float(f1_macro), 4),
        "weighted_f1": round(float(f1_weighted), 4),
        "confusion_matrix": cm.tolist(),
        "class_wise_metrics": class_report_dict
    }
    
    logger.info(f"--- Evaluation Summary [{model_name}] ---")
    logger.info(f"Accuracy: {acc:.4f} | Macro F1: {f1_macro:.4f} | Macro Recall: {r_macro:.4f}")
    
    return metrics

def format_evaluation_markdown(metrics: Dict[str, Any]) -> str:
    """Formats evaluation dictionary into clean Markdown for reporting."""
    md = f"### Model Evaluation Report: `{metrics['model_name']}`\n\n"
    md += f"- **Accuracy**: `{metrics['accuracy'] * 100:.2f}%`\n"
    md += f"- **Macro F1-Score**: `{metrics['macro_f1']:.4f}`\n"
    md += f"- **Macro Recall**: `{metrics['macro_recall']:.4f}`\n"
    md += f"- **Macro Precision**: `{metrics['macro_precision']:.4f}`\n\n"
    
    md += "#### Class-wise Performance Breakdown\n\n"
    md += "| Risk Level | Precision | Recall | F1-Score | Support |\n"
    md += "|---|---|---|---|---|\n"
    for label, stats in metrics["class_wise_metrics"].items():
        md += f"| **{label}** | {stats['precision']:.4f} | {stats['recall']:.4f} | {stats['f1_score']:.4f} | {stats['support']} |\n"
        
    return md
