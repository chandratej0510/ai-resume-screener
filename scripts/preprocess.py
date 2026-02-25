# scripts/preprocess.py

import re
import string

def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - Lowercasing
    - Removing numbers
    - Removing punctuation
    - Collapsing extra spaces
    """
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


if __name__ == "__main__":
    sample = "I worked on 3 ML projects in 2024!! "
    print("Original:", sample)
    print("Cleaned :", clean_text(sample))
