from src.tools.web_search import web_search

ALL_TOOLS = [web_search]
TOOLS_MAP = {tool.name: tool for tool in ALL_TOOLS}

__all__ = [
    "web_search",
    "ALL_TOOLS",
    "TOOLS_MAP",
]