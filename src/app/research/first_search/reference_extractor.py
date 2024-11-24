from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import Dict
from app.research.settings import settings

def extract_reference_papers(state: Dict)-> Dict:
    """Extract paper titles from the query."""
    llm = ChatGroq(
            temperature=0.2,
            model="llama3-8b-8192",
            api_key=settings.groq_api_key
        )
    
    template = """
    Given the research query below, identify and extract any paper titles mentioned.
    Return them as a list, one per line starting with '-'.
    Include both formally cited papers and those mentioned in plain text.

    Research Query: {query}

    Paper titles:
    """

    prompt = PromptTemplate(template=template, input_variables=["query"])
    chain = prompt | llm

    try:
        result = chain.invoke({"query": state["query"]}).content
        # Extract paper titles from the result (lines starting with '-')
        papers = [
            line[1:].strip() for line in result.split('\n')
            if line.strip().startswith('-')
        ]
        state["reference_papers"] = papers if papers else [] 
        return state
    except Exception:
        return state