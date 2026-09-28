# StudentSense AI 🎓

> **Student Behavior Prediction & Personalized Recommendation System**  
> An intelligent decision-support application combining Machine Learning Risk Classification (scikit-learn), Explainable AI (SHAP), Knowledge Base RAG (Vector Indexing), Generative AI (Google Gemini + Offline Fallback), and an Interactive Streamlit Dashboard.

---

## 📌 Features & Key Capabilities

- **ML Risk Classification**: Predicts student academic risk levels (`Low`, `Medium`, `High`) with class probabilities.
- **Explainable AI (SHAP)**: Provides local feature importance (waterfall directional contribution) and global feature importance.
- **Curated Knowledge Base & RAG**: Splits educational strategy markdown files into chunks and indexes them using a persistent TF-IDF Cosine Similarity Vector Store.
- **Generative AI Recommendations**: Combines student profile, SHAP risk drivers, and retrieved knowledge chunks to produce grounded, actionable recommendations (supports Google Gemini API & dual-mode offline engine).
- **Interactive Streamlit Dashboard**: 5-page interactive UI featuring student risk lookups, what-if simulations, SHAP bar charts, RAG source inspection, class-level analytics, and dataset data dictionaries.

---

## 🏗 System Architecture

```
Student Data CSV ──> Data Validation & Preprocessing ──> ML Classification Model ──> SHAP Explainer
                                                                                         │
                                                                                         ▼
Streamlit Dashboard <── Generative AI Engine <── RAG Knowledge Retriever <── Vector Index Store
```

---

## 📁 Repository Directory Structure

```
StudentSense-AI/
├── README.md                          # Complete build & user guide
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Repository gitignore rules
├── app.py                             # Interactive Streamlit dashboard
├── config.py                          # Central settings, schemas, and paths
├── data/
│   ├── raw/
│   │   └── student_data.csv           # Raw dataset (250 student records)
│   ├── processed/                     # Preprocessed data directory
│   └── sample/                        # Sample data snapshots
├── models/
│   ├── trained_model/                 # Saved ML model (.joblib)
│   ├── preprocessor/                  # Saved ColumnTransformer pipeline (.joblib)
│   └── model_metadata.json            # Model evaluation metrics & timestamp
├── notebooks/                         # Exploration & analysis Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_shap_analysis.ipynb
├── src/
│   ├── data/
│   │   ├── load_data.py               # Raw CSV loader
│   │   ├── validate.py               # Schema & range validator
│   │   └── preprocess.py             # Feature scaling & train/test split
│   ├── ml/
│   │   ├── train.py                  # Model training & selection script
│   │   ├── predict.py                # Prediction & inference API
│   │   └── evaluate.py               # Classification metrics calculator
│   ├── xai/
│   │   └── shap_explainer.py         # SHAP local/global explainer
│   ├── rag/
│   │   ├── ingest.py                 # Document chunking & vector indexing
│   │   ├── retriever.py              # Top-k vector retriever
│   │   └── prompt_builder.py         # Structured prompt builder
│   ├── genai/
│   │   └── recommender.py            # Gemini API & offline recommendation engine
│   └── utils/
│       └── logging_utils.py          # Structured logging module
├── knowledge_base/                    # Curated educational strategy documents
│   ├── academic_support/
│   ├── study_skills/
│   ├── attendance/
│   └── mentoring/
└── tests/                             # Automated pytest suite
    ├── test_data.py
    ├── test_model.py
    ├── test_xai.py
    └── test_rag.py
```

---

## 🚀 Quick Start & Installation

### 1. Clone & Setup Environment
```bash
# Clone repository or navigate to directory
cd "c:\first project"

# Install Python requirements
python -m pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env` to supply a Google Gemini API key if live LLM generation is desired:
```bash
cp .env.example .env
```
*(If no API key is provided, StudentSense AI automatically operates in Rule-Grounded Offline Mode with 100% functionality).*

### 3. Generate Data & Train Model
```bash
# Generate sample student dataset (250 records)
python scripts/generate_sample_data.py

# Train classification model and save artifacts
python -m src.ml.train

# Build RAG knowledge base vector index
python -m src.rag.ingest
```

### 4. Launch Streamlit Web Dashboard
```bash
streamlit run app.py
```

---

## 🧪 Running Automated Tests

Run the complete test suite using `pytest`:
```bash
python -m pytest tests/
```

---

## 🔒 Responsible AI & Decision Support Notice

StudentSense AI is designed exclusively as an **educator decision-support tool**. Predicted risk levels represent statistical model outputs based on historical indicators and should **never** be used as the sole basis for disciplinary actions, academic penalties, or high-stakes institutional decisions. Human review by qualified academic advisors is required for all interventions.
