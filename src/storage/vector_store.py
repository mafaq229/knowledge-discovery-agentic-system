import chromadb

from src.state import Document, DocumentType


class VectorStore:
    def __init__(self, 
                 persistent_path="./chroma_db", 
                 collection_name="documents",
                 embedding_function_name="all-MiniLM-L6-v2"
                 ):
        self.client = chromadb.PersistentClient(path=persistent_path)
        self.embedding_function = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_function_name)
        self.collection = self.client.get_or_create_collection(name=collection_name, 
                                                               embedding_function=self.embedding_function)
    
    def add_documents(self, documents: list[Document]):
        # .upsert allows us to add new documents or update existing ones based on ID
        self.collection.upsert(
            ids=[doc.id for doc in documents],
            documents=[doc.content for doc in documents],
            metadatas=[{
                "source": doc.source,
                "doc_type": doc.doc_type.value,
                **doc.metadata
            } for doc in documents]
        )
    
    def query(self, query_text: str, k: int = 5) -> list[Document]:
        results = self.collection.query(
            query_texts=[query_text],
            n_results=k
        )

        # .query returns dict with keys "ids", "documents", "metadatas" - each is a list of lists (one per query)
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        return [
            Document(
                id=i,
                source=m["source"],
                content=d,
                doc_type=DocumentType(m["doc_type"]),
                metadata={k: v for k, v in m.items() if k not in ["source", "doc_type"]}
            )
            for i, d, m in zip(ids, documents, metadatas)
        ]


