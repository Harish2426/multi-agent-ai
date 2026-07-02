import chromadb
from sentence_transformers import SentenceTransformer


class Memory:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="database/vector_db"
        )

        self.collection = self.client.get_or_create_collection(
            "memory"
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def add(self, text):

        embedding = self.model.encode(text).tolist()

        self.collection.add(
            ids=[str(self.collection.count())],
            documents=[text],
            embeddings=[embedding]
        )

    def search(self, query):

        embedding = self.model.encode(query).tolist()

        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=3
        )

        return result["documents"][0]


memory = Memory()