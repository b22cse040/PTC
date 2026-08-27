# Programmatic Tool Calling POC

A proof-of-concept framework for **semantic tool retrieval and programmatic tool calling (PTC)** with Claude.

## Aim

The goal of this project is to avoid exposing an LLM to an entire tool catalog for every query.

Instead, the system:

1. Semantically searches the available tools.
2. Retrieves only the most relevant tools for the user's query.
3. Resolves those tools to `ToolExecutor` objects.
4. Passes the retrieved tools to Claude's Programmatic Tool Calling interface.
5. Executes native Python tools or MCP tools through the corresponding executor.
6. Feeds the results back to Claude until it produces a final response or reaches the turn limit.

This allows the PTC layer to work with a **dynamic subset of tools** while supporting both natively implemented tools and MCP-backed tools.

## How It Works

```text
                         User Query
                             │
                             ▼
                   ┌───────────────────┐
                   │  ToolSearchModule │
                   └─────────┬─────────┘
                             │
                    Semantic Search
                             │
                             ▼
                   ┌───────────────────┐
                   │  Top-K Tool       │
                   │  Definitions      │
                   └─────────┬─────────┘
                             │
                             ▼
                    ToolSearchResult
                    ┌────────┴────────┐
                    │                 │
                  tools        tool_executors
                    │                 │
                    ▼                 ▼
              Tool Metadata     ToolExecutor Objects
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
                NativeToolExecutor          MCPToolExecutor
                         │                         │
                    Python Callable          MCP Client
                                                   │
                                                   ▼
                                              MCP Server
                             │
                             └───────────┬─────────────┘
                                         ▼
                                  ┌───────────────┐
                                  │ PTCAnthropic  │
                                  └───────┬───────┘
                                          │
                                          ▼
                                       Claude
                                          │
                                   Tool Use / PTC
                                          │
                                          ▼
                                   Tool Executor
                                          │
                                          ▼
                                     Tool Result
                                          │
                                          ▼
                                       Claude
                                          │
                                          ▼
                                   Final Response
```

## Tool Architecture

The project separates **tool metadata**, **tool execution**, and **tool retrieval**.

### 1. Tool Definitions

Each tool is represented using metadata such as:

```python
{
    "name": "get_employees_by_department",
    "description": "Return employees belonging to a specified department.",
    "source": "native",
    "input_schema": {...},
    "input_example": {...}
}
```

The metadata is stored in the tool-search database.

The actual execution logic is maintained separately.

Native tools are wrapped using:

```python
NativeToolExecutor(get_employees_by_department)
```

MCP tools are represented using:

```python
MCPToolExecutor("get_employee_attendance")
```

This means the search layer does not need to maintain a `Dict[str, Callable]` containing every implementation.

### 2. Tool Executors

`ToolExecutor` provides the common abstraction used to execute retrieved tools:

```python
class ToolExecutor(ABC):

    @abstractmethod
    async def execute(self, **args) -> Any:
        ...
```

There are currently two implementations.

#### NativeToolExecutor

A native executor is simply a wrapper around a Python callable:

```text
NativeToolExecutor
       │
       ▼
Python Callable
       │
       ▼
   Tool Result
```

Its execution is effectively:

```python
await executor.execute(**args)
```

#### MCPToolExecutor

An MCP executor stores the MCP tool name but **does not store the MCP client**.

```text
MCPToolExecutor
      │
      │ tool name
      ▼
execute(mcp_client, **args)
      │
      ▼
  MCP Client
      │
      ▼
  MCP Server
      │
      ▼
MCP Tool Function
```

The MCP client is supplied at execution time. This keeps the executor lightweight and prevents every executor from owning an MCP connection.

## Tool Search

`ToolSearchModule` is responsible for semantic retrieval.

During ingestion, an embedding is generated using only the tool's name and description:

```text
[CLS] tool[name] [SEP] tool[description]
```

The embedding is stored alongside the tool's database ID.

When a user sends a query:

```text
User Query
    │
    ▼
Query Embedding
    │
    ▼
Cosine Similarity
    │
    ▼
Top-K Tools
```

