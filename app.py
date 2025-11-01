import streamlit as st
import pandas as pd
from utils.text_extraction import extract_text
from utils.skill_extraction import extract_skills_from_text, compute_skill_overlap
from utils.scoring import compute_similarity_and_scores
from models.embeddings import load_model

# --- Page Setup ---
st.set_page_config(page_title="Automated Resume Shortlisting", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        .main-container {
        padding: 2rem;
        background-color: var(--background-color);  /* matches theme */
        color: var(--text-color);                   /* matches theme */
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .result-card {
        padding: 1.2rem;
        border-radius: 12px;
        background-color: var(--secondary-background-color); /* matches theme */
        color: var(--text-color);
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

        .stButton>button {
         background: linear-gradient(90deg, #4a90e2, #357ab8);
         color: white;
         font-weight: 600;
         border-radius: 10px;
         padding: 0.6em 1.5em;
         border: none;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #357ab8, #2d6ca4);
        }
        .result-card {
            padding: 1.2rem;
            border-radius: 12px;
            background-color: white;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }
        .candidate-name {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    semantic_weight = st.slider("Semantic Weight", 0.0, 1.0, 0.7)
    skill_weight = 1.0 - semantic_weight
    st.caption("Adjust importance between semantic similarity and skills.")

# --- Main UI ---
st.title("📄 Automated Resume Shortlisting System")
st.markdown("#### Streamlined recruitment using NLP & Machine Learning")

with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Layout: 2 columns
    col1, col2 = st.columns(2)

    with col1:
        jd_text = st.text_area("📝 Paste Job Description", height=250)

    with col2:
        uploaded_resumes = st.file_uploader(
            "📂 Upload Resumes",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )

    custom_skills = st.text_input("🎯 Custom Skills (comma-separated)", "")
    skills_list = [s.strip() for s in custom_skills.split(",") if s.strip()] or None

    # Load model
    model = load_model()

    # Action button
    if st.button("🚀 Process and Rank", use_container_width=True):
        if not jd_text or not uploaded_resumes:
            st.error("⚠️ Please provide a Job Description and at least one Resume.")
        else:
            with st.spinner("🔍 Analyzing resumes..."):
                df = compute_similarity_and_scores(
                    jd_text, uploaded_resumes, model, skills_list, semantic_weight, skill_weight
                )

            st.success("✅ Ranking complete!")
            st.subheader("📊 Ranked Results (Table View)")
            st.dataframe(
                df.style.background_gradient(
                    cmap="Blues", subset=["combined_score"]
                ).format({
                    "semantic_similarity": "{:.3f}",
                    "skill_overlap": "{:.3f}",
                    "combined_score": "{:.3f}"
                })
            )

            # --- Candidate Profile Cards ---
            st.subheader("👤 Candidate Profiles")
            for _, row in df.iterrows():
                with st.container():
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    
                    # Candidate Name (use resume filename if available)
                    st.markdown(f"<div class='candidate-name'>📛 {row.get('resume_name', 'Unknown Candidate')}</div>", unsafe_allow_html=True)
                    
                    # Scores with progress bars
                    st.write("**Semantic Similarity**")
                    st.progress(float(row["semantic_similarity"]))
                    
                    st.write("**Skill Overlap**")
                    st.progress(float(row["skill_overlap"]))
                    
                    st.write("**Overall Combined Score**")
                    st.progress(float(row["combined_score"]))
                    
                    # Skills matched (if present in DF)
                    if "matched_skills" in row and isinstance(row["matched_skills"], list):
                        st.write("**Matched Skills:**", ", ".join(row["matched_skills"]))
                    
                    st.markdown('</div>', unsafe_allow_html=True)

            # --- Download button ---
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Results as CSV",
                csv,
                "resume_ranking.csv",
                "text/csv",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
