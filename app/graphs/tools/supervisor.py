from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.types import Command

from app.graphs.states.number import num_init_state 
from app.graphs.states.word import word_init_state


def create_handoff_tool(*, sub_graph_name: str, description: str | None = None):
    name = f"transfer_to_{sub_graph_name}"
    description = description or f"Ask {sub_graph_name} for help."

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {sub_graph_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        if sub_graph_name == "number_graph":
            init_state = num_init_state()
        else:
            init_state = word_init_state()
        return Command(
            goto=sub_graph_name,  
            update={**init_state},  
            graph=Command.PARENT,  
        )

    return handoff_tool


# Handoffs
handoff_to_number_graph = create_handoff_tool(
    sub_graph_name="number_graph",
    description="Give control to the number guessing agent.",
)

handoff_to_word_graph = create_handoff_tool(
    sub_graph_name="word_graph",
    description="Give control to the word guessing agent.",
)