The database stores the remaining metadata (`input_schema`, `input_example`) alongside the tool.

The search module then resolves the names of retrieved tools against the globally maintained:

```python
TOOL_EXECUTORS: Dict[str, ToolExecutor]
```

This produces a `ToolSearchResult`.

## ToolSearchResult

A search returns:

```python
@dataclass
class ToolSearchResult:
    tools: List[Dict[str, Any]]
    tool_executors: Dict[str, ToolExecutor]
```

`tools` contains the metadata retrieved from the database.

`tool_executors` contains only the executors corresponding to those retrieved tools:

```text
Full TOOL_EXECUTORS
        │
        │ filter by retrieved tool names
        ▼
Retrieved Tool Executors
        │
        ├── NativeToolExecutor
        └── MCPToolExecutor
```

This replaces the previous `tools_callable: Dict[str, Callable]` design.

## Programmatic Tool Calling

`PTCAnthropic` converts the retrieved tools into Anthropic's PTC-compatible format.

Only the retrieved tools are exposed to Claude:

```text
Full Tool Catalog
       │
       │ semantic search
       ▼
Relevant Tools
       │
       ▼
Claude PTC
```

When Claude requests a tool call, `PTCModule._execute_tool()` resolves the tool name against:

```python
result.tool_executors
```

The executor type determines how the tool is invoked:

```text
                    Tool Call
                        │
                        ▼
                  _execute_tool()
                        │
               ┌────────┴────────┐
               │                 │
               ▼                 ▼
      NativeToolExecutor   MCPToolExecutor
               │                 │
               ▼                 ▼
          Callable(**args)   MCP Client
                                 │
                                 ▼
                            MCP Server
```

The resulting data is formatted and returned to Claude, allowing Claude to continue reasoning and make additional tool calls if necessary.

The PTC loop currently allows a maximum of:

```python
TURNS_LEFT = 10
```

turns.

## MCP Integration

MCP-backed tools are implemented as an MCP server in:

```text
src/tools/mcp_tools.py
```

The server exposes tools such as:

```text
get_employee_benefits
calculate_employee_bonus
get_company_holidays
get_employee_attendance
get_employee_projects
get_project_status
```

The server is started using the MCP stdio transport:

```python
if __name__ == "__main__":
    mcp.run()
```

The PTC application creates an MCP client session and launches the server process:

```text
PTC_POC.py
    │
    │ creates MCP ClientSession
    ▼
stdio transport
    │
    ▼
mcp_tools.py
    │
    ▼
MCPServer
    │
    ▼
MCP Tool Function
```

The MCP client is **not stored in `MCPToolExecutor`**. Instead, it is passed into the PTC execution lifecycle and supplied only when an MCP tool needs to execute.

This also means the MCP server does not need to be manually started in another terminal when running the main PTC application. The stdio client launches it as a subprocess.

## Usage

### 1. Create the Tool Search Module

```python
from src.tool_search_module.tool_search import ToolSearchModule

tool_search = ToolSearchModule(db_path="tools.db")
```

### 2. Add Tool Definitions

Tool definitions can be ingested into the search database using:

```python
for tool in TOOL_DEFINITIONS:
    tool_search.add_tool(tool)
```

The tool embedding is generated during ingestion.

### 3. Search for Relevant Tools

```python
query = (
    "Find Engineering employees whose salary is greater than 30000. "
    "For each matching employee, retrieve their attendance statistics."
)

search_result = tool_search.invoke(query=query, k=8)
```

The result contains:

```python
search_result.tools
```

and:

```python
search_result.tool_executors
```

### 4. Initialize Claude PTC

Set your Anthropic API key in the environment:

```text
ANTHROPIC_API_KEY=your-api-key
```

Then:

```python
from anthropic import Anthropic
from src.ptc.PTC_Anthropic.ptcAnthropic import PTCAnthropic

client = Anthropic()

ptc = PTCAnthropic(
    client=client,
    model="claude-sonnet-4-5",
)
```

