from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.agents import agent_node, tools_node

def should_continue(state: AgentState) -> str:
    """Check if the agent wants to call tools or is finished."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "end"

graph = StateGraph(AgentState)

# adding nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)

# adding edges
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "agent")

app = graph.compile()
