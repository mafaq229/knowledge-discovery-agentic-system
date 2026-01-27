import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from tavily import TavilyClient

load_dotenv()

# Create client once at module level (more efficient)
_tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class WebSearchInput(BaseModel):  # PascalCase for class names
    """Input schema for web search tool."""
    query: str = Field(..., description="The search query string")
    max_results: int = Field(default=5, description="Maximum results to return")


@tool(args_schema=WebSearchInput)
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for current information on any topic."""
    try:
        response = _tavily_client.search(query=query, max_results=max_results)
    except Exception as e:
        return f"Search failed: {str(e)}"
    
    results = response.get("results", [])
    if not results:
        return "No results found."
    
    formatted = ""
    for result in results:
        formatted += f"Title: {result.get('title', 'N/A')}\n"
        formatted += f"URL: {result.get('url', 'N/A')}\n"
        formatted += f"Content: {result.get('content', 'N/A')}\n\n"
    
    return formatted.strip()
