import pytest
import pandas as pd
import numpy as np
from src.data.validate import validate_student_data, generate_data_dictionary
from src.data.preprocess import prepare_train_test_data

def test_validate_student_data_valid(tmp_path):
    valid_df = pd.DataFrame({
        "student_id": ["STU001", "STU002"],
        "attendance_percentage": [85.0, 45.0],
        "assignment_average": [78.0, 50.0],
        "internal_marks": [80.0, 40.0],
        "exam_average": [82.0, 35.0],
        "study_hours_per_week": [15.0, 5.0],
        "participation_score": [70.0, 30.0],
        "previous_semester_score": [75.0, 45.0],
        "risk_level": ["Low", "High"]
    })
    is_valid, report = validate_student_data(valid_df)
    assert is_valid is True
    assert len(report["missing_columns"]) == 0
    assert report["duplicate_ids"] == 0

def test_validate_student_data_missing_column():
    invalid_df = pd.DataFrame({
        "student_id": ["STU001"],
        "attendance_percentage": [85.0],
        "risk_level": ["Low"]
    })
    is_valid, report = validate_student_data(invalid_df)
    assert is_valid is False
    assert len(report["missing_columns"]) > 0

def test_validate_student_data_invalid_range():
    out_of_bounds_df = pd.DataFrame({
        "student_id": ["STU001"],
        "attendance_percentage": [150.0],  # Invalid percentage > 100
        "assignment_average": [78.0],
        "internal_marks": [80.0],
        "exam_average": [82.0],
        "study_hours_per_week": [15.0],
        "participation_score": [70.0],
        "previous_semester_score": [75.0],
        "risk_level": ["Low"]
    })
    is_valid, report = validate_student_data(out_of_bounds_df)
    assert is_valid is False
    assert report["invalid_range_counts"]["attendance_percentage"] == 1

def test_generate_data_dictionary():
    sample_df = pd.DataFrame({
        "student_id": ["STU001"],
        "attendance_percentage": [85.0],
        "risk_level": ["Low"]
    })
    dict_df = generate_data_dictionary(sample_df)
    assert len(dict_df) == 3
    assert "Column Name" in dict_df.columns
