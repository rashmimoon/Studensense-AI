import pytest
from src.rag.ingest import build_and_save_vector_index
from src.rag.retriever import retrieve_relevant_knowledge, build_query_from_student_profile
from src.genai.recommender import generate_personalized_recommendation

def test_rag_ingestion_and_retrieval():
    index_store = build_and_save_vector_index()
    assert index_store["total_chunks"] > 0
    
    # Query retrieval
    results = retrieve_relevant_knowledge("attendance lecture habit absenteeism", top_k=2)
    assert len(results) == 2
    assert "relevance_score" in results[0]
    assert "source_file" in results[0]

def test_genai_recommendation_generation():
    feature_vals = {
        "attendance_percentage": 50.0,
        "assignment_average": 45.0,
        "internal_marks": 40.0,
        "exam_average": 35.0,
        "study_hours_per_week": 4.0,
        "participation_score": 30.0,
        "previous_semester_score": 45.0
    }
    query = build_query_from_student_profile("High", feature_vals, ["Low attendance increases risk"])
    chunks = retrieve_relevant_knowledge(query, top_k=2)
    
    shap_factors = {
        "top_risk_drivers": ["Attendance Rate (50.0%) increases predicted risk."],
        "top_protective_factors": []
    }
    
    rec = generate_personalized_recommendation(
        "STU_TEST", "High", {"High": 0.85, "Medium": 0.10, "Low": 0.05}, feature_vals, shap_factors, chunks
    )
    
    assert "recommendation_text" in rec
    assert "Situation Summary" in rec["recommendation_text"]
    assert "Actionable Intervention Steps" in rec["recommendation_text"]
