from typing import Dict, Any, List
import os
import time

from config import LLM_API_KEY, LLM_MODEL
from src.rag.prompt_builder import construct_recommendation_prompt
from src.utils.logging_utils import get_logger

logger = get_logger("genai_recommender")

def generate_offline_grounded_recommendation(
    student_id: str,
    risk_level: str,
    feature_values: Dict[str, float],
    shap_factors: Dict[str, Any],
    retrieved_chunks: List[Dict[str, Any]]
) -> str:
    """
    Generates a structured, high-quality recommendation grounded in RAG chunks 
    when operating offline or when LLM API keys are omitted.
    """
    top_drivers = shap_factors.get("top_risk_drivers", [])
    
    # Identify key weak areas
    weaknesses = []
    if feature_values.get("attendance_percentage", 100) < 75:
        weaknesses.append(f"Attendance Rate ({feature_values.get('attendance_percentage')}%) is below 75% threshold.")
    if feature_values.get("assignment_average", 100) < 60:
        weaknesses.append(f"Assignment Performance ({feature_values.get('assignment_average')}%) requires recovery.")
    if feature_values.get("exam_average", 100) < 60:
        weaknesses.append(f"Exam Average ({feature_values.get('exam_average')}%) shows academic risk.")
    if feature_values.get("study_hours_per_week", 20) < 10:
        weaknesses.append(f"Weekly Study Hours ({feature_values.get('study_hours_per_week')} hrs) indicate study habit gaps.")

    focus = weaknesses[0] if weaknesses else "Overall academic consistency and exam strategy."

    # Extract practical actions from retrieved chunks
    action_steps = []
    sources_ref = []
    for idx, chunk in enumerate(retrieved_chunks, 1):
        sources_ref.append(f"- **[{chunk['document_title']}]** - *{chunk['section_heading']}* (`{chunk['source_file']}`)")
        # Extract bullet points from chunk content
        lines = chunk['content'].split('\n')
        for line in lines:
            if line.strip().startswith('-') or line.strip().startswith('*'):
                cleaned_line = line.strip().lstrip('-* ').strip()
                if cleaned_line and cleaned_line not in action_steps and len(action_steps) < 5:
                    action_steps.append(cleaned_line)

    if not action_steps:
        action_steps = [
            "Establish a dedicated weekly study schedule dividing work into 90-minute focused blocks.",
            "Schedule weekly office hours check-ins with subject instructors to review weak course concepts.",
            "Form peer study groups to practice past examination papers under timed conditions.",
            "Set attendance alerts and non-negotiable daily routines to maintain >75% class participation."
        ]

    formatted_actions = "\n".join([f"{i+1}. {act}" for i, act in enumerate(action_steps[:5])])
    formatted_sources = "\n".join(sources_ref) if sources_ref else "- Grounded Knowledge Base Documents"

    rec_md = f"""### 1. Situation Summary
Student **{student_id}** is evaluated at **{risk_level.upper()} ACADEMIC RISK**. The primary model risk indicators highlight {focus}

### 2. Primary Support Focus
**Immediate Priority:** Focus on improving {focus.lower()} and establishing structured study routines grounded in institutional support strategies.

### 3. Actionable Intervention Steps
{formatted_actions}

### 4. Recommended Follow-up Schedule
- **Bi-Weekly Progress Check:** Meet with assigned academic mentor every 14 days.
- **Monthly Milestone:** Re-evaluate internal assessment grades and attendance logs after 30 days.

### 5. Knowledge Base Sources Referenced
{formatted_sources}
"""
    return rec_md

def generate_personalized_recommendation(
    student_id: str,
    risk_level: str,
    probabilities: Dict[str, float],
    feature_values: Dict[str, float],
    shap_factors: Dict[str, Any],
    retrieved_chunks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generates personalized recommendations using Gemini GenAI SDK if API key is present,
    or falls back gracefully to rule-grounded offline engine.
    """
    prompt = construct_recommendation_prompt(
        student_id, risk_level, probabilities, feature_values, shap_factors, retrieved_chunks
    )
    
    api_key = LLM_API_KEY or os.getenv("GEMINI_API_KEY")
    
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            logger.info("Attempting GenAI recommendation generation via Gemini API...")
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=LLM_MODEL,
                contents=prompt
            )
            if response and response.text:
                return {
                    "recommendation_text": response.text,
                    "mode": "Live LLM (Google Gemini)",
                    "is_fallback": False,
                    "sources": retrieved_chunks
                }
        except Exception as e:
            logger.warning(f"GenAI API call failed or timed out ({e}). Switching to offline grounded fallback.")

    # Offline Grounded Fallback Mode
    logger.info("Using offline grounded recommendation engine.")
    fallback_text = generate_offline_grounded_recommendation(
        student_id, risk_level, feature_values, shap_factors, retrieved_chunks
    )
    
    return {
        "recommendation_text": fallback_text,
        "mode": "Rule-Grounded Knowledge Engine (Offline Mode)",
        "is_fallback": True,
        "sources": retrieved_chunks
    }
