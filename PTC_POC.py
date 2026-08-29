import asyncio
import os
from pprint import pprint
from dotenv import load_dotenv

from anthropic import Anthropic
# from openai import OpenAI

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.ptc.ptc_anthropic.ptcAnthropic import PTCAnthropic
# from src.ptc.ptc_openai.ptcOpenAI import PTCOpenAI

from src.tool_search_module.tool_search import ToolSearchModule
from src.tools.tool_definitions import TOOL_DEFINITIONS


load_dotenv(".env")


# Anthropic
api_key = os.getenv("ANTHROPIC_API_KEY")
assert api_key is not None

# OpenAI
# api_key = os.getenv("OPENAI_API_KEY")
# assert api_key is not None


async def main():

    ## Anthropic
    client = Anthropic()
    MODEL = "claude-sonnet-4-5"

    ## OpenAI
    # client = OpenAI(api_key=api_key)
    # MODEL = "gpt-5.6-terra"
    print(f"Model: {MODEL}")


    ## Tool Search
    tool_search = ToolSearchModule(db_path="tools.db")
    for tool in TOOL_DEFINITIONS:
        tool_search.add_tool(tool)
        print(f"Added '{tool['name']}' to search DB")


    ## Query
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
    print("\nQuery:")
    print(query)


    ## Retrieve Relevant Tools
    search_result = tool_search.invoke(query=query, k=10)

    print("\nRetrieved Tools")
    for i, tool in enumerate(search_result.tools, start=1):
        print(f"{i}. {tool['name']:<35} {tool['score']:.4f}")


    print("\nTool Executors")
    for name, executor in search_result.tool_executors.items():
        print(f"{name:<35} {type(executor).__name__}")


    ## Create PTC Implementation Anthropic
    ptc = PTCAnthropic(client=client, model=MODEL, truncate_data=True)

    # OpenAI
    # ptc = PTCOpenAI(client=client, model=MODEL, truncate_data=True)
    print("\nCreated PTC Module")

    ## MCP Client
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.tools.mcp_tools"],
    )
    print("\nConnecting to MCP server...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_client:
            await mcp_client.initialize()

            print("Connected to MCP server")
            tools = await mcp_client.list_tools()

            print("\nMCP Tools")
            for tool in tools.tools:
                print(f"- {tool.name}")

            ## Execute Query
            print("\nExecuting PTC query...")
            result = await ptc.invoke(
                user_message=query,
                tool_search_result=search_result,
                mcp_client=mcp_client,
            )


    ## Results
    print("\nResponse:")
    print(result.response)
    print("\nTotal tokens:")
    # print(result.tokens_usage)
    for key, val in result.tokens_usage.items():
        print(f"{key} : {val}")
    print("\nAPI calls:")
    print(result.api_count)
    print("\nElapsed time:")
    print(result.elapsed_time)
    print("\nMessages:")
    pprint(result.messages, indent=2, width=120)

    tool_search.close()


if __name__ == "__main__":
    asyncio.run(main())