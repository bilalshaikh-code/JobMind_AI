import streamlit as st
import tempfile
import os
from core.rag_pipline import RAGPipeline

# ========================= CONFIG =========================
st.set_page_config(
    page_title="JobMind AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("JobMind AI")
st.markdown("**Local AI Resume & Job Matcher** | Privacy-First RAG System")

# Initialize Session State
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline()
    st.session_state.analyzed = False
    st.session_state.messages = []

# ====================== SIDEBAR ======================
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
                with st.spinner("Processing documents..."):
                    try:
                        # Save uploaded files temporarily
                        resume_path = None
                        jd_path = None

                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(resume_file.getbuffer())
                            resume_path = tmp.name

                        if jd_file:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
                                tmp2.write(jd_file.getbuffer())
                                jd_path = tmp2.name

                        # Ingest using new RAGPipeline
                        file_list = [resume_path]
                        if jd_path:
                            file_list.append(jd_path)

                        st.session_state.rag.ingest(file_list)
                        
                        # Cleanup
                        os.unlink(resume_path)
                        if jd_path:
                            os.unlink(jd_path)

                        st.session_state.analyzed = True
                        st.success("Documents analyzed successfully!")

                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")

    with col2:
        if st.button("Clear All", use_container_width=True):
            st.session_state.rag = RAGPipeline()
            st.session_state.analyzed = False
            st.session_state.messages = []
            st.rerun()

# ====================== MAIN AREA ======================
if st.session_state.analyzed:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Dashboard", 
        "Gap Analysis", 
        "Cover Letter", 
        "Interview Prep", 
        "Chat"
    ])

    with tab1:
        st.header("Match Dashboard")
        st.info("Match Score & Visualization coming soon (you can add later)")
        st.metric(label="Overall Match", value="78%", delta="Good Match")

    with tab2:
        st.header("Gap Analysis")
        if st.button("Generate Detailed Gap Analysis", type="primary"):
            with st.spinner("Analyzing gaps..."):
                result = st.session_state.rag.query(
                    "Perform a detailed gap analysis. Highlight missing skills, experience gaps, and specific suggestions."
                )
                st.markdown(result)

    with tab3:
        st.header("AI Cover Letter")
        if st.button("Generate Cover Letter", type="primary"):
            with st.spinner("Writing personalized cover letter..."):
                result = st.session_state.rag.query(
                    "Write a professional, concise, and impactful cover letter for this job position."
                )
                st.markdown(result)
                st.download_button(
                    label="Download Cover Letter",
                    data=result,
                    file_name="Cover_Letter.txt",
                    mime="text/plain"
                )

    with tab4:
        st.header("Interview Preparation")
        if st.button("Generate Likely Interview Questions"):
            with st.spinner("Generating questions..."):
                result = st.session_state.rag.query(
                    "Generate 6-8 likely technical and behavioral interview questions for this role with sample answers based on my resume."
                )
                st.markdown(result)

    with tab5:
        st.header("Ask Anything")
        for msg, is_user in st.session_state.messages:
            with st.chat_message("user" if is_user else "assistant"):
                st.write(msg)

        if prompt := st.chat_input("Ask about resume, job, improvements, etc..."):
            st.session_state.messages.append((prompt, True))
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.rag.query(prompt)
                    st.write(answer)
            st.session_state.messages.append((answer, False))

else:
    st.info("Upload your **Resume** and **Job Description** from the sidebar and click **Analyze Documents** to start.")

# Footer
st.caption("JobMind AI | 100% Local | Powered by Ollama + LangChain + ChromaDB")