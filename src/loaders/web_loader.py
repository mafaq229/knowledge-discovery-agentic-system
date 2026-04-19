import httpx
import hashlib
from bs4 import BeautifulSoup

from src.state import Document, DocumentType

def load_web_page(url: str) -> Document:
    try:
        response = httpx.get(url)
        response.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Error loading web page {url}") from e
    soup = BeautifulSoup(response.content, "html.parser")
    
    doc = Document(
        id=hashlib.sha256(url.encode()).hexdigest(),
        source=url,
        content=soup.get_text(separator="\n", strip=True),
        doc_type=DocumentType.WEB,
        metadata={
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }
    )
    return doc
