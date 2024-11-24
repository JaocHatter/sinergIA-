from langgraph.graph import StateGraph, END
from typing import Optional, Dict, List
import logging

from app.research.tools.arxiv_tool import ArxivSearcher
from app.research.states.state_query import QueryState
from app.research.states.state_sugerence import SugerenceState
from app.research.states.state_graph import GraphState
from app.research.states.state_constructor import StateConstructor

from app.research.settings import settings
from app.research.agents.translator import translator_step
from app.research.first_search.analyze_papers import analyze_step
from app.research.first_search.recommender import recommender_step
from app.research.first_search.reference_extractor import extract_reference_papers
from app.research.first_search.query_enhancer import enhance_query

from app.research.retriever.translator_query import ReActRetrieverSystem


MAX_LEN_CONTEXT_WINDOW = 10

# Use settings for logging configuration

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


# REFINEMENT

def create_refinement_workflow() -> StateGraph:
    workflow = StateGraph(QueryState)
    
    workflow.add_node("ref_extractor", extract_reference_papers)
    workflow.add_node("query_enhancer", enhance_query)
    
    workflow.set_entry_point("ref_extractor")
    workflow.add_edge("ref_extractor", "query_enhancer")
    workflow.add_edge("query_enhancer", END)

    return workflow.compile()

def run_refinement(topic: str) -> Optional[Dict]:
    try:
        workflow = create_refinement_workflow()
        initial_state = QueryState()
        initial_state["query"] = topic
        return workflow.invoke(initial_state) # Run the workflow
    except Exception as e:
        logger.error(f"x - Error during refinement: {e}")
        return None


# SEARCH

def run_search(queries: List, max_results = 1, sort_by="Relevance"):
    arxiv_searcher = ArxivSearcher()
    all_results = []
    for enhanced_query in queries:
        results = arxiv_searcher.search(
                        enhanced_query,
                        max_results=max_results,
                        sort_by=sort_by)
        all_results.extend(results)
    # Remove duplicates based on entry_id
    unique_results = {
        paper['entry_id']: paper for paper in all_results
    }
    return unique_results


# SUGERENCE

def create_sugerence_workflow() -> StateGraph:
    """Create and configure the research workflow graph with chat-like interface"""
    workflow = StateGraph(state_schema=SugerenceState)

    workflow.add_node("analyze", analyze_step)
    workflow.add_node("recommend", recommender_step)

    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "recommend")
    workflow.add_edge("recommend", END) 
    return workflow.compile()


def run_sugerence(papers: Dict) -> Optional[Dict]:
    try:
        workflow = create_sugerence_workflow()
        initial_state = SugerenceState()
        initial_state["papers"] = papers
        response = workflow.invoke(initial_state)
        response.pop("papers")
        return  response # Run the workflow
    except Exception as e:
        logger.error(f"x - Error during sugerence: {e}")
        return None


# GRAPH CONSTRUCTOR

def json2dict(result) -> Dict:
    """
    Converts a paper result object to a dictionary format.
    Args:
        result: Paper result object containing paper metadata
    Returns:
        PaperDict: Dictionary containing formatted paper data
    """
    paper_dict = {
        'title': result.title,
        'authors': [author.name for author in result.authors],
        'abstract': result.summary,
        'published': result.published.strftime("%Y-%m-%d"),
        'updated': result.updated.strftime("%Y-%m-%d"),
        'pdf_url': result.pdf_url,
        'entry_id': result.entry_id,
        'categories': result.primary_category
    }
    return paper_dict

def init_constructor_state(papers: List[Dict]) -> StateConstructor:
    """
    Initializes a StateConstructor with the given papers.
    Args:
        papers: List of paper dictionaries
    Returns:
        StateConstructor: Initialized state with default values
    """
    return StateConstructor(
        papers=papers,
        atomized_answer= [],
        stage='',
        next='',
        source='arxiv'
    )

def run_construction(papers_json) -> Optional[Dict]:
    papers = json2dict(papers_json)
    try:
        initial_state = init_constructor_state(papers=papers)
        return translator_step(initial_state)
    except Exception as e:
        logger.error(f"x - Error during construction of the Knowledge Graph: {e}")
        return None

# RETRIEVER

def init_retriever_state(topic: str)->GraphState:
    return GraphState(
        stage = "init",
        user_input = topic,
        next = "supervisor",
        top_k = 5,
        similarity_threshold= 0.7,
        query_type = None,
        embeddings_result = None,
        cypher_result = None
    )

def retriever_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)
    ret = ReActRetrieverSystem()
    # NODES
    workflow.add_node("supervisor", ret.supervisor_step)
    workflow.add_node("embedding", ret.embed_step)
    #workflow.add_node("cypher", ret.cypher_step)

    # EDGES
    #workflow.add_conditional_edges(
    #                                "supervisor",
     #                               ret.type_query, 
      #                              {
       #                                 "embed_step": "embedding",
        #                                "cypher_step": "cypher"
         #                           }
          #                      )
    workflow.add_edge("supervisor","embedding")
    workflow.add_edge("embedding", END)
    #workflow.add_edge("cypher", END)
    workflow.set_entry_point("supervisor")
    return workflow.compile()

def query_graph(topic: str) -> Optional[Dict]:
    try:
        workflow = retriever_workflow()
        initial_state = init_retriever_state(topic=topic)
        return workflow.invoke(initial_state) # Run the workflow
    except Exception as e:
        logger.error(f"y - Error during retrieve: {e}")

