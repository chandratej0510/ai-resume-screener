# scripts/match.py

import os
import sys
from sentence_transformers import SentenceTransformer, util

# --- Add project root to system path ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --- Import the loader/cleaner ---
from scripts.load_and_clean import load_texts, RESUME_DIR, JD_DIR

# -------------------------------------------------------------------
# 🧠 Step 1. Load pre-trained Sentence-BERT model
# -------------------------------------------------------------------
"""
Concept:
A SentenceTransformer (BERT-based) converts text into a dense vector (embedding).
Similar meanings → similar vectors in high-dimensional space.
"""
model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------------------------------------------------
# 🧾 Step 2. Load and clean text data
# -------------------------------------------------------------------
jd_names, jd_raw, jd_clean = load_texts(JD_DIR)
res_names, res_raw, res_clean = load_texts(RESUME_DIR)

# We'll use the first job description for now
job_text = jd_clean[0]

print(f"🧾 Matching resumes for job description: {jd_names[0]}")
print("-" * 70)
print(job_text[:200], "...\n")

# -------------------------------------------------------------------
# 🧮 Step 3. Encode job + resumes into embeddings
# -------------------------------------------------------------------
"""
Concept:
Each text is transformed into a 384-dimensional vector that captures semantic meaning.
The model.encode() converts each document (string) → embedding (list of floats).
"""
job_embedding = model.encode(job_text, convert_to_tensor=True)
resume_embeddings = model.encode(res_clean, convert_to_tensor=True)

# -------------------------------------------------------------------
# 📈 Step 4. Compute cosine similarity
# -------------------------------------------------------------------
"""
Concept:
Cosine similarity measures the angle between two vectors.
1 → identical meaning, 0 → no similarity, -1 → opposite meaning.
"""
scores = util.cos_sim(job_embedding, resume_embeddings)[0]

# -------------------------------------------------------------------
# 🏆 Step 5. Rank and print results
# -------------------------------------------------------------------
"""
We zip names + scores, sort them descending (highest match first).
"""
ranked = sorted(
    zip(res_names, scores),
    key=lambda x: float(x[1]),
    reverse=True
)

print("🏆 Resume Ranking based on Similarity:\n")
for name, score in ranked:
    print(f"{name:20s} → similarity score = {float(score):.4f}")

# -------------------------------------------------------------------
# 💡 Step 6. Interpretation
# -------------------------------------------------------------------
"""
A higher similarity score means the resume content is semantically
closer to the job description (uses similar terms & concepts).
"""
best_match = ranked[0]
print("\n✅ Best Match:", best_match[0], "with score =", float(best_match[1]))
