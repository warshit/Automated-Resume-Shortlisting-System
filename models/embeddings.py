from sentence_transformers import SentenceTransformer, util

def load_model(model_name="all-MiniLM-L6-v2"):
    return SentenceTransformer(model_name, device="cpu")

def compute_similarity(job_desc, resume_text, model):
    embeddings = model.encode([job_desc, resume_text], convert_to_tensor=True)
    return float(util.cos_sim(embeddings[0], embeddings[1]))
