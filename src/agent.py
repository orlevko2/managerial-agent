import json

from openai import OpenAI

from tools import TOOL_DEFINITIONS, TOOL_REGISTRY

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

SYSTEM_PROMPT = """You are a managerial assistant agent. You help managers with tasks such as:
- Drafting and summarizing communications
- Tracking action items and decisions
- Preparing meeting agendas and notes
- Prioritizing tasks and projects
- Summarizing status updates

You have access to tools for web search, file management, email drafting, and calendar events.
Be concise, structured, and action-oriented in your responses."""


def execute_tool(name: str, arguments: str) -> str:
    if name not in TOOL_REGISTRY:
        return f"Error: unknown tool '{name}'."
    try:
        kwargs = json.loads(arguments)
    except json.JSONDecodeError as e:
        return f"Error: could not parse tool arguments as JSON: {e}"
    try:
        return str(TOOL_REGISTRY[name](**kwargs))
    except Exception as e:
        return f"Error executing tool '{name}': {e}"


def run_turn(conversation: list) -> str:
    while True:
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )
        message = response.choices[0].message

        if message.tool_calls:
            conversation.append(message.model_dump(exclude_unset=True))
            for tc in message.tool_calls:
                print(f"  [tool] {tc.function.name}({tc.function.arguments})")
                result = execute_tool(tc.function.name, tc.function.arguments)
                conversation.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })
        else:
            final = message.content or ""
            conversation.append({"role": "assistant", "content": final})
            return final


def run_agent():
    conversation = []
    print("Managerial Agent ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue

        conversation.append({"role": "user", "content": user_input})
        reply = run_turn(conversation)
        print(f"\nAgent: {reply}\n")


if __name__ == "__main__":
    run_agent()
