import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

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

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=8096,
            system=SYSTEM_PROMPT,
            messages=conversation,
        )

        assistant_message = response.content[0].text
        conversation.append({"role": "assistant", "content": assistant_message})

        print(f"\nAgent: {assistant_message}\n")


if __name__ == "__main__":
    run_agent()
