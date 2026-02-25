# backend/model_utils.py

from sentence_transformers import SentenceTransformer, util

# Load Sentence-BERT model once (fast, cached)
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(job_text: str, resumes: list[str]):
    """
    Given a job description and a list of resume texts,
    return resume names + similarity scores sorted by best match.
    """
    # Encode job description
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    # Encode all resumes
    resume_embeddings = model.encode(resumes, convert_to_tensor=True)

    # Compute cosine similarity
    scores = util.cos_sim(job_embedding, resume_embeddings)[0]

    # Convert tensor scores to Python floats
    results = [
        {"index": i, "score": float(score)}
        for i, score in enumerate(scores)
    ]

    # Sort highest match first
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results
