from dotenv import load_dotenv
from pprint import pprint
import os 

load_dotenv(".env")

api_key = os.getenv("ANTHROPIC_API_KEY")
assert api_key is not None
# =====================================================
from anthropic import Anthropic

from src.ptc.PTC_Anthropic.ptcAnthropic import PTCAnthropic
from src.tool_search_module.tool_search import ToolSearchModule
from src.tools.tool_implementation import TOOLS
from src.tools.tool_ingestion import TOOL_DEFINITIONS


client = Anthropic()

MODEL = "claude-sonnet-4-5"
print(MODEL)

tool_search = ToolSearchModule(
    db_path="tools.db",
)

for tool in TOOL_DEFINITIONS:
    tool_search.add_tool(tool)
    print(f"Added {tool["name"]} to searchDB")

query = "Get me employees having salary > 30000 in engineering, and also get me their attendance data."

# Retrieve relevant tools + their Python callables
search_result = tool_search.invoke(
    query=query,
    k=8,
    TOOLS=TOOLS,
)

for i, tool in enumerate(search_result.tools):
    print(
        f"{i + 1}. "
        f"{tool['name']:<35} "
        f"{tool['score']:.4f}"
    )

print(search_result.tools_callable)

# Create PTC implementation
ptc = PTCAnthropic(
    client=client,
    model=MODEL,
)

print("Created PTC Module")

# Run Claude with only the retrieved tools
result = ptc.invoke(
    user_message=query,
    tool_search_result=search_result,
)

print("Response:")
print(result.response)

print("\nTotal tokens:")
print(result.total_tokens)

print("\nAPI calls:")
print(result.api_count)

print("\nElapsed time:")
print(result.elapsed_time)

print("\n======== Messages =========")
pprint(result.messages, indent=2, width=120)