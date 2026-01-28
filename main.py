from src.graphs import app
from langchain_core.messages import HumanMessage


def main():
    # creating initial state with a user question
    initial_state = {
        "messages": [
            HumanMessage(content="What are the latest advancements in AI research?")
        ]
    }

    result = app.invoke(initial_state)
    print("Final Result:")
    for message in result["messages"]:
        print(f"\n[{message.__class__.__name__}]")
        if hasattr(message, "content") and message.content:
            print(message.content[:500])
        if hasattr(message, "tool_calls") and message.tool_calls:
            print(f"Tool Calls: {message.tool_calls}")


if __name__ == "__main__":
    main()
