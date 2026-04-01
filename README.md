# JobMind AI

JobMind AI is a fully local, privacy-first AI application that lets users upload their resume (PDF) + a job description (PDF or text), then instantly:

- Analyzes how well the resume matches the job (with a match score %).
- Highlights missing skills, experience gaps, and strong points.
- Generates a customized cover letter tailored to the job.
- Answers any follow-up questions about the documents (e.g., “What should I improve in my resume?” or “Explain this requirement from the JD”).

## Architecture diagram

## Tech Stack

- Python 3.10+
- LangChain (or LlamaIndex) – for the entire RAG pipeline
- Ollama + Llama 3.2 or Mistral (small & fast local LLM)
- Chroma (vector database – simple and local)
- FastEmbed or sentence-transformers (embeddings)
- Streamlit (beautiful web UI in <100 lines)
- PyPDF2 + LangChain loaders (document handling)

## 🤝 Contributing

Pull requests and ideas are welcome.

## Author

- Bilal Shaikh
- Github:- [https://github.com/bilalshaikh-code](https://github.com/bilalshaikh-code)
