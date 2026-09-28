import json
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import RAG_INDEX_PATH, RAG_TOP_K
from src.utils.logging_utils import get_logger

logger = get_logger("rag_retriever")

_cached_index_store = None
_cached_vectorizer = None

def load_vector_index():
    """Lazy loader and deserializer for RAG index store and TF-IDF vectorizer."""
    global _cached_index_store, _cached_vectorizer
    if _cached_index_store is None:
        if not RAG_INDEX_PATH.exists():
            logger.info("RAG index file not found. Building index automatically...")
            from src.rag.ingest import build_and_save_vector_index
            _cached_index_store = build_and_save_vector_index()
        else:
            with open(RAG_INDEX_PATH, "r", encoding="utf-8") as f:
                _cached_index_store = json.load(f)
                
        # Reconstruct TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        vectorizer.vocabulary_ = _cached_index_store["vocabulary"]
        vectorizer.idf_ = np.array(_cached_index_store["idf"])
        _cached_vectorizer = vectorizer
        
    return _cached_index_store, _cached_vectorizer

def retrieve_relevant_knowledge(query: str, top_k: int = RAG_TOP_K) -> List[Dict[str, Any]]:
    """
    Queries vector index and retrieves top-k relevant educational strategy chunks with source metadata.
    
    Args:
        query: Search query describing student risk factors or academic situation.
        top_k: Number of relevant chunks to retrieve.
        
    Returns:
        List of dicts containing score, category, document_title, section_heading, source_file, and content.
    """
    index_store, vectorizer = load_vector_index()
    chunks = index_store["chunks"]
    tfidf_matrix = np.array(index_store["tfidf_matrix"])
    
    # Vectorize query
    query_vec = vectorizer.transform([query]).toarray()
    
    # Calculate Cosine Similarities
    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]
    
    # Get top-k indices
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        score = float(similarities[idx])
        chunk_info = chunks[idx].copy()
        chunk_info["relevance_score"] = round(score, 4)
        results.append(chunk_info)
        
    logger.info(f"Retrieved {len(results)} chunks for query: '{query[:40]}...'")
    return results

def build_query_from_student_profile(risk_level: str, feature_values: Dict[str, float], top_risk_drivers: List[str]) -> str:
    """
    Builds an optimized search query string based on a student's risk profile and weak areas.
    """
    query_parts = [f"Student academic risk level: {risk_level}"]
    
    if feature_values.get("attendance_percentage", 100) < 75:
        query_parts.append("attendance habit building lecture engagement absenteeism")
    if feature_values.get("assignment_average", 100) < 60:
        query_parts.append("assignment performance coursework submission study schedule")
    if feature_values.get("exam_average", 100) < 60 or feature_values.get("internal_marks", 100) < 60:
        query_parts.append("exam recovery revision active recall test preparation")
    if feature_values.get("study_hours_per_week", 20) < 10:
        query_parts.append("time management study hours planning deep work routines")
    if feature_values.get("participation_score", 100) < 50:
        query_parts.append("class participation peer study group active learning")

    if top_risk_drivers:
        query_parts.extend(top_risk_drivers)
        
    return " ".join(query_parts)
