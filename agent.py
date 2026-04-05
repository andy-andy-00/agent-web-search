import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk
from langchain_openai import ChatOpenAI

# Override via env vars: LLM_HOST for LM Studio, MCP_HOST for `ddgs api`
LLM_HOST = os.getenv("LLM_HOST", "host.docker.internal")
MCP_HOST = os.getenv("MCP_HOST", "localhost")

llm = ChatOpenAI(base_url=f"http://{LLM_HOST}:1234/v1", api_key="lm-studio", model="qwen/qwen3.5-9b")


async def main():
    # Fetch tools from the DDGS MCP server (search_text, search_news, ...)
    tools = await MultiServerMCPClient(
        {"ddgs": {"url": f"http://{MCP_HOST}:8000/sse", "transport": "sse"}}
    ).get_tools()

    agent = create_agent(
        model=llm, tools=tools,
        system_prompt=(
            "You do not know the current date, time, or any real-time information. "
            "For any question about today's date, current events, weather, or anything time-sensitive, "
            "you MUST search the web by using the search_text tool to look it up before answering."
        )
    )

    print("Agent ready. Type your question (or 'exit' to quit).")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit", ""):
            break

        # Stream response tokens to terminal; skip tool call/result messages
        print("\nAI: ", end="", flush=True)
        async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": user_input}]},
            stream_mode="messages",
        ):
            msg, _ = chunk
            if isinstance(msg, AIMessageChunk) and msg.content:
                print(msg.content, end="", flush=True)
        print()

asyncio.run(main())
