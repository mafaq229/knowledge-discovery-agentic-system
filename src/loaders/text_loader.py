import os
import hashlib

from src.state import Document, DocumentType


def load_text_file(file_path: str) -> Document:
    try:
        with open(file_path) as f:
            content = f.read()
    except Exception as e:
        # from e is used to preserve the original traceback, which can be helpful for debugging. print(e) is for human readability
        raise RuntimeError(f"Error loading file {file_path}") from e
    
    doc = Document(
        # encodes converts string to bytes, required for hashlib.sha256 or .md5
        # hexdigest returns a string representation of the hash, which is suitable for our document ID
        id=hashlib.sha256(file_path.encode()).hexdigest(),
        source=file_path,
        content=content,
        doc_type=DocumentType.TEXT,
        metadata= {
            "last_modified": os.path.getmtime(file_path),
            "file_size": os.path.getsize(file_path),
            "filename": os.path.basename(file_path)
        }
    )
    return doc

