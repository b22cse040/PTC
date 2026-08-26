import copy, json, time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from src.tool_search_module.tool_executor import (
    MCPToolExecutor,
    ToolExecutor,
)
from src.tool_search_module.tool_search import ToolSearchResult

TURNS_LEFT = 10

@dataclass
class PTCResult:
    response : Optional[str]
    messages : List[Any]
    total_tokens : int
    elapsed_time : float
    api_count : int 

@dataclass
class PTCResponseState:
    finished: bool
    response: Optional[str] = None

class PTCModule(ABC):
    def __init__(
            self,
            model: str,
            max_tokens : int = 4000,
            truncate_data : bool = False
        ):
        self.model = model
        self.max_tokens = max_tokens 
        self.truncate_data: bool = truncate_data ## If true, a system prompt must be added to Indicate only peek the data.

    async def invoke(
        self,
        user_message: str,
        tool_search_result: ToolSearchResult,
        mcp_client: Any = None,
        ) -> PTCResult:

        """
        Execute a query using the retrieved tools.
        This contains the provider-independent PTC Lifecycle.
        Provider-specific behaviour is delegated to subclasses.
        """

        tools = self._build_tools(tool_search_result)

        messages = self._initialize_messages(
            user_message
        )

        total_tokens = 0
        api_count = 0
        start_time = time.time()

        state = self._initialize_state()

        turns_left = TURNS_LEFT 

        while turns_left > 0:
            turns_left -= 1

            response = self._create_response(
                messages=messages,
                tools=tools,
                state=state
                )

            api_count += 1

            total_tokens += self._get_token_usage(response)

            self._update_state(response=response, state=state)

            result_type = await self._process_response(
                    response=response,
                    messages=messages,
                    result=tool_search_result,
                    state=state,
                    mcp_client=mcp_client
                )

            if result_type.finished:
                elapsed_time = time.time() - start_time

                return PTCResult(
                    response = result_type.response,
                    messages=messages,
                    total_tokens = total_tokens,
                    elapsed_time=elapsed_time,
                    api_count=api_count
                )

        elapsed_time = time.time() - start_time 

        return PTCResult(
            response="Max number of PTC Turns reached",
            messages=messages,
            total_tokens=total_tokens,
            elapsed_time=elapsed_time,
            api_count=api_count
        )

    def _build_tools(
        self,
        result: ToolSearchResult
        ) -> List[Dict[str, Any]]:
        """
        Build the tool list that will be exposed to the underlying PTC implementation.
        """

        tools = copy.deepcopy(result.tools)

        for tool in tools:
            tool["allowed_callers"] = ["code_execution_20260120"]

        tools.append(
            {
                "type" : "code_execution_20260120",
                "name" : "code_execution"
            }    
        )

        return tools

    @staticmethod
    def _format_tool_result(
        result: Any
    ) -> str:
        """
        Convert a Python callable's result into a string.
        """

        if isinstance(result, list) and result:
            if isinstance(result[0], str):
                return "\n".join(result)

        if isinstance(result, (dict, list)):
            return json.dumps(result)

        return str(result)

    @staticmethod
    async def _execute_tool(
        tool_name: str,
        tool_input: Dict[str, Any],
        tool_executors: Dict[str, ToolExecutor],
        mcp_client: Any = None
    ) -> str:
        """
        Resolve and execute a retrieved ToolExecutor.

        Native tools execute through their wrapped callable while
        MCP tools execute through the supplied MCP client.
        """

        if tool_name not in tool_executors:
            raise KeyError(
                f"Tool '{tool_name}' was requested by the "
                f"model but was not present in the retrieved "
                f"tool executor dictionary."
            )

        tool_executor = tool_executors[tool_name]

        if isinstance(tool_executor, MCPToolExecutor):
            if mcp_client is None:
                raise ValueError(
                    f"MCP client is required to execute "
                    f"MCP Tool '{tool_name}'"

                )

            result = await tool_executor.execute(mcp_client=mcp_client, **tool_input)

        else:
            result = await tool_executor.execute(**tool_input)

        return PTCModule._format_tool_result(result)

    @abstractmethod
    def _initialize_messages(
        self,
        user_message: str,
    ) -> List[Any]:
        """
        Initialize the provider-specific conversation format.
        """
        pass

    @abstractmethod
    def _initialize_state(self) -> Dict[str, Any]:
        """
        Initialize provider-specific execution state.
        """
        pass

    @abstractmethod
    def _create_response(
        self,
        messages: List[Any],
        tools: List[Dict[str, Any]],
        state: Dict[str, Any],
    ) -> Any:
        """
        Make one API request to the provider.
        """
        pass

    @abstractmethod
    def _get_token_usage(
        self,
        response: Any,
    ) -> int:
        """
        Extract token usage from the provider response.
        """
        pass

    @abstractmethod
    def _update_state(
        self,
        response: Any,
        state: Dict[str, Any],
    ) -> None:
        """
        Update provider-specific state after a response.

        For Anthropic this includes things such as the
        container ID.
        """
        pass

    @abstractmethod
    async def _process_response(
        self,
        response: Any,
        messages: List[Any],
        result: ToolSearchResult,
        state: Dict[str, Any],
        mcp_client: Any
    ) -> "PTCResponseState":
        """
        Process a provider response.

        The implementation is responsible for:

        1. Detecting whether the model finished.
        2. Detecting tool calls.
        3. Executing retrieved callables.
        4. Appending provider-specific messages.
        """
        pass