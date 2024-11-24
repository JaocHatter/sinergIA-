from typing import List, TypedDict, Dict

class StateConstructor(TypedDict, total = False):
    papers: List[Dict] = []
    atomized_answer: List[str] = []
    stage: str = ''
    next: str = ''
    source: str = "arxiv"