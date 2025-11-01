import spacy
import nltk

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample skills list (you can expand this)
SKILLS = [
    "python", "java", "c++", "sql", "nlp", "machine learning", "deep learning",
    "tensorflow", "pytorch", "transformers", "spacy", "nltk", "react", "docker", "aws"
]

def extract_skills(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc]

    found_skills = []
    for skill in SKILLS:
        if skill.lower() in tokens or skill.lower() in text.lower():
            found_skills.append(skill)
    return list(set(found_skills))
