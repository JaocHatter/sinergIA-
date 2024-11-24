from typing import List , Dict, TypedDict
from enum import Enum

class ResearchField(Enum):
    ARXIV = "arxiv"
    PMC = "pmc"
    UNKNOWN = "unknown"

class ResearchState(TypedDict, total=False):    
    search_results: List 
    plos_results: List
    pmc_results: List
    arxiv_results: List
    enhanced_queries: List
    topic: str = ""
    research_data: Dict 
    plan: str = ""
    stage: str = "init"
    next: str = ""
    path: str = ""
    field: ResearchField = ResearchField.UNKNOWN
