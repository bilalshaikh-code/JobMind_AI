# JobMind AI

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B?style=flat-square&logo=streamlit)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-9B59B6?style=flat-square)

JobMind AI is a fully local, privacy-first AI application that lets users upload their resume (PDF) + a job description (PDF or text), then instantly:

- Analyzes how well the resume matches the job (with a match score %).
- Highlights missing skills, experience gaps, and strong points.
- Generates a customized cover letter tailored to the job.
- Answers any follow-up questions about the documents (e.g., “What should I improve in my resume?” or “Explain this requirement from the JD”).

---

## Key Features

- **Smart Match Scoring** — Semantic + keyword-based match percentage between resume and job description
- **Detailed Gap Analysis** — Identifies missing skills, experience gaps, and improvement areas
- **Actionable Suggestions** — AI-generated bullet points tailored to your experience and the target job
- **Custom Cover Letter Generation** — Professional, personalized cover letters with one-click download
- **Evidence Highlighting** — Shows exactly which parts of your resume and JD were used for each suggestion
- **Interactive Chat** — Ask anything about your resume or the job description
- **Visual Dashboard** — Match score gauge, skill radar charts, and gap visualizations
- **Fully Local & Private** – Everything runs on your machine (no data leaves your PC)
- **Modern Modular Architecture** – Clean, maintainable code structure

---

## Architecture diagram

JobMind AI uses a **modern Retrieval-Augmented Generation (RAG)** pipeline:

1. Document Ingestion & Chunking
2. Embedding Generation
3. Vector Storage (Chroma)
4. Hybrid Retrieval + Reranking
5. Prompt Engineering with multiple specialized agents
6. Response Generation with source citations

---

## Tech Stack

- **Language**: Python 3.10+
- **AI Framework**: LangChain
- **LLM**: Ollama (llama3.2:1b)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace Sentence Transformers
- **Frontend**: Streamlit
- **Document Processing**: PyPDF2 + LangChain loaders
- **Visualization**: Streamlit components

---

## Option 1: Setup with Docker (Recommended)

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 2. Build and Start
Open your terminal in the project root and run:
```bash
docker-compose up --build -d
```

### 3. Initialize the LLM
Because the Docker container starts with a fresh Ollama instance, you must pull the model manually the first time:
```bash
docker exec -it <YOUR_CONTAINER_ID> ollama pull llama3.2:1b
```

### 4. Access the App
Open your browser to: **`http://localhost:8501`**

---

## Option 2: Setup without Docker (Local Python)

### 1. Prerequisites
* **Python 3.11 or 3.12** (Avoid 3.14 for now due to library compatibility).
* [Ollama](https://ollama.com/) installed and running on your machine.

### 2. Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare the Model
Ensure Ollama is running and download the model:
```bash
ollama pull llama3.2:1b
```

### 5. Run the App
```bash
streamlit run app.py
```
Open your browser to: **`http://localhost:8501`**

---

## 🛠️ Configuration Note
The application is designed to be flexible. It looks for the Ollama URL in an environment variable:

* **In Docker:** It automatically uses `http://ollama:11434`.
* **In Local:** It defaults to `http://localhost:11434`.

> **Note for Developers:** If you change the model in `rag_pipeline.py`, ensure you update the `ollama pull` command in the steps above to match the new model name.

---

## Usage Guide

- Upload your Resume (PDF) and Job Description (PDF or text)
- Click Analyze to get instant match score and insights
- Explore tabs: Dashboard, Gap Analysis, Suggestions, Cover Letter, Interview Prep
- Use the chat interface for follow-up questions
- Download Full Report as PDF

---

## What Makes JobMind AI Unique

- Fully local & private — no data leaves your computer
- Combines semantic understanding with rule-based ATS checks (Future implement)
- Provides actionable outputs (not just analysis)
- Supports multiple resume versions and persona-based analysis (Future implement)
- Production-ready code structure with modular design

---

## Future Improvements

- Bulk job application analysis
- Integration with LinkedIn export
- ATS compatibility scoring
- Visual skill radar charts
- Export full report as PDF
- Chat history persistence

---

## ⚖️ License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Author

- Bilal Shaikh
- Github:- [https://github.com/bilalshaikh-code](https://github.com/bilalshaikh-code)
