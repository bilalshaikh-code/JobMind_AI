import streamlit as st
import os
from core.rag_pipeline import RAGPipeline
from core.analyzer import Analyzer
from core.suggestions import SuggestionEngine
from utils.helpers import save_uploaded_file, cleanup_temp_files, get_match_color

# ========================= CONFIG =========================
st.set_page_config(
    page_title="JobMind AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("JobMind AI")
st.markdown("**Smart Local AI Resume & Job Description Matcher**")

# ===================== SESSION STATE =====================
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline()
    st.session_state.analyzer = Analyzer(st.session_state.rag)
    st.session_state.suggestions = SuggestionEngine(st.session_state.rag)
    st.session_state.analyzed = False
    st.session_state.messages = []

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("Upload Documents")
    
    resume_file = st.file_uploader("Your Resume (PDF)", type="pdf", key="resume")
    jd_file = st.file_uploader("Job Description (PDF)", type="pdf", key="jd")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Analyze Documents", type="primary", use_container_width=True):
            if not resume_file:
                st.error("Please upload your Resume")
            else:
                temp_paths = []
                try:
                    with st.spinner("Processing documents..."):
                        resume_path = save_uploaded_file(resume_file)
                        temp_paths.append(resume_path)
                        
                        jd_path = save_uploaded_file(jd_file)
                        if jd_path:
                            temp_paths.append(jd_path)

                        # Ingest using your rag_pipeline
                        st.session_state.rag.ingest(temp_paths)
                        
                        st.session_state.analyzed = True
                        st.success("Documents Analyzed Successfully!")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    cleanup_temp_files(temp_paths)

    with col2:
        if st.button("Clear Session", use_container_width=True):
            st.session_state.rag = RAGPipeline()
            st.session_state.analyzed = False
            st.session_state.messages = []
            st.rerun()

# ===================== MAIN CONTENT =====================
if st.session_state.analyzed:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Dashboard", 
        "Gap Analysis", 
        "Cover Letter", 
        "Suggestions", 
        "Chat"
    ])

    # ------------------- Dashboard -------------------
    with tab1:
        st.header("Match Dashboard")
        score = st.session_state.analyzer.get_match_score()
        color = get_match_color(score)
        
        print(score)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Overall Match", score, delta=color)
        with col2:
            st.success("Analysis Complete! Check other tabs for details.")

    # ------------------- Gap Analysis -------------------
    with tab2:
        st.header("Gap Analysis")
        if st.button("Generate Detailed Gap Analysis", type="primary"):
            with st.spinner("Analyzing gaps between resume and job description..."):
                result = st.session_state.analyzer.gap_analysis()
                st.markdown(result)

    # ------------------- Cover Letter -------------------
    with tab3:
        st.header("AI Cover Letter")
        if st.button("Generate Personalized Cover Letter", type="primary"):
            with st.spinner("Writing professional cover letter..."):
                result = st.session_state.suggestions.generate_cover_letter()
                st.markdown(result)
                
                st.download_button(
                    label="Download Cover Letter",
                    data=result,
                    file_name="Cover_Letter.txt",
                    mime="text/plain"
                )

    # ------------------- Suggestions -------------------
    with tab4:
        st.header("Resume Improvement Suggestions")
        if st.button("Get Actionable Suggestions"):
            with st.spinner("Generating suggestions..."):
                result = st.session_state.suggestions.get_improvement_suggestions()
                st.markdown(result)

    # ------------------- Chat -------------------
    with tab5:
        st.header("Ask Anything")
        
        for msg, is_user in st.session_state.messages:
            with st.chat_message("user" if is_user else "assistant"):
                st.write(msg)

        if prompt := st.chat_input("Ask about resume, job, skills, or improvements..."):
            st.session_state.messages.append((prompt, True))
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # You can improve this later by adding a query method in RAGPipeline
                    answer = st.session_state.rag.query(prompt) if hasattr(st.session_state.rag, 'query') else \
                             "Chat functionality needs .query() method in RAGPipeline. Use other tabs for now."
                    st.write(answer)
            st.session_state.messages.append((answer, False))

else:
    st.info("Please upload your **Resume** and **Job Description** from the sidebar and click **Analyze Documents**")

# Footer
st.caption("JobMind AI | 100% Local | RAG | LangChain + Ollama")