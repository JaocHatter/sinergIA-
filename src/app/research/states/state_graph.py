from typing import List , Dict, Annotated, TypedDict, Optional
from enum import Enum

class QueryType(str, Enum):
    EMBEDDING = "embed_step"
    CYPHER = "cypher_step"

class GraphState(TypedDict, total = False):
    stage: str 
    user_input: str = ""
    next: str = "supervisor"
    top_k: int = 5
    similarity_threshold: float = 0.7
    query_type: Optional[QueryType] = None
    embedding_result: Optional[List[dict]] = None
    cypher_result: Optional[List[dict]] = None
