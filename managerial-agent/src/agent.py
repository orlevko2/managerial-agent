from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

SYSTEM_PROMPT = """You are a managerial assistant agent. You help managers with tasks such as:
- Drafting and summarizing communications
- Tracking action items and decisions
- Preparing meeting agendas and notes
- Prioritizing tasks and projects
- Summarizing status updates

Be concise, structured, and action-oriented in your responses."""


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

        response = client.chat.completions.create(
            model="llama3.2",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation,
        )

        assistant_message = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_message})

        print(f"\nAgent: {assistant_message}\n")


if __name__ == "__main__":
    run_agent()
