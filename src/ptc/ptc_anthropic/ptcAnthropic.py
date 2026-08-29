from typing import Any, Dict, List

from anthropic import Anthropic
from anthropic.types.beta import BetaTextBlock, BetaToolUseBlock
from dotenv import load_dotenv

from src.ptc.PTC import PTCModule, PTCResponseState
from src.tool_search_module.tool_search import ToolSearchResult


load_dotenv(".env")


class PTCAnthropic(PTCModule):

    def __init__(self, client: Anthropic, model: str, max_tokens: int = 4000, truncate_data: bool = False):
        super().__init__(model=model, max_tokens=max_tokens)

        self.client = client
        self.truncate_data = truncate_data

    def _initialize_messages(self, user_message: str) -> List[Any]:

        messages = []

        # if self.truncate_data:
        #     messages.append({
        #         # "role": "system",
        #         # "content": (
        #         #     "When inspecting tool results or datasets, "
        #         #     "only peek at the data needed to answer the "
        #         #     "user's query. Do not return or process the "
        #         #     "entire dataset unless explicitly requested."
        #         # ),
           
        #     })

        messages.append({
            "role": "user",
            "content": user_message,
        })

        return messages

    def _initialize_state(self) -> Dict[str, Any]:
        return {"container_id": None}

    def _create_response(self, messages: List[Any], tools: List[Dict[str, Any]], state: Dict[str, Any]):

        request_params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "tools": tools,
            "messages": messages,
        }

        if self.truncate_data:
            SYSTEM_PROMPT = ("When inspecting tool results or datasets, "
            "only peek at the data needed to answer the "
            "user's query. Do not return or process the "
            "entire dataset unless explicitly requested.")

            request_params["system"] = SYSTEM_PROMPT

        container_id = state.get("container_id")

        return self.client.beta.messages.create(
            **request_params,
            betas=["advanced-tool-use-2025-11-20"],
            extra_body={"container": container_id} if container_id else None,
        )

    def _get_token_usage(self, response: Any) -> Dict[str, int]:
        ## return response.usage.input_tokens + response.usage.output_tokens
        return {
            "input-tokens" : response.usage.input_tokens,
            "output-tokens" : response.usage.output_tokens,
            "total-tokens" : response.usage.input_tokens + response.usage.output_tokens
        }

    def _update_state(self, response: Any, state: Dict[str, Any]) -> None:

        if hasattr(response, "container") and response.container:
            state["container_id"] = response.container.id

    async def _process_response(
        self,
        response: Any,
        messages: List[Any],
        result: ToolSearchResult,
        state: Dict[str, Any],
        mcp_client: Any = None,
    ) -> PTCResponseState:

        # Model finished

        if response.stop_reason == "end_turn":

            final_response = "\n".join(
                block.text
                for block in response.content
                if isinstance(block, BetaTextBlock)
            )

            return PTCResponseState(finished=True, response=final_response)

        # Model requested tool usage

        if response.stop_reason == "tool_use":

            messages.append({
                "role": "assistant",
                "content": response.content,
            })

            tool_results = []

            for block in response.content:

                if not isinstance(block, BetaToolUseBlock):
                    continue

                tool_name = block.name
                tool_input = block.input
                tool_use_id = block.id
                caller_type = block.caller.type

                if caller_type == "code_execution_20250825":
                    print(f"[PTC] Tool called from code execution environment: {tool_name}")

                elif caller_type == "direct":
                    print(f"[Direct] Tool called by model: {tool_name}")

                content = await self._execute_tool(
                    tool_name=tool_name,
                    tool_input=tool_input,
                    tool_executors=result.tool_executors,
                    mcp_client=mcp_client,
                )

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": content,
                })

            messages.append({
                "role": "user",
                "content": tool_results,
            })

            return PTCResponseState(finished=False)

        # Unexpected stop reason

        final_response = next(
            (
                block.text
                for block in response.content
                if isinstance(block, BetaTextBlock)
            ),
            f"Stopped with reason: {response.stop_reason}",
        )

        return PTCResponseState(finished=True, response=final_response)

    def _build_tools(self, result: ToolSearchResult) -> List[Dict[str, Any]]:

        ptc_tools: List[Dict[str, Any]] = []

        for tool in result.tools:

            ptc_tool = {
                "name": tool["name"],
                "description": tool["description"],
                "input_schema": tool["input_schema"],
                "allowed_callers": ["code_execution_20250825"],
            }

            if "input_example" in tool:
                ptc_tool["input_examples"] = [tool["input_example"]]

            ptc_tools.append(ptc_tool)

        ptc_tools.append({
            "type": "code_execution_20250825",
            "name": "code_execution",
        })

        return ptc_tools