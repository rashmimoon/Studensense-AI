import pytest
import pandas as pd
import numpy as np
from src.ml.train import train_and_select_best_model
from src.ml.predict import predict_student_risk, predict_batch
from config import RAW_DATA_PATH

def test_model_training_and_prediction():
    if not RAW_DATA_PATH.exists():
        pytest.skip("Raw dataset missing, skipping model test.")
        
    metadata = train_and_select_best_model()
    assert "model_name" in metadata
    assert metadata["evaluation_metrics"]["accuracy"] >= 0.70

def test_predict_student_risk_single():
    sample_student = {
        "student_id": "TEST_001",
        "attendance_percentage": 40.0,
        "assignment_average": 45.0,
        "internal_marks": 40.0,
        "exam_average": 35.0,
        "study_hours_per_week": 4.0,
        "participation_score": 30.0,
        "previous_semester_score": 40.0
    }
    pred_res = predict_student_risk(sample_student)
    assert pred_res["risk_level"] in ["Low", "Medium", "High"]
    assert "probabilities" in pred_res
    assert sum(pred_res["probabilities"].values()) == pytest.approx(1.0, abs=1e-2)
