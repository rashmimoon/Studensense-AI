from typing import Dict, Any, Tuple, List
import pandas as pd
from config import ID_COLUMN, TARGET_COLUMN, FEATURE_COLUMNS, RISK_LEVELS
from src.utils.logging_utils import get_logger

logger = get_logger("validate")

def validate_student_data(df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates student dataset for required columns, data types, missing values, and valid numerical ranges.
    
    Returns:
        Tuple[bool, Dict[str, Any]]: (is_valid, validation_report)
    """
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_columns": [],
        "invalid_range_counts": {},
        "missing_value_counts": df.isnull().sum().to_dict(),
        "duplicate_ids": 0,
        "invalid_target_values": [],
        "is_valid": True,
        "warnings": [],
        "errors": []
    }
    
    # 1. Check Required Columns
    required_cols = [ID_COLUMN, TARGET_COLUMN] + FEATURE_COLUMNS
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        report["missing_columns"] = missing_cols
        report["is_valid"] = False
        report["errors"].append(f"Missing required columns: {missing_cols}")
        return False, report

    # 2. Check Duplicate Student IDs
    if ID_COLUMN in df.columns:
        dups = df[ID_COLUMN].duplicated().sum()
        report["duplicate_ids"] = int(dups)
        if dups > 0:
            report["warnings"].append(f"Found {dups} duplicate student_id records.")

    # 3. Check Range Constraints for Numerical Features
    # Percentage features should be within 0 to 100
    percentage_cols = [
        "attendance_percentage",
        "assignment_average",
        "internal_marks",
        "exam_average",
        "participation_score",
        "previous_semester_score",
    ]
    
    for col in FEATURE_COLUMNS:
        if col in df.columns:
            if col in percentage_cols:
                invalid_mask = (df[col] < 0) | (df[col] > 100)
            elif col == "study_hours_per_week":
                invalid_mask = (df[col] < 0) | (df[col] > 168)  # Max hours in a week
            else:
                invalid_mask = df[col] < 0
                
            invalid_count = int(invalid_mask.sum())
            report["invalid_range_counts"][col] = invalid_count
            if invalid_count > 0:
                report["is_valid"] = False
                report["errors"].append(f"Column '{col}' has {invalid_count} out-of-bounds values.")

    # 4. Check Target Column Labels
    if TARGET_COLUMN in df.columns:
        unique_targets = df[TARGET_COLUMN].dropna().unique()
        invalid_targets = [t for t in unique_targets if t not in RISK_LEVELS]
        if invalid_targets:
            report["invalid_target_values"] = invalid_targets
            report["is_valid"] = False
            report["errors"].append(f"Target column '{TARGET_COLUMN}' contains unexpected labels: {invalid_targets}")

    logger.info(f"Data validation completed. Valid: {report['is_valid']}")
    return report["is_valid"], report

def generate_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a structured Data Dictionary summarizing column statistics, data types, 
    missing counts, ranges, and feature suitability.
    """
    dict_rows = []
    required_cols = [ID_COLUMN, TARGET_COLUMN] + FEATURE_COLUMNS
    
    for col in df.columns:
        col_type = str(df[col].dtype)
        null_count = int(df[col].isnull().sum())
        unique_count = int(df[col].nunique())
        
        if pd.api.types.is_numeric_dtype(df[col]):
            val_min = round(float(df[col].min()), 2) if not df[col].isnull().all() else None
            val_max = round(float(df[col].max()), 2) if not df[col].isnull().all() else None
            val_range = f"[{val_min}, {val_max}]"
        else:
            sample_vals = df[col].dropna().unique()[:3]
            val_range = f"Categories: {list(sample_vals)}"
            
        if col == ID_COLUMN:
            role = "Identifier (Excluded from modeling)"
        elif col == TARGET_COLUMN:
            role = "Target Label (Low / Medium / High)"
        elif col in FEATURE_COLUMNS:
            role = "Predictive Feature"
        else:
            role = "Secondary Attribute"
            
        dict_rows.append({
            "Column Name": col,
            "Data Type": col_type,
            "Role": role,
            "Missing Count": null_count,
            "Unique Values": unique_count,
            "Range / Values": val_range
        })
        
    return pd.DataFrame(dict_rows)
