import chromadb
import os
import hashlib
# import LLMConnection
from pathlib import Path
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from src import LLMConnection

EMBEDDING_MODEL = "text-embedding-ada-002"
class EmbeddingGenerator:

    def __init__(self, model="all-MiniLM-L6-v2", collection_name="document_chunks", persist_directory=None):
        self.embedding_fn = None
        if model == "all-MiniLM-L6-v2":
            self.model = SentenceTransformer(model)
            
        else:
            self.model= None
            self.embedding_fn = LLMConnection.CustomeOpenAIEmbeddings()
        
        self.add_data_now = 0
        self.chroma_client = chromadb.Client()

        if persist_directory:
            Path(persist_directory).mkdir(parents=True, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=persist_directory) #Rather than hosting in disk, we would have to create server for this with the settings configed.
        else:
            self.chroma_client = chromadb.EphemeralClient()

        collection_details = self.chroma_client.list_collections()
        print(f"Collection(name={collection_name})", collection_details)
        
        if f"Collection(name={collection_name})" in str(collection_details):
            print("here")
            self.collection = self.chroma_client.get_collection(name=collection_name)
        # else:
        #     self.add_data_now = 1
        #     if self.embedding_fn:

        #         self.collection = self.chroma_client.create_collection(name=collection_name, embedding_function=self.embedding_fn)
        #     else:
        #         self.collection = self.chroma_client.create_collection(name=collection_name, metadata={"hnsw:space":"cosine"})

    
    def generate_id(self, text):
        #simple IDS
        return [str(i) for i in range(len(text))]
        
        #normal ids
        #return hashlib.sha256(text.encode()).hexdigest()
        
    
    def get_embedding(self, text):
        return self.model.encode(text).tolist()


    def add_data(self, documents, ids=None, metadata=None):
        # embeddings = self.model.encode(documents).tolist()

        if not ids:
            ids = self.generate_id(documents)

        if metadata:
            self.collection.add(documents=documents, metadata=metadata, ids=ids)
        else:
            self.collection.add(documents=documents, ids=ids)
        
        return ids

    def search(self, query, top_k=3):
        if self.model:
            query_embedding = self.model.encode(query).tolist()
        else:
            query_embedding = self.embedding_fn.embed_query(query)

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )


    def get_details_about_collection(self):
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }

