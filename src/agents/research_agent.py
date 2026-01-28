import os

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI

from src.state.base import AgentState
from src.tools import TOOLS_MAP, ALL_TOOLS

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-mini"
)
llm = llm.bind_tools(ALL_TOOLS)

def agent_node(state: AgentState) -> dict:
    """
    The agent node - calls LLM to decide next action.
    
    Returns: dict with "messages" key containing the LLM response
    """
    response = llm.invoke(state["messages"])
    # add_messages will handle adding the response to the state after return
    return {"messages": [response]}

def tools_node(state: AgentState) -> dict:
    """
    Execute tool calls from the last AI message.
    Returns ToolMessages with results.
    """
    tool_calls = state["messages"][-1].tool_calls
    results = []
    for tool_call in tool_calls:
        tool_fn = TOOLS_MAP[tool_call["name"]]
        tool_result = tool_fn.invoke(tool_call["args"])
        results.append(ToolMessage(
            content=tool_result,
            tool_call_id=tool_call["id"]
        ))
    return {"messages": results}
