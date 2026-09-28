import json
import re
from pathlib import Path
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer

from config import KNOWLEDGE_BASE_DIR, RAG_INDEX_PATH, RAG_CHUNK_SIZE, RAG_CHUNK_OVERLAP
from src.utils.logging_utils import get_logger

logger = get_logger("rag_ingest")

def chunk_markdown_file(file_path: Path, chunk_size: int = RAG_CHUNK_SIZE, overlap: int = RAG_CHUNK_OVERLAP) -> List[Dict[str, Any]]:
    """
    Parses a markdown file into semantic chunks using heading sections and sliding windows.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    category = file_path.parent.name
    doc_title = file_path.stem.replace("_", " ").title()
    
    # Split text by sections (Markdown headers)
    sections = re.split(r'\n(?=##?\s+)', text)
    chunks = []
    
    chunk_counter = 1
    for sec in sections:
        sec_text = sec.strip()
        if not sec_text:
            continue
            
        # Extract section heading if present
        heading_match = re.match(r'^(##?\s+[^\n]+)', sec_text)
        section_heading = heading_match.group(1).strip("# ").strip() if heading_match else "General Guidance"
        
        words = sec_text.split()
        if len(words) <= chunk_size:
            chunks.append({
                "chunk_id": f"{file_path.stem}_c{chunk_counter}",
                "category": category,
                "document_title": doc_title,
                "section_heading": section_heading,
                "source_file": file_path.name,
                "content": sec_text
            })
            chunk_counter += 1
        else:
            # Sub-chunk long sections using word windowing
            start = 0
            while start < len(words):
                end = min(start + chunk_size, len(words))
                chunk_words = words[start:end]
                sub_text = " ".join(chunk_words)
                chunks.append({
                    "chunk_id": f"{file_path.stem}_c{chunk_counter}",
                    "category": category,
                    "document_title": doc_title,
                    "section_heading": section_heading,
                    "source_file": file_path.name,
                    "content": sub_text
                })
                chunk_counter += 1
                if end == len(words):
                    break
                start += (chunk_size - overlap)
                
    return chunks

def build_and_save_vector_index() -> Dict[str, Any]:
    """
    Loads markdown documents from knowledge_base, chunks them, computes TF-IDF embeddings,
    and persists index store JSON file to disk.
    """
    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(f"Knowledge base directory missing at '{KNOWLEDGE_BASE_DIR}'")
        
    md_files = list(KNOWLEDGE_BASE_DIR.rglob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No markdown documents found in '{KNOWLEDGE_BASE_DIR}'")
        
    logger.info(f"Found {len(md_files)} knowledge base documents. Starting ingestion...")
    
    all_chunks = []
    for filepath in md_files:
        file_chunks = chunk_markdown_file(filepath)
        all_chunks.extend(file_chunks)
        
    logger.info(f"Total chunks extracted: {len(all_chunks)}")
    
    corpus = [c["content"] for c in all_chunks]
    
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    index_store = {
        "chunks": all_chunks,
        "vocabulary": vectorizer.vocabulary_,
        "idf": vectorizer.idf_.tolist(),
        "tfidf_matrix": tfidf_matrix.toarray().tolist(),
        "total_chunks": len(all_chunks)
    }
    
    RAG_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RAG_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_store, f, indent=2)
        
    logger.info(f"RAG Vector Index successfully persisted to '{RAG_INDEX_PATH}'")
    return index_store

if __name__ == "__main__":
    build_and_save_vector_index()
