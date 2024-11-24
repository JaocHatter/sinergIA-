from typing import List, TypedDict, Optional

class QueryState(TypedDict, total = False):
    query: str =  ""
    reference_papers: List[str] = []
    enhanced_queries: List[str] = []
    source: str = "arxiv"