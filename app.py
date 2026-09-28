import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configure Streamlit Page Settings
st.set_page_config(
    page_title="StudentSense AI — Student Behavior Prediction & Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .risk-badge-low {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        display: inline-block;
    }
    .risk-badge-medium {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        display: inline-block;
    }
    .risk-badge-high {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        display: inline-block;
    }
    .metric-card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Imports from src package
from config import (
    FEATURE_COLUMNS, HUMAN_READABLE_FEATURES, RISK_LEVELS, 
    RAW_DATA_PATH, MODEL_METADATA_PATH
)
from src.data.load_data import load_raw_data
from src.data.validate import validate_student_data, generate_data_dictionary
from src.ml.predict import predict_student_risk, predict_batch
from src.xai.shap_explainer import explain_student_prediction, get_global_feature_importance
from src.rag.retriever import retrieve_relevant_knowledge, build_query_from_student_profile
from src.genai.recommender import generate_personalized_recommendation

@st.cache_data
def get_cached_dataset():
    """Loads and caches student raw dataset."""
    try:
        return load_raw_data()
    except Exception as e:
        st.error(f"Error loading raw dataset: {e}")
        return pd.DataFrame()

# Main Header
st.markdown('<div class="main-header">🎓 STUDENTSENSE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Student Behavior Risk Prediction, Explainable AI (SHAP), RAG Vector Search & Personalized Guidance</div>', unsafe_allow_html=True)

df_raw = get_cached_dataset()

