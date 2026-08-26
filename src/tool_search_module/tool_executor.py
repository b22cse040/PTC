"""
The purpose of this file is to form an abstraction for the tool execution methods.
If the tool is natively implemented, in that case we can invoke the tool with the help of Callable(**args)

For MCP we'll need to process.
"""
from abc import ABC, abstractmethod 
from typing import Any, Callable

## Tool Executors are globally mainatained at src/tools/tool_executors.py

class ToolExecutor(ABC):
    
    @abstractmethod
    async def execute(self, **args) -> Any:
        ...

## Native Tool-Executor is just a wrapper over the Callable for 
## that function
class NativeToolExecutor(ToolExecutor):
    def __init__(self, fn: Callable):
        self.fn = fn 

    async def execute(self, **args) -> Any:
        return self.fn(**args)

## MCPToolExecutor utilizes the mcp-client and invokes the fn
class MCPToolExecutor(ToolExecutor):
    def __init__(self, name: str):
        self.name = name 
        
    async def execute(
        self,
        mcp_client,
        **args
        ) -> Any:
        result = await mcp_client.call_tool(self.name, args)
        ## return str(result)
        return result.structured_content["result"]