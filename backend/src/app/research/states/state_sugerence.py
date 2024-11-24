from enum import Enum
from typing import Dict, List, TypedDict

"""
papers: Son los papers que ya han sido elegidos por el usuario, una vez que el usuario se encuentre conforme con su busqueda estos serán enviados como JSON al proximo proceso
stage: Etapa actual del flujo
queries: Queries generadas por la AI para mejores resultados
analysis: Analisis del nodo "Analyzer", basicamente es la sintesis de los 5 o menos ultimos papers elegidos
user_input: En caso las queries que haya elegido no parezcan convencer al usuario, este puede agregar una sugerencia de lo que busca
"""

class SugerenceState(TypedDict, total=False):
    papers: List[Dict] = []
    stage: str = ''
    action: str = ''
    next: str = ''
    action: str = ''
    queries: List = []
    analysis: str = ''
    user_input: str = ''

class ResearchStage(Enum):
    SEARCH = "search"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    COMPLETE = "complete"