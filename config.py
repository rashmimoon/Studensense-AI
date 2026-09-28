import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Directory Paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

MODELS_DIR = BASE_DIR / "models"
TRAINED_MODEL_DIR = MODELS_DIR / "trained_model"
PREPROCESSOR_DIR = MODELS_DIR / "preprocessor"
MODEL_METADATA_PATH = MODELS_DIR / "model_metadata.json"

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
RAG_INDEX_PATH = BASE_DIR / "src" / "rag" / "index_store.json"

# File Paths
RAW_DATA_PATH = RAW_DATA_DIR / "student_data.csv"
MODEL_FILE_PATH = TRAINED_MODEL_DIR / "student_risk_model.joblib"
PREPROCESSOR_FILE_PATH = PREPROCESSOR_DIR / "preprocessor.joblib"

# Dataset Schema Definition
ID_COLUMN = "student_id"
TARGET_COLUMN = "risk_level"

FEATURE_COLUMNS = [
    "attendance_percentage",
    "assignment_average",
    "internal_marks",
    "exam_average",
    "study_hours_per_week",
    "participation_score",
    "previous_semester_score",
]

# Human-readable Feature Names for SHAP & Dashboard UI
HUMAN_READABLE_FEATURES = {
    "attendance_percentage": "Attendance Rate (%)",
    "assignment_average": "Assignment Performance (%)",
    "internal_marks": "Internal Assessment Marks (%)",
    "exam_average": "Final Exam Performance (%)",
    "study_hours_per_week": "Weekly Study Hours",
    "participation_score": "Class Participation Score",
    "previous_semester_score": "Previous Semester Score (%)",
}

# Target Labels
RISK_LEVELS = ["Low", "Medium", "High"]

# Model Hyperparameters
RANDOM_SEED = 42
TEST_SIZE = 0.2

# RAG Configuration
RAG_TOP_K = 3
RAG_CHUNK_SIZE = 300
RAG_CHUNK_OVERLAP = 50

# GenAI Config
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
