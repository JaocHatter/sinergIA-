from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from neo4j import GraphDatabase
import numpy as np
from scipy.spatial.distance import cosine
import logging

from app.research.settings import settings
from app.research.settings import client_openai

# Use settings for logging configuration
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

def get_embedding(text, model: str = "text-embedding-ada-002"):
    embedding_result = client_openai.embeddings.create(
        model = model,
        input = [text]
    )
    return embedding_result.data[0].embedding

class ReActRetrieverSystem():
    def __init__(self, model:str = settings.groq_model):
        self.llm = ChatGroq(
            model = model,
            temperature = 0,
            api_key=  settings.groq_api_key
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system","""
            Analyze the following query and determine if it requires:
            1. Semantic search using embeddings (for general information retrieval)
            2. Graph query using Cypher (for relationship-based queries)
            Return only "embed_step" or "cypher":
            """),
            ("user", "Question: {question}")]
        )

        self.driver = GraphDatabase.driver(
                                            "url", 
                                            auth = (
                                                    "neo4j", 
                                                    "pass"
                                                    )
                                            )

    def supervisor_step(self, state: Dict)->Dict:
        state["stage"] = "supervisor"
        response = self.llm.invoke(
            self.prompt.format_messages(
                question=state["user_input"]
            )
        )
        veredict:str = response.content
        state["next"] = veredict
        return state


    def embed_step(self, state: Dict)->Dict:
        query_embedding = np.array(get_embedding(state["user_input"]))
        with self.driver.session() as session:
            # Fetch all paper embeddings
            result = session.run(
            """
            MATCH (p:Paper)
            WHERE p.abstract_embedding IS NOT NULL
            RETURN
            p.id as id,
            p.abstract as abstract,
            p.abstract_embedding as embedding
            """
            )
            similarities = []
            threshold =state["similarity_threshold"]

            for record in result:
                # Convert embedding string to list of floats
                paper_embedding = np.array(record['embedding'])
                
                # Calculate cosine similarity
                similarity = 1 - cosine(query_embedding, paper_embedding)
                
                # Add to results if above threshold
                if similarity >=  threshold:
                    similarities.append({
                        'title': record['id'],
                        'abstract': record['abstract'],
                        'similarity_score': similarity
                    })
            
            # Sort by similarity score and return top k
            state["embedding_result"] = sorted(
                similarities, 
                key=lambda x: x['similarity_score'], 
                reverse=True
            )[:state["top_k"]]
        return state

    def cypher_step(self, state: Dict)->Dict:
        cypher_prompt = PromptTemplate(
            template="""Generate Cypher query for:
            {query}
            Return only the Cypher query:""",
            input_variables=["query"]
        )
        cypher_query = self.llm.predict(cypher_prompt.format(query=state["user_input"]))
        with self.driver.session() as session:
            print("XD")
        return state

    def type_query(self, state: Dict)->str:
        return state["next"].value
    
