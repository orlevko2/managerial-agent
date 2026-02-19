# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Managerial Agent

A CLI-based conversational AI agent that uses the Anthropic Claude API to assist managers with communications, action items, meeting prep, and task prioritization.

## Setup

```bash
pip install -r managerial-agent/requirements.txt
```

Requires [Ollama](https://ollama.com) running locally with `llama3.2` pulled (`ollama pull llama3.2`). No API key needed.

## Running

```bash
python managerial-agent/src/agent.py
```

Type `exit` or `quit` to stop the agent.

## Architecture

- **`src/agent.py`** — Entry point. Initializes an OpenAI-compatible client pointed at the local Ollama server (`http://localhost:11434/v1`), defines `SYSTEM_PROMPT`, and runs a multi-turn conversation loop that maintains message history and calls `llama3.2`.
- **`src/tools/`** — Empty module placeholder for future tool integrations (e.g., function-calling tools to extend the agent's capabilities).

The agent uses a simple stateful loop: user input is appended to a `conversation` list, sent to the API with the full history each turn, and the assistant's reply is appended back before the next iteration.
