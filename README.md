# Programmatic Tool Calling POC

A proof-of-concept framework for **semantic tool retrieval and programmatic tool calling (PTC)** with Claude.

## Aim

The goal of this project is to avoid exposing an LLM to an entire tool catalog for every query.

Instead, the system:

1. Semantically searches the available tools.
2. Retrieves only the most relevant tools for the user's query.
3. Resolves those tools to their actual Python callables.
4. Passes the retrieved tools to Claude's Programmatic Tool Calling interface.
5. Executes the requested Python functions.
6. Feeds the results back to Claude until it produces a final response or reaches the turn limit.

This allows the PTC layer to work with a **dynamic subset of tools** rather than the complete tool registry.

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
                  tools        tools_callable
                    │                 │
                    ▼                 ▼
              Tool Metadata      Python Functions
                    │                 │
                    └────────┬────────┘
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
                     Python Callable
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

### 1. Tool Registration

Each tool is represented using metadata such as:

```python
{
    "name": "search_employees",
    "description": "Search employees using optional department and salary filters.",
    "input-schema": {...},
    "input_example": {...}
}
```

The Python implementation is maintained separately:

```python
TOOLS = {
    "search_employees": search_employees,
    ...
}
```

This separates **tool metadata exposed to the model** from the **actual executable Python functions**.

### 2. Semantic Tool Search

`ToolSearchModule` creates an embedding using only the tool's name and description:

```text
[CLS] tool[name] [SEP] tool[description]
```

The embedding is stored alongside the tool's database ID.

When a user sends a query, the query is embedded and compared against the stored tool embeddings. The top-`k` relevant tools are returned.

The database stores the remaining metadata (`input_schema`, `input_example`) using the tool ID.

### 3. ToolSearchResult

Every search returns:

```python
@dataclass
class ToolSearchResult:
    tools: List[Dict[str, Any]]
    tools_callable: Dict[str, Callable]
```

`tools` contains the metadata retrieved from the database, while `tools_callable` maps those tool names to their actual Python implementations.

### 4. Programmatic Tool Calling

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

When Claude requests a tool call, the PTC module resolves the tool name against:

```python
result.tools_callable
```

and executes the corresponding Python function.

The tool result is then returned to Claude, allowing it to continue reasoning and make additional tool calls if necessary.

The PTC loop currently allows a maximum of:

```python
TURNS_LEFT = 10
```

turns.

## Usage

### 1. Create the Tool Search Module

```python
from src.tool_search_module.tool_search import ToolSearchModule
from src.tools.tool_implementation import TOOLS


tool_search = ToolSearchModule(
    db_path="tools.db",
)
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
query = "Get me employees having salary > 30000 in engineering"

search_result = tool_search.invoke(
    query=query,
    k=3,
    TOOLS=TOOLS,
)
```

The result contains both:

```python
search_result.tools
```

and:

```python
search_result.tools_callable
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
    model="claude-sonnet-4-20250514",
)
```

### 5. Execute the Query

Pass the `ToolSearchResult` directly to the PTC module:

```python
result = ptc.invoke(
    user_message=query,
    result=search_result,
)
```

The final response can be accessed using:

```python
print(result.response)
```

Additional execution information is available through:

```python
print(result.messages)
print(result.total_tokens)
print(result.elapsed_time)
print(result.api_count)
```

## Complete Example

```python
from anthropic import Anthropic

from src.tool_search_module.tool_search import ToolSearchModule
from src.tools.tool_implementation import TOOLS
from src.ptc.PTC_Anthropic.ptcAnthropic import PTCAnthropic


query = "Get me employees having salary > 30000 in engineering"


# ------------------------------------------------------------
# Tool Retrieval
# ------------------------------------------------------------

tool_search = ToolSearchModule(
    db_path="tools.db",
)

search_result = tool_search.invoke(
    query=query,
    k=3,
    TOOLS=TOOLS,
)


# ------------------------------------------------------------
# Claude PTC
# ------------------------------------------------------------

client = Anthropic()

ptc = PTCAnthropic(
    client=client,
    model="claude-sonnet-4-20250514",
)

result = ptc.invoke(
    user_message=query,
    result=search_result,
)


# ------------------------------------------------------------
# Output
# ------------------------------------------------------------

print("\n======== Response =========")
print(result.response)

print("\n======== Messages =========")
print(result.messages)

print("\n======== Token Usage =========")
print(result.total_tokens)

print("\n======== API Calls =========")
print(result.api_count)

print("\n======== Elapsed Time =========")
print(result.elapsed_time)
```

## Architecture

The project separates the system into three major components.

### `ToolSearchModule`

Responsible for:

* Tool metadata storage
* Tool embedding generation
* Semantic retrieval
* Resolving retrieved tool names to Python callables

### `PTCModule`

Provider-independent base class responsible for:

* Managing the PTC execution loop
* Executing retrieved Python callables
* Tracking turns, tokens, and execution time
* Defining the provider interface

### `PTCAnthropic`

Anthropic-specific implementation responsible for:

* Constructing Anthropic tool definitions
* Calling the Claude API
* Handling Anthropic response objects
* Handling PTC/code-execution tool calls
* Managing Anthropic container state

The architecture allows another provider to be added later without changing the retrieval layer:

```text
                    PTCModule
                    /        \
                   /          \
        PTCAnthropic        PTCOpenAI
              │                   │
          Claude API          OpenAI API
```

## Current Limitations

This is currently a POC and intentionally keeps several components simple:

* Vector search currently performs brute-force similarity search over stored embeddings.
* Tool arguments are expected to be JSON-compatible values.
* Complex Python type deserialization is not currently implemented.
* The PTC execution loop has a fixed maximum of 10 turns.
* Tool retrieval quality depends on the embedding model and tool descriptions.

## Project Goal

The central idea is to combine **tool retrieval** with **programmatic tool calling**:

> **Retrieve only the tools that are relevant to the user's intent, then allow the model to programmatically compose those tools to solve the task.**

This provides a foundation for experimenting with scalable tool catalogs while reducing the number of irrelevant tools exposed to the model.
