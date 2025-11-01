import re

def normalize_text(text):
    text = text.lower()
    return re.sub(r"[^a-z0-9\\s]+", " ", text)

def extract_skills_from_text(text, skills_list):
    """Return list of skills found in the text."""
    if not skills_list: 
        return []
    text_norm = normalize_text(text)
    return sorted([s for s in skills_list if re.search(rf"\\b{s.lower()}\\b", text_norm)])

def compute_skill_overlap(resume_skills, jd_skills):
    """Return overlap ratio between resume and JD skills."""
    if not jd_skills: 
        return 0.0
    inter = set(rs.lower() for rs in resume_skills) & set(jd_skills)
    return len(inter) / len(jd_skills)
