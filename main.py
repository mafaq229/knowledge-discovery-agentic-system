from src.graphs import app
from langchain_core.messages import HumanMessage


def main():
    # creating initial state with a user question
    initial_state = {
        "messages": [
            HumanMessage(content="What are the latest advancements in AI research?")
        ]
    }

    # streaming events from the graph application
    for event in app.stream(initial_state):
        for node_name, output in event.items():
            print(f"--{node_name}--")
            if "messages" in output:
                for msg in output["messages"]:
                    if hasattr(msg, "content") and msg.content:
                        print(f"Content: {msg.content[:500]}")
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        print(f"Tool Calls: {[tc['name'] for tc in msg.tool_calls]}")


if __name__ == "__main__":
    main()
