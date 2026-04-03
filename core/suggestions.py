# core/suggestions.py
from core.rag_pipeline import RAGPipeline
from langchain_classic.prompts import PromptTemplate
from langchain_classic.schema.output_parser import StrOutputParser

class SuggestionEngine:
    def __init__(self, rag: RAGPipeline):
        self.rag = rag

    def generate_cover_letter(self) -> str:
        """Generate personalized cover letter"""
        prompt_template = PromptTemplate.from_template(
            """You are a professional cover letter writer.

            Context:
            {context}

            Write a concise, professional, and impactful cover letter (maximum 300 words).
            Highlight relevant experience and show enthusiasm.
            Do not use generic statements.

            Cover Letter:"""
        )

        context = "\n\n".join(self.rag.retrieve("Write cover letter for this job", k=5))
        
        chain = prompt_template | self.rag.llm | StrOutputParser()
        result = chain.invoke({"context": context})
        return result.strip()

    def get_improvement_suggestions(self) -> str:
        """Actionable resume improvement suggestions"""
        prompt_template = PromptTemplate.from_template(
            """You are an expert resume writer.

            Context:
            {context}

            Give 5-7 specific, actionable bullet point suggestions to improve this resume 
            for the target job description. Focus on achievements, keywords, and impact.

            Suggestions:"""
        )

        context = "\n\n".join(self.rag.retrieve("resume improvement suggestions", k=4))
        
        chain = prompt_template | self.rag.llm | StrOutputParser()
        result = chain.invoke({"context": context})
        return result.strip()