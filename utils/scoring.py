import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.text_extraction import extract_text
from utils.skill_extraction import extract_skills_from_text, compute_skill_overlap

def compute_similarity_and_scores(jd_text, uploaded_resumes, model, skills_list, semantic_weight, skill_weight):
    """Compute semantic similarity + skill overlap scores for resumes."""
    jd_skills = extract_skills_from_text(jd_text, skills_list or [])
    jd_emb = model.encode([jd_text])[0]

    data = []
    for f in uploaded_resumes:
        resume_text = extract_text(f)
        resume_skills = extract_skills_from_text(resume_text, skills_list or [])
        sim = cosine_similarity([jd_emb], model.encode([resume_text]))[0][0]
        overlap = compute_skill_overlap(resume_skills, jd_skills)
        combined = semantic_weight * sim + skill_weight * overlap
        data.append({
            "resume_name": f.name,
            "semantic_similarity": sim,
            "skill_overlap": overlap,
            "combined_score": combined,
            "extracted_skills": ", ".join(resume_skills)
        })

    return pd.DataFrame(data).sort_values(by="combined_score", ascending=False).reset_index(drop=True)
