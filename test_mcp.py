import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.tools.mcp_tools"],
    )

    async with stdio_client(server_params) as (
        read,
        write,
    ):
        async with ClientSession(
            read,
            write,
        ) as session:

            await session.initialize()

            print("MCP server connected successfully!")

            tools = await session.list_tools()

            print("\nAvailable tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            # Execute an MCP tool
            print("\nExecuting get_employee_attendance...")

            result = await session.call_tool(
                "get_employee_attendance",
                {
                    "employee_id": 1,
                },
            )

            print("\nTool result:")
            print(result)

            print("\nStructured content:")
            print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())