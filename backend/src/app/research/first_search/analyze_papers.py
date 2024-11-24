from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

from app.research.settings import settings
from app.research.states.state_sugerence import ResearchStage


def analyze_step(state: Dict[str, Any]) -> Dict[str, Any]:
    llm = ChatGroq(
            temperature=0.2,
            model="llama3-8b-8192",
            api_key=settings.groq_api_key
        )
    papers = state.get("papers", [])
    messages = [
        SystemMessage(
            content=
            "You are a research paper analyzer. Analyze the papers and identify common themes."
        ),
        HumanMessage(content=f"""
        Analyze the following papers and identify common themes:
        
        Papers: {[paper['title'] + ': ' + paper['abstract'] for paper in papers]}
        
        Key themes and research directions:
        """)
    ]
    try:
        response = llm.invoke(messages)
        analysis = response.content
        state["analysis"] = analysis
        state["stage"] = ResearchStage.ANALYSIS.value
        return state
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        state["analysis"] = error_msg
        state["stage"] = ResearchStage.ANALYSIS.value
        return state
