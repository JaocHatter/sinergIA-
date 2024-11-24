from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

from app.research.settings import settings
from app.research.states.state_sugerence import ResearchStage

def recommender_step(state: Dict[str, Any]) -> Dict[str, Any]:
    llm = ChatGroq(
            temperature=0.2,
            model="llama3-8b-8192",
            api_key=settings.groq_api_key
        )

    # Get analysis from state properly
    analysis = state.get('analysis', '')
    messages = [
        SystemMessage(
            content=
            "You are a research paper recommendation system. Generate search queries based on the analysis."
        ),
        HumanMessage(content=f'''
        Based on the analysis: {analysis}
        
        Generate 5 search queries that:
        1. Explore extensions of the research direction
        2. Cover potential knowledge gaps
        3. Include alternative approaches
        4. Focus on recent developments
        5. Consider related applications
        6. Dont include "Query" in the query
        7. Dont put the queries between quotes

        Format your response as:
        - This is a new query to search
        - Another query 
        - Query 3
        - Query 4
        - Query 5
        ''')
    ]

    try:
        response = llm.invoke(messages)
        queries = [
            line.strip()[2:] for line in response.content.split('\n')
            if line.strip().startswith('-')
        ]

        state["queries"] = queries
        state["stage"] = ResearchStage.RECOMMENDATION.value
        return state
    
    except Exception as e:
        state["recommendations"] = []
        state["queries"] = []
        state["stage"] = ResearchStage.RECOMMENDATION.value
        return state
