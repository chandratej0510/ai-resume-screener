import re
from typing import List

# A basic heuristic list of common tech skills to look out for
COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust",
    "angular", "react", "vue", "node.js", "express", "django", "flask", "fastapi",
    "spring", "docker", "kubernetes", "aws", "gcp", "azure", "sql", "mysql",
    "postgresql", "mongodb", "redis", "elasticsearch", "machine learning",
    "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "git", "ci/cd", "agile", "scrum",
    "html", "css", "sass", "graphql", "rest api", "linux", "bash"
}

def extract_skills(text: str) -> List[str]:
    """
    Extract skills from the resume text using a predefined dictionary
    and a capitalized word heuristic.
    """
    found_skills = set()
    text_lower = text.lower()
    
    # 1. Match against predefined common skills
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill.title() if len(skill) > 3 else skill.upper())
            
    # 2. Extract capitalized phrases (e.g., "Data Science", "Project Management")
    # This is a basic heuristic for finding proper nouns that might be skills
    capitalized_phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    for phrase in capitalized_phrases:
        if len(phrase) > 5 and len(phrase.split()) <= 3:
            # Filter out generic words
            if phrase.lower() not in {"resume", "education", "experience", "projects", "skills", "summary", "university", "college", "bachelor", "master", "phd"}:
                found_skills.add(phrase)

    # Return top 10 unique skills to keep the UI clean
    return sorted(list(found_skills))[:10]
