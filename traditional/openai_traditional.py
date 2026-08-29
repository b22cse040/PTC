import asyncio
import json
import os
import pprint
import time

from dotenv import load_dotenv
from openai import OpenAI

from src.tool_search_module.tool_search import ToolSearchModule
from src.tools.tool_definitions import TOOL_DEFINITIONS
from src.tools.tool_executors import TOOL_EXECUTORS
from src.tool_search_module.tool_executor import MCPToolExecutor


MODEL = "gpt-5.6-terra"
MAX_TURNS = 25


def build_tools(tools):
    return [
        {
            "type": "function",
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["input_schema"],
        }
        for tool in tools
    ]


async def execute_tool(name, arguments, mcp_client):
    print(f"[Traditional] Tool called: {name}")

    executor = TOOL_EXECUTORS[name]

    if isinstance(executor, MCPToolExecutor):
        return await executor.execute(
            mcp_client=mcp_client,
            **arguments,
        )

    return await executor.execute(**arguments)


def print_tool_search_results(search_result):
    print("\nRetrieved Tools")

    for index, tool in enumerate(search_result.tools, start=1):
        score = getattr(tool, "score", None)

        if score is None:
            print(f"{index}. {tool['name']}")
        else:
            print(f"{index}. {tool['name']:<35} {score:.4f}")


def print_tool_executors(tools):
    print("\nTool Executors")

    for tool in tools:
        tool_name = tool["name"]
        executor = TOOL_EXECUTORS[tool_name]

        print(f"{tool_name:<35} {executor.__class__.__name__}")


def print_mcp_tools(mcp_tools):
    print("\nMCP Tools")

    for tool in mcp_tools:
        print(f"- {tool.name}")


def print_response(response):
    print("\nResponse:")
    print(response.output_text)


def print_messages(messages):
    print("\nMessages:")
    pprint.pprint(messages, sort_dicts=False, width=120)


async def main():
    start_time = time.perf_counter()

    load_dotenv(".env")

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPENAI_API_KEY is not set"

    client = OpenAI(api_key=api_key)
    
    query = (
        "Give me a complete Engineering workforce report. "
        "First identify all employees in the Engineering department. "
        "For each Engineering employee, report their salary, attendance statistics, benefits, and current projects. "
        "For every project they are assigned to, also report the current project status. "
        "Present the results as a clear, detailed textual report organized by employee. "
        "For each employee, describe their salary, attendance rate, days present, days absent, "
        "projects and the status of each project. "
        "Do not use a table; provide the complete answer in natural language."
    )

    # ------------------------------------------------------------------
    # Tool Search
    # ------------------------------------------------------------------

    tool_search = ToolSearchModule(db_path="tools.db")

    for tool in TOOL_DEFINITIONS:
        tool_search.add_tool(tool)
        print(f"Added '{tool['name']}' to search DB")

    print("\nQuery:")
    print(query)

    search_result = tool_search.invoke(query=query, k=10)

    print_tool_search_results(search_result)

    tools = build_tools(search_result.tools)

    print_tool_executors(search_result.tools)

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.tools.mcp_tools"],
    )

    messages = [
        {
            "role": "user",
            "content": query,
        }
    ]

    total_input_tokens = 0
    total_output_tokens = 0
    api_calls = 0

    print("\nConnecting to MCP server...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_client:
            await mcp_client.initialize()

            print("Connected to MCP server")

            mcp_tool_result = await mcp_client.list_tools()
            print_mcp_tools(mcp_tool_result.tools)

            print("\nExecuting Traditional query...")

            for _ in range(MAX_TURNS):
                response = client.responses.create(
                    model=MODEL,
                    input=messages,
                    tools=tools,
                )

                api_calls += 1

                if response.usage:
                    total_input_tokens += response.usage.input_tokens
                    total_output_tokens += response.usage.output_tokens

                function_calls = [
                    item
                    for item in response.output
                    if item.type == "function_call"
                ]

                if not function_calls:
                    print_response(response)
                    break

                messages.extend(
                    [
                        item.model_dump(exclude_none=True)
                        for item in response.output
                    ]
                )

                for function_call in function_calls:
                    arguments = json.loads(function_call.arguments)

                    result = await execute_tool(
                        function_call.name,
                        arguments,
                        mcp_client,
                    )

                    messages.append(
                        {
                            "type": "function_call_output",
                            "call_id": function_call.call_id,
                            "output": json.dumps(
                                result,
                                default=str,
                            ),
                        }
                    )

    tool_search.close()

    total_tokens = total_input_tokens + total_output_tokens
    elapsed_time = time.perf_counter() - start_time

    print("\nTotal tokens:")
    print(f"input-tokens : {total_input_tokens}")
    print(f"output-tokens : {total_output_tokens}")
    print(f"total-tokens : {total_tokens}")

    print("\nAPI calls:")
    print(api_calls)

    print("\nElapsed time:")
    print(elapsed_time)

    print_messages(messages)


if __name__ == "__main__":
    asyncio.run(main())