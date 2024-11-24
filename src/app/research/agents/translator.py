from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.text_splitter import CharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.graphs import Neo4jGraph
from langchain_community.graphs.graph_document import GraphDocument,Node,Relationship
from langchain_core.documents import Document

from app.research.settings import client_openai

import time
from typing import Dict, List
from app.research.settings import settings
import logging

# Use settings for logging configuration
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

class Translator:
    def __init__(self, model: str = settings.groq_model):
        print("TRANSLATOR: You are using "+ model)
        
        self.llm = ChatGroq(
            model = model,
            temperature= 0,
            api_key= settings.groq_api_key
        )

        self.text_splitter = CharacterTextSplitter(
            separator= "-"*80+"\n",
            chunk_size=2000,
            chunk_overlap=200,
            keep_separator= False
        )

        self.neo4j_db = Neo4jGraph(
            url = "url",#settings.url,
            username= "neo4j",#settings.username,
            password = "pass"#settings.password
        )

        # GRAPH SETTINGS
        self.txt2graph = LLMGraphTransformer(
            llm = self.llm
        )

def get_embedding(text, model: str = "text-embedding-ada-002"):
    embedding_result = client_openai.embeddings.create(
        model = model,
        input = [text]
    )
    return embedding_result.data[0].embedding

def translator_step(state: Dict) -> bool:
    try:
        translator = Translator()
        state["stage"] = "translator"
        state["next"] = "END"

        # CONVERTING BY BATCHES
        batch_size = 4

        # Atomized Answer
        graph_docs:List[GraphDocument] = [] #:List[GraphDocument]

        for idx, result in enumerate(state["papers"]):
            if idx % batch_size == 0 and idx != 0:
                time.sleep(15)
            root = Node(
                id = result["title"], 
                type = "Paper", 
                properties= {"abstract" : result["abstract"],
                             "abstract_embedding" : get_embedding(result["abstract"]), 
                             "year": result["published"]})
            single_doc = Document(page_content = result["abstract"])

            graph_doc = translator.txt2graph.process_response(single_doc)

            # Connecting authors with their respective Paper
            authors = [Node(id = aut, type= "Author", properties = { "name" : aut }) for aut in result["authors"]]
            authors_relationships = []
            
            for node in authors:
                if node.id != root.id:
                    relationship = Relationship(
                        source=node,
                        target=root,
                        type="AUTHOR_OF", 
                        properties={}
                    )
                    authors_relationships.append(relationship)

            # create a relationship with each new node from graph_doc
            relationships = []
            for node in graph_doc.nodes:
                if node.id != root.id:
                    relationship = Relationship(
                        source=root,
                        target=node,
                        type="RELATED_TO", 
                        properties={}
                    )
                    relationships.append(relationship)
            
            graph_doc.nodes.append(root)
            graph_doc.relationships.extend(authors_relationships)
            graph_doc.relationships.extend(relationships)

            # Append to graph_docs
            graph_docs.append(graph_doc) 
        
        # Connecting to Neo4j Database
        translator.neo4j_db.add_graph_documents(graph_docs)

        # Refresh the graph schema
        translator.neo4j_db.refresh_schema()
        
        return True

    except Exception as e:
        logger.error(f"Error updating Neo4j database: {str(e)}")
        return False