import pytest
import pandas as pd
from src.xai.shap_explainer import explain_student_prediction
from src.data.load_data import load_raw_data

def test_explain_student_prediction():
    df_raw = load_raw_data()
    student_sample = df_raw.iloc[0].to_dict()
    
    shap_res = explain_student_prediction(student_sample, background_df=df_raw)
    
    assert "predicted_risk_level" in shap_res
    assert "feature_contributions" in shap_res
    assert len(shap_res["feature_contributions"]) == 7
    assert "disclaimer" in shap_res
    
    first_feature = shap_res["feature_contributions"][0]
    assert "feature" in first_feature
    assert "shap_value" in first_feature
    assert "human_readable_name" in first_feature
