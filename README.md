# LangChain + DDGS MCP Web Search Agent

A minimal LangChain agent that uses a local LLM (LM Studio) and DDGS MCP server to answer questions with live web search.

## Architecture

```
agent.py
  ├── LM Studio (OpenAI-compatible API)  ← LLM_HOST:1234
  └── DDGS MCP Server (HTTP SSE)         ← MCP_HOST:8000
        └── tools: search_text, search_news, search_images ...
```

## Requirements

- [LM Studio](https://lmstudio.ai/) with a tool-call capable model (e.g. `qwen/qwen3.5-9b`)
- Python 3.10+

## Setup

```bash
pip install -r requirements.txt
```

## Usage

**1. Start DDGS MCP server**

```bash
ddgs api
```

**2. Start LM Studio Local Server** (port 1234, load a function-calling model)

**3. Run the agent**

```bash
python agent.py
```

```
Agent ready. Type your question (or 'exit' to quit).

You: What is the weather in Taipei today?

AI: ...
```

Type `exit` or press Ctrl+C to quit.

## Environment Variables

| Variable   | Default                | Description                      |
|------------|------------------------|----------------------------------|
| `LLM_HOST` | `host.docker.internal` | LM Studio host (port 1234)       |
| `MCP_HOST` | `localhost`            | DDGS MCP server host (port 8000) |

**Example — running inside a Linux Docker container:**

```bash
LLM_HOST=localhost MCP_HOST=localhost python agent.py
```