### 5. Create the MCP Client

The MCP server uses stdio transport:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["-m", "src.tools.mcp_tools"],
)
```

The PTC query must execute inside the MCP client session:

```python
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as mcp_client:
        await mcp_client.initialize()

        result = await ptc.invoke(
            user_message=query,
            tool_search_result=search_result,
            mcp_client=mcp_client,
        )
```

Because MCP tool execution is asynchronous, `PTCModule.invoke()` is also asynchronous:

```python
result = await ptc.invoke(...)
```

## Complete Example

```python
import asyncio

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.ptc.PTC_Anthropic.ptcAnthropic import PTCAnthropic
from src.tool_search_module.tool_search import ToolSearchModule
from src.tools.tool_definitions import TOOL_DEFINITIONS


async def main():

    query = (
        "Find Engineering employees whose salary is greater than 30000. "
        "For each matching employee, retrieve their attendance statistics "
        "and report their name, salary, and attendance rate."
    )

    # Tool Retrieval

    tool_search = ToolSearchModule(db_path="tools.db")

    for tool in TOOL_DEFINITIONS:
        tool_search.add_tool(tool)

    search_result = tool_search.invoke(query=query, k=8)

    # Claude PTC

    client = Anthropic()

    ptc = PTCAnthropic(
        client=client,
        model="claude-sonnet-4-5",
    )

    # MCP Client

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.tools.mcp_tools"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as mcp_client:

            await mcp_client.initialize()

            result = await ptc.invoke(
                user_message=query,
                tool_search_result=search_result,
                mcp_client=mcp_client,
            )

    # Output

    print("\nResponse:")
    print(result.response)

    print("\nMessages:")
    print(result.messages)

    print("\nToken Usage:")
    print(result.total_tokens)

    print("\nAPI Calls:")
    print(result.api_count)

    print("\nElapsed Time:")
    print(result.elapsed_time)

    tool_search.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Architecture

The project separates the system into four major layers.

### `ToolSearchModule`

Responsible for:

* Tool metadata storage
* Tool embedding generation
* Semantic retrieval
* Resolving retrieved tool names to `ToolExecutor` objects

### `ToolExecutor`

Responsible for:

* Providing a common execution interface
* Wrapping native Python callables
* Executing MCP-backed tools through an MCP client

The implementations are:

```text
ToolExecutor
    /              \
   /                \
NativeToolExecutor  MCPToolExecutor
```

### `PTCModule`

Provider-independent base class responsible for:

* Managing the PTC execution loop
* Resolving retrieved `ToolExecutor` objects
* Executing native and MCP tools
* Passing the MCP client at runtime
* Tracking turns, tokens, and execution time
* Defining the provider interface

### `PTCAnthropic`

Anthropic-specific implementation responsible for:

* Constructing Anthropic tool definitions
* Calling the Claude API
* Handling Anthropic response objects
* Handling PTC/code-execution tool calls
* Managing Anthropic container state
* Appending tool results to the conversation

The architecture allows another provider to be added later without changing the retrieval or executor layers:

```text
                         PTCModule
                       /           \
                      /             \
             PTCAnthropic         PTCOpenAI
                  │                   │
             Claude API          OpenAI API
                  │                   │
                  └────────┬──────────┘
                           │
                    ToolExecutor
                    /          \
                   /            \
             Native            MCP
```

## Current Limitations

This is currently a POC and intentionally keeps several components simple:

* Tool arguments are expected to be JSON-compatible values.
* Complex Python type deserialization is not currently implemented.
* The current MCP integration uses stdio transport.
* The PTC layer currently performs synchronous Anthropic API calls while MCP tool execution is asynchronous.

## Project Goal

The central idea is to combine **semantic tool retrieval**, **programmatic tool calling**, and **MCP-based tool execution**:

> **Retrieve only the tools relevant to the user's intent, then allow the model to programmatically compose native and MCP-backed tools to solve the task.**

This provides a foundation for experimenting with scalable tool catalogs while reducing the number of irrelevant tools exposed to the model.
