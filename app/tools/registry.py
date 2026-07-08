from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

from openai.types.chat import ChatCompletionFunctionToolParam

from app.tools.calculator import add_numbers, multiply_numbers

ToolHandler = Callable[..., Any]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: ToolHandler

    def to_openai_tool(self) -> ChatCompletionFunctionToolParam:
        return cast(
            ChatCompletionFunctionToolParam,
            {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": self.parameters,
                },
            },
        )


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def to_openai_tools(self) -> list[ChatCompletionFunctionToolParam]:
        return [tool.to_openai_tool() for tool in self._tools.values()]

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        tool = self._tools.get(tool_name)

        if tool is None:
            raise RuntimeError(f"Unknown tool: {tool_name}")

        return tool.handler(**arguments)


def create_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="add_numbers",
            description="Add two numbers and return the result.",
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            handler=add_numbers,
        )
    )

    registry.register(
        ToolDefinition(
            name="multiply_numbers",
            description="Multiply two numbers and return the result.",
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            handler=multiply_numbers,
        )
    )

    return registry
