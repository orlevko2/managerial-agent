# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Managerial Agent

A CLI-based conversational AI agent that assists managers with communications, action items, meeting prep, and task prioritization. Uses a local Ollama model via an OpenAI-compatible API — no external API key needed.

## Setup

```bash
pip install -r managerial-agent/requirements.txt
ollama pull llama3.2   # one-time model download
```

Requires [Ollama](https://ollama.com) running locally (`ollama serve`).

## Running

```bash
python managerial-agent/src/agent.py
```

Type `exit` or `quit` to stop. The agent runs from `managerial-agent/src/`, so relative file paths in tool calls resolve there.

## Architecture

### Agentic loop (`src/agent.py`)

`run_turn(conversation)` drives the tool-calling loop:
1. Calls `llama3.2` with the full conversation history + `TOOL_DEFINITIONS`.
2. If the model returns `tool_calls`, each is dispatched via `execute_tool`, and the results are appended as `role: tool` messages before looping back.
3. When the model returns plain text (no tool calls), the reply is returned and the outer loop prints it.

`execute_tool` handles three error paths gracefully (unknown tool, bad JSON arguments, runtime exception) by returning error strings — the model sees them and can recover.

### Tools (`src/tools/`)

`__init__.py` exports two objects consumed by `agent.py`:
- `TOOL_DEFINITIONS` — list of OpenAI JSON Schema function descriptors passed to the model.
- `TOOL_REGISTRY` — dict mapping tool name → callable.

Adding a new tool requires: (1) create the function in a new module, (2) import it in `__init__.py`, (3) add its JSON Schema entry to `TOOL_DEFINITIONS`, and (4) add it to `TOOL_REGISTRY`.

| Tool | Module | Description |
|------|--------|-------------|
| `web_search` | `tools/web_search.py` | DuckDuckGo search via `duckduckgo-search` |
| `read_file` / `write_file` / `list_files` | `tools/files.py` | Local filesystem access (stdlib) |
| `draft_email` | `tools/email_draft.py` | Returns a formatted email block (no SMTP) |
| `create_calendar_event` | `tools/calendar_event.py` | Writes a valid `.ics` file to CWD |
