import hashlib
import pdfplumber

from src.state import Document, DocumentType


def load_pdf_file(file_path: str) -> Document:
    try:
        with pdfplumber.open(file_path) as pdf:
            text = []
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text.append(f"\n\n--- Page {i} ---\n\n{page_text}")
            content = "\n\n".join(text)
            metadata = pdf.metadata
            page_count = len(pdf.pages)
    except Exception as e:
        raise RuntimeError(f"Error loading PDF file {file_path}") from e
    
    doc = Document(
        id=hashlib.sha256(file_path.encode()).hexdigest(),
        source=file_path,
        content=content,
        doc_type=DocumentType.PDF,
        metadata={
            "page_count": page_count,
            "author": metadata.get("Author"),
            "title": metadata.get("Title"),
        }
    )
    return doc
    
    