if df_raw.empty:
    st.warning("No dataset loaded. Please check data/raw/student_data.csv")
    st.stop()

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Select Module / Section:",
    [
        "1. Overview & System Status",
        "2. Student Risk Prediction & SHAP",
        "3. RAG & Personalized Recommendation",
        "4. Class-Level Analytics",
        "5. Data Quality & Data Dictionary"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("StudentSense AI v1.0 • Antigravity AI Stack")

# ==========================================
# PAGE 1: OVERVIEW & SYSTEM STATUS
# ==========================================
if page == "1. Overview & System Status":
    st.header("📋 Project Overview & Architecture")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students Analyzed", len(df_raw))
    with col2:
        high_risk_count = (df_raw["risk_level"] == "High").sum()
        st.metric("High Risk Students", high_risk_count, delta=f"{high_risk_count/len(df_raw)*100:.1f}%", delta_color="inverse")
    with col3:
        med_risk_count = (df_raw["risk_level"] == "Medium").sum()
        st.metric("Medium Risk Students", med_risk_count)
    with col4:
        low_risk_count = (df_raw["risk_level"] == "Low").sum()
        st.metric("Low Risk Students", low_risk_count)

    st.markdown("---")
    
    st.subheader("⚙️ System Pipeline Architecture")
    st.markdown("""
    ```
    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
    │  Student Academic    │───>│  scikit-learn Model  │───>│   SHAP Explainer     │
    │  & Engagement Data   │    │   Risk Prediction    │    │ (Local/Global Impact)│
    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘
                                                                       │
                                                                       ▼
    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
    │ Streamlit Dashboard  │<───│ Generative AI Engine │<───│   RAG Vector Store   │
    │ Interactive Insights │    │ Grounded Advice      │    │  Knowledge Retrieval │
    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘
    ```
    """)
    
    st.markdown("### 🏆 Trained Model Performance")
    if MODEL_METADATA_PATH.exists():
        import json
        with open(MODEL_METADATA_PATH, "r") as f:
            meta = json.load(f)
        st.success(f"Selected Model: **{meta['model_name']}** trained on {meta['trained_at']}")
        metrics = meta["evaluation_metrics"]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Model Accuracy", f"{metrics['accuracy']*100:.2f}%")
        m2.metric("Macro F1-Score", f"{metrics['macro_f1']:.4f}")
        m3.metric("Macro Recall", f"{metrics['macro_recall']:.4f}")
        m4.metric("Macro Precision", f"{metrics['macro_precision']:.4f}")
    else:
        st.info("Run `python -m src.ml.train` to view saved model evaluation metrics.")

# ==========================================
# PAGE 2: STUDENT RISK PREDICTION & SHAP
# ==========================================
elif page == "2. Student Risk Prediction & SHAP":
    st.header("🔍 Student Risk Prediction & SHAP Explanations")
    
    # Selection Mode
    mode = st.radio("Input Source Mode:", ["Select Existing Student ID", "Custom What-If Simulation"], horizontal=True)
    
    if mode == "Select Existing Student ID":
        student_id_sel = st.selectbox("Select Student ID:", df_raw["student_id"].unique())
        student_row = df_raw[df_raw["student_id"] == student_id_sel].iloc[0]
        student_data = student_row.to_dict()
    else:
        st.subheader("🛠️ Custom Student Attributes")
        c1, c2, c3 = st.columns(3)
        with c1:
            att = st.slider("Attendance Percentage (%)", 0.0, 100.0, 65.0)
            ass = st.slider("Assignment Average (%)", 0.0, 100.0, 58.0)
            int_m = st.slider("Internal Marks (%)", 0.0, 100.0, 55.0)
        with c2:
            ex_m = st.slider("Final Exam Average (%)", 0.0, 100.0, 50.0)
            hrs = st.slider("Weekly Study Hours", 0.0, 50.0, 8.0)
            part = st.slider("Class Participation Score", 0.0, 100.0, 45.0)
        with c3:
            prev = st.slider("Previous Semester Score (%)", 0.0, 100.0, 60.0)
            stu_id_custom = st.text_input("Custom Student ID", "SIM_001")
            
        student_data = {
            "student_id": stu_id_custom,
            "attendance_percentage": att,
            "assignment_average": ass,
            "internal_marks": int_m,
            "exam_average": ex_m,
            "study_hours_per_week": hrs,
            "participation_score": part,
            "previous_semester_score": prev
        }

    st.markdown("---")
    
    # Run Prediction
    try:
        pred_res = predict_student_risk(student_data)
        shap_res = explain_student_prediction(student_data, background_df=df_raw)
        
        col_risk, col_probs = st.columns([1, 2])
        
        with col_risk:
            st.markdown("### Predicted Risk Level")
            risk = pred_res["risk_level"]
            badge_class = f"risk-badge-{risk.lower()}"
            st.markdown(f'<div class="{badge_class}">{risk.upper()} RISK</div>', unsafe_allow_html=True)
            st.write(f"**Model Confidence:** `{pred_res['confidence']*100:.2f}%`")
            st.caption(f"Student ID: **{pred_res['student_id']}**")
            
        with col_probs:
            st.markdown("### Class Probabilities")
            probs = pred_res["probabilities"]
            for label in RISK_LEVELS:
                prob_val = probs.get(label, 0.0)
                st.write(f"**{label} Risk**: `{prob_val*100:.1f}%`")
                st.progress(prob_val)
                
        st.markdown("---")
        
        # SHAP Waterfall / Feature Contributions Visualization
        st.subheader("💡 Why This Prediction? (SHAP Feature Contributions)")
        st.info("SHAP (SHapley Additive exPlanations) shows how each student feature shifted the model's prediction relative to average baseline data.")
        
        shap_df = pd.DataFrame(shap_res["feature_contributions"])
        
        # Plotly Horizontal Bar Chart
        colors = ['#EF4444' if val > 0 else '#10B981' for val in shap_df['shap_value']]
        fig_shap = go.Figure(go.Bar(
            x=shap_df['shap_value'],
            y=shap_df['human_readable_name'],
            orientation='h',
            marker_color=colors,
            text=[f"{val:+.4f}" for val in shap_df['shap_value']],
            textposition='auto'
        ))
        fig_shap.update_layout(
            title="Local SHAP Feature Contributions (Red = Increases Risk, Green = Reduces Risk)",
            xaxis_title="SHAP Value (Impact on Risk)",
            yaxis_title="Feature",
            yaxis={'categoryorder':'total ascending'},
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_shap, use_container_width=True)
        
        c_pos, c_neg = st.columns(2)
        with c_pos:
            st.markdown("##### 🚨 Top Factors Increasing Risk")
            if shap_res["top_risk_drivers"]:
                for item in shap_res["top_risk_drivers"]:
                    st.write(f"- {item}")
            else:
                st.write("No major negative factors identified.")
                
        with c_neg:
            st.markdown("##### 🛡️ Top Protective Factors")
            if shap_res["top_protective_factors"]:
                for item in shap_res["top_protective_factors"]:
                    st.write(f"- {item}")
            else:
                st.write("No major protective factors identified.")
                
        st.caption(f"ℹ️ {shap_res['disclaimer']}")

    except Exception as e:
        st.error(f"Prediction / SHAP execution failed: {e}")

# ==========================================
# PAGE 3: RAG & PERSONALIZED RECOMMENDATION
# ==========================================
elif page == "3. RAG & Personalized Recommendation":
    st.header("🤖 RAG-Grounded Personalized Recommendation")
    
    student_id_sel = st.selectbox("Select Student for Recommendation:", df_raw["student_id"].unique())
    student_row = df_raw[df_raw["student_id"] == student_id_sel].iloc[0]
    student_data = student_row.to_dict()
    
    pred_res = predict_student_risk(student_data)
    shap_res = explain_student_prediction(student_data, background_df=df_raw)
    
    # Retrieve RAG Chunks
    query_str = build_query_from_student_profile(
        pred_res["risk_level"], pred_res["feature_values"], shap_res["top_risk_drivers"]
    )
    retrieved_chunks = retrieve_relevant_knowledge(query_str, top_k=3)
    
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        generate_btn = st.button("🚀 Generate Personalized Recommendation", type="primary")
        
    if generate_btn or "last_rec" in st.session_state:
        if generate_btn:
            with st.spinner("Retrieving knowledge context and generating grounded recommendations..."):
                rec_output = generate_personalized_recommendation(
                    student_data["student_id"],
                    pred_res["risk_level"],
                    pred_res["probabilities"],
                    pred_res["feature_values"],
                    shap_res,
                    retrieved_chunks
                )
                st.session_state["last_rec"] = rec_output
                st.session_state["last_stu_id"] = student_id_sel
        else:
            rec_output = st.session_state["last_rec"]

        st.markdown("---")
        st.subheader("📝 Actionable Educational Support Plan")
        st.caption(f"Generation Engine Mode: **{rec_output['mode']}**")
        
        st.markdown(rec_output["recommendation_text"])
        
        st.markdown("---")
        st.subheader("📚 Retrieved Knowledge Base Chunks (RAG Traceability)")
        for idx, chunk in enumerate(retrieved_chunks, 1):
            with st.expander(f"Source [{idx}]: {chunk['document_title']} — {chunk['section_heading']} (Score: {chunk['relevance_score']:.4f})"):
                st.write(f"**Category:** `{chunk['category']}` | **File:** `{chunk['source_file']}`")
                st.markdown(chunk["content"])

# ==========================================
# PAGE 4: CLASS-LEVEL ANALYTICS
# ==========================================
elif page == "4. Class-Level Analytics":
    st.header("📊 Class-Level Academic & Engagement Analytics")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Risk Level Class Breakdown")
        fig_pie = px.pie(
            df_raw, names="risk_level", title="Student Risk Distribution",
            color="risk_level",
            color_discrete_map={"Low": "#10B981", "Medium": "#F59E0B", "High": "#EF4444"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Attendance vs Exam Performance")
        fig_scatter = px.scatter(
            df_raw, x="attendance_percentage", y="exam_average",
            color="risk_level", hover_data=["student_id", "study_hours_per_week"],
            title="Attendance Rate vs Final Exam Score",
            color_discrete_map={"Low": "#10B981", "Medium": "#F59E0B", "High": "#EF4444"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Feature Correlation Matrix")
    num_df = df_raw[FEATURE_COLUMNS]
    corr = num_df.corr()
    fig_corr = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        title="Predictive Feature Correlation Matrix",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ==========================================
# PAGE 5: DATA QUALITY & DATA DICTIONARY
# ==========================================
elif page == "5. Data Quality & Data Dictionary":
    st.header("📋 Data Quality Report & Schema Dictionary")
    
    is_valid, val_report = validate_student_data(df_raw)
    
    st.subheader("Data Validation Summary")
    if is_valid:
        st.success("✅ Dataset schema, columns, and numerical ranges passed all validation checks!")
    else:
        st.error(f"❌ Data Validation Warnings/Errors: {val_report['errors']}")
        
    col_v1, col_v2, col_v3 = st.columns(3)
    col_v1.metric("Total Rows", val_report["total_rows"])
    col_v2.metric("Total Columns", val_report["total_columns"])
    col_v3.metric("Duplicate IDs", val_report["duplicate_ids"])
    
    st.markdown("---")
    st.subheader("Data Dictionary")
    data_dict_df = generate_data_dictionary(df_raw)
    st.dataframe(data_dict_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Raw Dataset Preview")
    st.dataframe(df_raw, use_container_width=True)
