import logging
import re
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util
from app.core.config import settings
from app.services.insights import extract_skills

logger = logging.getLogger(__name__)

# Load Sentence-BERT model once during startup
logger.info(f"Loading SentenceTransformer model: {settings.MODEL_NAME}")
model = SentenceTransformer(settings.MODEL_NAME)

def split_into_sentences(text: str) -> List[str]:
    # Clean up excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Split by sentence terminators or bullet points
    sentences = re.split(r'(?<=[.!?]) +|•|\u2022|- ', text)
    
    valid_sentences = []
    for s in sentences:
        s = s.strip()
        word_count = len(s.split())
        # Filter: keep only concise technical signals (5 to 35 words)
        if 5 <= word_count <= 35:
            valid_sentences.append(s)
    return valid_sentences

def compute_similarity(job_text: str, resumes: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    if not resumes:
        return []

    # Encode job description
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    results = []
    
    for r in resumes:
        resume_text = r["text"]
        sentences = split_into_sentences(resume_text)
        
        # If the resume is too short or couldn't be parsed
        if not sentences:
            results.append({
                "filename": r["filename"],
                "score": 0.0,
                "summary": "• Could not extract sufficient technical signals.",
                "skills": []
            })
            continue
            
        # Encode all sentences of the resume
        sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
        
        # Compute similarities of each sentence against the job description
        scores = util.cos_sim(job_embedding, sentence_embeddings)[0]
        
        # The overall score is the average of the top 3 most relevant sentences
        top_k = min(5, len(scores))
        top_scores, top_indices = scores.topk(top_k)
        
        overall_score = float(top_scores.mean())
        
        # Generate concise recruiter summary (top 2-3 signals)
        summary_k = min(3, len(top_indices))
        summary_sentences = [sentences[idx] for idx in top_indices[:summary_k]]
        
        clean_summary_lines = []
        for s in summary_sentences:
            s = s.strip().capitalize()
            # Ensure it ends with punctuation
            if not s.endswith('.'):
                s += '.'
            # Truncate if it's too long
            if len(s) > 130:
                s = s[:127].rsplit(' ', 1)[0] + "..."
            clean_summary_lines.append(f"• {s}")
            
        summary = "\n".join(clean_summary_lines)
        if not summary:
            summary = "• No highly relevant highlights found."
            
        # Extract skills
        skills = extract_skills(resume_text)
        
        results.append({
            "filename": r["filename"],
            "score": overall_score,
            "summary": summary,
            "skills": skills
        })

    # Sort highest match first
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results
