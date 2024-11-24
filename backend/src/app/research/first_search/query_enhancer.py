from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import Dict

from app.research.settings import settings

def enhance_query(state: Dict) -> Dict:
    """Generate multiple enhanced search queries, prioritizing reference papers."""
    llm = ChatGroq(
            temperature=0.2,
            model="llama3-8b-8192",
            api_key=settings.groq_api_key
        )

    template = """
    Generate exactly 10 search queries based on the following input. 
    If reference papers are provided, include them first, then complement with additional queries.
    Each query should explore a different aspect of the research topic.

    User Query: {query}
    Reference Papers: {ref_papers}

    Rules:
    1. Return exactly 10 queries total
    2. Each line must start with '-'
    3. If reference papers exist,put them first and use them as exact search strings
    4. Generate complementary queries for remaining slots
    5. Ensure queries are specific and research-focused
    6. Dont put the queries between quotes
    Format your response as:
    - [Query 1]
    - [Query 2]
    - [Query 3]
    - [Query 4]
    - [Query 5]
    - ...
    """

    ref_papers = "\n".join([
        f"- {paper}" for paper in (state["reference_papers"] or [])
    ]) if state["reference_papers"] else "None"

    prompt = PromptTemplate(template=template,
                            input_variables=["query", "ref_papers"])

    try:
        chain = prompt | llm
        result = chain.invoke({
            "query": state["query"],
            "ref_papers": ref_papers
        }).content

        # Extract queries from the result
        queries = [
            line[2:].strip() for line in result.split('\n')
            if line.strip().startswith('-')
        ]

        # Return at least one query (original if enhancement fails)
        state["enhanced_queries"] =  queries if queries else [state["query"]]
        return state
    except Exception as e:
        print(f"Query enhancement failed: {str(e)}")
        return state
