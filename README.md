# Automated Resume Shortlisting System

Short: A Streamlit app that ranks uploaded resumes against a pasted Job Description using semantic embeddings + skill overlap.

## Quick start (Windows PowerShell)

1. (Optional) Create & activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Fix `requirements.txt` if it contains invalid lines (remove stray text like `(rerun without)`).

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Run the app:
   ```powershell
   python -m streamlit run app.py
   ```

If `streamlit` CLI is not on PATH, use the `python -m streamlit` form or add your Python Scripts folder (e.g. `C:\Users\varsh\AppData\Roaming\Python\Python312\Scripts`) to PATH.

## What it does (brief)

- Inputs: Job Description (paste), multiple resumes (pdf/docx/txt), optional custom skills.
- Processing:
  - Extracts text from resumes.
  - Extracts skills and computes skill overlap with JD/custom skills.
  - Encodes JD and resumes with an embedding model and computes semantic similarity.
  - Computes a weighted combined score (semantic vs skill).
- Outputs: Ranked table, candidate cards, downloadable CSV.

## Key files

- `app.py` — Streamlit UI and orchestration.
- `utils/text_extraction.py` — resume parsing (PDF/DOCX/TXT).
- `utils/skill_extraction.py` — skill extraction and matching.
- `utils/scoring.py` — score computation and ranking logic.
- `models/embeddings.py` — loading embedding model.

## Troubleshooting

- streamlit not recognized: run `python -m streamlit run app.py` or add Scripts folder to PATH.
- Invalid `requirements.txt`: open the file and remove any non-dependency lines.
- Missing parsing libs: install `python-docx`, `PyPDF2`, etc., as needed.


