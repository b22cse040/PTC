import json 
from typing import Any, Dict, List

from openai import OpenAI

from src.ptc.PTC import PTCModule, PTCResponseState
from src.tool_search_module.tool_search import ToolSearchResult

class PTCOpenAI(PTCModule):
    def __init__(self, client: OpenAI, model: str, max_tokens: int = 4000, truncate_data: bool = False):
        super().__init__(model=model, max_tokens=max_tokens, truncate_data=truncate_data)

        self.client = client 

    def _initialize_messages(self, user_message: str) -> List[Any]:
        return [
            {
                "role" : "user",
                "content" : user_message
            }    
        ]

    def _initialize_state(self) -> Dict[str, Any]:
        return {}

    def _create_response(self, messages: List[Any], tools: List[Dict[str, Any]], state: Dict[str, Any]) -> Any:
        request_params = {
            "model" : self.model,
            "input" : messages,
            "tools" : tools,
            "store" : False
        }

        if self.truncate_data:
            request_params["instructions"] = (
                "When inspecting tool results or datasets, only inspect the data needed to answer the "
                "user's query. Do not return or process the entire dataset unless explicitly requested."
            )

        return self.client.responses.create(**request_params)

    def _get_token_usage(self, response: Any) -> int:
        if response.usage is None:
            return 0

        return response.usage.input_tokens + response.usage.output_tokens

    def _update_state(self, response: Any, state: Dict[str, Any]) -> None:
        ## openAI PTC does not require provider-side state here because we use
        ## store=False and relplay response itmes.
        pass

    async def _process_response(
        self,
        response: Any,
        messages: List[Any],
        result: ToolSearchResult,
        state: Dict[str, Any],
        mcp_client: Any = None
    ) -> PTCResponseState:
        if response.status != "completed":
            return PTCResponseState(finished=True, response=f"Response ended with status: {response.status}")

        # OpenAI requires us to preserve EVERY response output item, including program/reasoning/function_call/program_output items
        messages.extend(item.model_dump(exclude_none=True) for item in response.output)

        function_calls = [item for item in response.output if item.type == "function_call"]

        if not function_calls:
            message = next((
                    item for item in response.output if item.type == "message"
                ), None)

            if message is not None:
                return PTCResponseState(finished=True, response=response.output_text or self._get_refusal(message))

            ## in case of no final assistant message
            return PTCResponseState(finished=False)

        for call in function_calls:
            tool_name = call.name
            tool_input = json.loads(call.arguments)

            caller = call.caller.model_dump(exclude_none=True) if call.caller is not None else None

            if caller is not None and caller.get("type") == "program":
                print(f"[PTC] Tool called from program: {tool_name}")

            else:
                print(f"[PTC DirectTool called by model: {tool_name}")

            content = await self._execute_tool(
                tool=tool_name,
                tool_input=tool_input,
                tool_executors=result.tool_executors,
                mcp_client=mcp_client,
            )

            messages.append(
                {
                    "type" : "function_call_output",
                    "call_id" : call.call_id,
                    "output" : content,
                    "caller" : caller,
                }    
            )

        return PTCResponseState(finished=False)

    @staticmethod 
    def _get_refusal(message: Any) -> str:
        for content in message.content:
            if content.type == "refusal":
                return content.refusal

        return ""

    def _build_tools(self, result: ToolSearchResult) -> List[Dict[str, Any]]:
        ptc_tools: List[Dict[str, Any]] = []

        ## "Invalid schema for function <tool-name>: In context=(), 'additionalProperties' is required to be supplied 
        ## and to be false."
        for tool in result.tools:
            parameters = tool["input_schema"].copy()

            if parameters.get("type") == "object":
                parameters["additionalProperties"] = False

            ptc_tool = {
                "type" : "function",
                "name" : tool["name"],
                "description" : tool["description"],
                "parameters" : parameters,
                "output_schema" : tool["output_schema"],
                "allowed_callers" : ["programmatic"],
                "strict" : True,
            }

            ptc_tools.append(ptc_tool)

        ptc_tools.append({"type" : "programmatic_tool_calling"})
        return ptc_tools