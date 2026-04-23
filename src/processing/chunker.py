from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib

from src.state import Document

def chunk_documents(documents: list[Document],
                    chunk_size: int = 1000,
                    chunk_overlap: int = 200) -> list[Document]:
    
    chunked_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for doc in documents:
        chunks = text_splitter.split_text(doc.content)
        for i, chunk in enumerate(chunks):
            chunked_docs.append(Document(
                id=hashlib.sha256(chunk.encode()).hexdigest(),
                source=doc.source,
                content=chunk,
                doc_type=doc.doc_type,
                metadata={**doc.metadata, "chunk_index": i, "chunk_size": len(chunk)}
            ))
    return chunked_docs