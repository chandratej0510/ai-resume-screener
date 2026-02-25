# scripts/load_and_clean.py

import os
import sys

# --- FIX: Ensure the project root (ai-resume-screener) is in the Python path ---
# This makes "from scripts.preprocess import clean_text" work from any location
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now the import will succeed
from scripts.preprocess import clean_text

# --- Define data paths ---
BASE_DIR = PROJECT_ROOT
RESUME_DIR = os.path.join(BASE_DIR, "data", "resumes")
JD_DIR = os.path.join(BASE_DIR, "data", "job_descriptions")

def load_texts(folder_path):
    """
    Load all .txt files from a folder, clean them, and return names, raw, and cleaned text lists.
    """
    names, raw, cleaned = [], [], []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            names.append(filename)
            raw.append(text)
            cleaned.append(clean_text(text))
    return names, raw, cleaned


if __name__ == "__main__":
    # --- Load and print resumes ---
    res_names, res_raw, res_clean = load_texts(RESUME_DIR)
    print("📄 Resumes found:", res_names)
    if res_names:
        print("\nRaw text (first resume):\n", res_raw[0][:200])
        print("\nCleaned text:\n", res_clean[0][:200])

    # --- Load and print job descriptions ---
    jd_names, jd_raw, jd_clean = load_texts(JD_DIR)
    print("\n📝 Job descriptions found:", jd_names)
    if jd_names:
        print("\nRaw JD (first):\n", jd_raw[0][:200])
        print("\nCleaned JD:\n", jd_clean[0][:200])
