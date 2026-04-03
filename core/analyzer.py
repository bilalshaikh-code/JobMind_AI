# core/analyzer.py
from core.rag_pipeline import RAGPipeline
from langchain_classic.prompts import PromptTemplate
from langchain_classic.schema.output_parser import StrOutputParser

class Analyzer:
    def __init__(self, rag: RAGPipeline):
        self.rag = rag

    def get_match_score(self) -> str:
        """Calculate match score using LLM"""
        prompt_template = PromptTemplate.from_template(
            """You are an expert recruiter. Based on the resume and job description, 
            give ONLY the overall match percentage.

            Context:
            {context}

            Reply with ONLY the number followed by % sign. Example: 76%
            Do not write any explanation."""
        )

        context = "\n\n".join(self.rag.retrieve("Calculate match score between resume and job description", k=6))
        
        chain = prompt_template | self.rag.llm | StrOutputParser()
        result = chain.invoke({"context": context})
        return result.strip()

    def gap_analysis(self) -> str:
        """Detailed gap analysis"""
        prompt_template = PromptTemplate.from_template(
            """You are a senior career coach. Perform a detailed gap analysis.

            Context:
            {context}

            Analyze the gaps in:
            - Technical Skills
            - Experience
            - Education / Certifications
            - Responsibilities

            Provide constructive and specific suggestions.
            Answer:"""
        )

        context = "\n\n".join(self.rag.retrieve("gap analysis between resume and job description", k=5))
        
        chain = prompt_template | self.rag.llm | StrOutputParser()
        result = chain.invoke({"context": context})
        return result.strip()