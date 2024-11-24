from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict,List
import re

from app.research.states.state_research import ResearchField
from app.research.settings import settings
from app.research.agents.search_tools.arxiv_search import ArxivSearcher
from app.research.agents.search_tools.plos_search import PlosSearcher
from app.research.agents.search_tools.pmc_search import PubMedSearcher

llm_out = """
specialized_db: arxiv
---
arxiv_query: "Deep Learning models for Human Activity Recognition"
arxiv_query: "Sensor-based Human Activity Recognition using Machine Learning"
arxiv_query: "Applications of Convolutional Neural Networks in Activity Recognition"
arxiv_query: "Wearable Devices and Deep Learning for Motion Detection"
arxiv_query: "Real-time Human Activity Recognition using LSTM networks"
"""

class Searcher():
    def __init__(self, model: str = settings.gpt_model):
        # Define your llm
        print("SEARCHER: You are using "+ model)
        self.supervisor_model = ChatOpenAI(
            model = model,
            temperature= settings.temperature,
            api_key = settings.openai_api_key
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a research assistant specializing in breaking down research topics into key concepts and determining the appropriate specialized database after conducting a PLOS search. Your role includes generating search queries and classifying topics into specific databases for further research. Follow these instructions carefully:

                    ### Objective:
                    1. Classify the topic into the most relevant specialized database:
                    - **ArXiv**: Use for topics related to Deep learning, artificial intelligence, physics, mathematics, computer science, quantitative finance, statistics, electrical engineering and systems science, and economics.
                    - **PubMed Central (PMC) and Public Library of Science**: Use for topics related to chemistry, biology, medicine research.
                    2. Generates Queries that could be useful for the user extracting the key words and key concepts.
                    3. If the user give you some papers for references, include them as queries.

                    ### Output Requirements:
                    1. **Classify the specialized database**:
                    - Output the classification in this format:
                        ```
                        specialized_db: <DATABASE_NAME>
                        ```
                    - Choose between `arxiv` or `pmc` based on the research topic's key concepts.

                    3. **Generate 8 queries for the specialized database**:
                    - Based on the classification, provide 5 specific search queries for the selected database:
                        - **If ArXiv**:
                        ```
                        arxiv_query: <QUERY>
                        ```
                        Example:
                        ```
                        arxiv_query: "Vision Transformer Models in Computer Science"
                        arxiv_query: "Graph Neural Networks for Engineering Applications"
                        ```
                        - **If PMC and Public Library of Science (4 to PMC and 4 ro PLOS**:
                        ```
                        plos_query: 'http://api.plos.org/search?q=<LLM_GENERATED_QUERY>&fl=title,author,abstract,reference,publication_date,id&wt=json'
                        ```
                        - Ensure the queries are relevant to the research topic and use Boolean operators (e.g., `OR`) to include variations of key concepts.
                        - Must there plos_queries and pmc_queries, 5 of each one
                        - Examples:
                        ```
                        plos_query: 'http://api.plos.org/search?q=abstract:"Attention Mechanism" OR abstract:"Multihead Attention"&fl=title,author,abstract,reference,publication_date,id&wt=json'
                        plos_query: 'http://api.plos.org/search?q=title:"Transformer Architecture" AND abstract:"Vision Transformers"&fl=title,author,abstract,reference,publication_date,id&wt=json'
                        ```
                        ```
                        pmc_query: <QUERY>
                        ```
                        Example:
                        ```
                        pmc_query: "Advances in Biomedical Imaging"
                        pmc_query: "Molecular Biology of Cancer"
                        ```

                    ### Additional Formatting Rules:
                    - Ensure that each query is specific, concise, and relevant to the input topic.
                    - Maintain consistency in the query format for easy integration with external APIs.
                    - If any ambiguity exists in the classification, choose the most suitable database based on the dominant topic.

                    ### Final Output Example (YOUR OUTPUT MUST LOOK EXACTLY LIKE THIS):
                    - **If ArXiv**:
                    ```
                    specialized_db: arxiv
                    ---
                    arxiv_query: "Optimization Techniques for Deep Learning"
                    arxiv_query: "Neural Network Training Strategies"
                    arxiv_query: "Adaptive Gradient Descent in Machine Learning"
                    ...
                    ```
                    - **If PMC and Public Library of Science**:
                    ```
                    specialized_db: pmc
                    ---
                    plos_query: 'http://api.plos.org/search?q=(abstract:"Cancer" AND title:"Deep Learning") OR (abstract:"Machine Learning" AND body:"Covid")&fl=title,author,abstract,reference,publication_date,id&wt=json'
                    plos_query: 'http://api.plos.org/search?q=abstract:"Virus" OR abstract:"Graph Neural Networks"&fl=title,author,abstract,reference,publication_date,id&wt=json'
                    plos_query: 'http://api.plos.org/search?q=abstract:"Biohazard" OR title:"Microplastics"&fl=title,author,abstract,reference,publication_date,id&wt=json'
                    ...
                    ---
                    pmc_query: "Advances in Biomedical Imaging"
                    pmc_query: "Molecular Biology of Cancer"
                    ...
                    ```
                    ## Example:
                    ### User input:
                    ```
                    I want to start a research about Transformer Architechture, I have these papers as references:
                    - Attention is all you need
                    - Focus Your Attention
                    ```
                    ### LLM output:
                    ```
                    specialized_db: arxiv
                    ---
                    arxiv_query: "Attention Is All You Need"
                    arxiv_query: "Focus you attention"
                    arxiv_query: "Transformers architecture applied to computer vision"
                    ...
                    ```
                    ### Notes for the LLM:
                    - Ensure that the specialized database classification is precise.
                    - Generate queries that are likely to yield relevant and valuable research results.
                    - Use natural language processing techniques to refine the queries and capture variations in terminology.
                    """
                ),
                (
                    "user",
                    "Topic: {topic}"
                )
            ]
        )
    def create_plan(self, state: Dict) -> Dict:
        result = self.supervisor_model.invoke(
            self.prompt.format_messages(
                topic=state["topic"]
            )
        )
        # Parse the LLM response to extract field classification and queries
        state["plan"] = result.content
        state["stage"] = "research"
        print(state["plan"])
        return state

def searcher_step(state: Dict) -> Dict:#
    print("SEARCHER STEP")
    supervisor = Searcher()
    new_topic = state.get("research_data", {}).get("topic", "")
    if not new_topic:
        raise ValueError("No topic provided in research data")
    state = supervisor.create_plan(state)
    
    # Extract research field
    db_match = re.search(r"specialized_db:\s*(\w+)", state["plan"])
    field = db_match.group(1).strip() if db_match else None
    
    # Determine research field
    if "arxiv" == field:
        state["field"] = ResearchField.ARXIV
        state["next"] = "arxiv_tool"
    elif "pmc" == field or "pubmed" == field:
        state["field"] = ResearchField.PMC
        state["next"] = "pmc_tool"
    state["topic"] = new_topic
    return state

def plos_step(state: Dict) -> Dict:
    print("PLOS_and_PMC_STEP")
    searcher = PlosSearcher(max_results=3)
    searcher = PubMedSearcher(query="", max_results=3)

    # Enhaced query extraction
    plos_queries = re.findall(r"plos_query:\s*'(.*?)'", state["plan"])
    pmc_queries = re.findall(r"pmc_query:\s*(.*?)",state["plan"])

    # pmc results
    pmc_results = []
    for query in pmc_queries:
        searcher.query = query
        results = searcher.get_results(query)
        pmc_results.extend(results)
    state["pmc_results"] = pmc_results 

    # plos_queries
    plos_results = []
    for solr_query in plos_queries:
        plos_results += searcher.get_results(solr_query)
    state["plos_results"] = plos_results

    # Determine next step based on field
    state["next"] = "translator"
    state["search_results"] = state["plos_results"] + state["pmc_results"]   
    print("pmc and plos results: " + str(len(state["search_results"])))
    return state


def arxiv_step(state: Dict) -> Dict:
    print("ARXIV_STEP")
    
    # Crear instancia del buscador de ArXiv
    searcher = ArxivSearcher(query="", max_results=3)
    
    # Extraer las queries especializadas de ArXiv desde el estado
    arxiv_queries = re.findall(r"arxiv_query:\s*\"(.*?)\"",state["plan"])
    specialized_results = []
    
    # Ejecutar las consultas en ArXiv y agregar los resultados
    for query in arxiv_queries:
        searcher.query = query
        results = searcher.get_results(query)
        specialized_results += results
    state["arxiv_results"] = specialized_results
    print("arxiv results: " + str(len(specialized_results)))

    # Actualizar el estado con los resultados especializados
    state["search_results"] = specialized_results
    state["next"] = "translator"
    return state

def is_arxiv(state: Dict) -> str:
    return state["field"].value 