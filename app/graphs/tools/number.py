from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain_core.messages import ToolMessage

from app.graphs.states.number import NumberToolState

@tool("guess_number", description="Guess the number based on user feedback. Ask if its number is greater")
def guess_number_tool(state: Annotated[NumberToolState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    """
    Tool to guess the number based on the user's feedback.
    """

    low = state["low_bound"]
    high = state["upper_bound"]
    
    # Calculate the middle point for the guess
    current_guess = (low + high) // 2
    
    user_answer = state.get("user_answer", None)
    # If this is the first guess or no previous answer

    if user_answer is None:
        return Command(update={
            "current_guess": current_guess,
            "game_in_progress": True,
            "guess_count": state["guess_count"] + 1,
            "messages": [
                ToolMessage(
                    content=f"Is the number you are thinking of greater than {current_guess}?",
                    tool_call_id=tool_call_id
                )
            ]
        })

    # Process previous answer
    user_response = state["user_answer"].strip().lower()
    if user_response == "yes":
        low = current_guess + 1
    elif user_response == "no":
        high = current_guess

    # Calculate next guess
    next_guess = (low + high) // 2
    game_continues = low < high

    
    return Command(update={
        "current_guess": next_guess,
        "game_in_progress": game_continues,
        "guess_count": state["guess_count"] + 1,
        "low_bound": low,
        "upper_bound": high,
        "messages": [
            ToolMessage({
                "status": "guessing" if not game_continues else "questioning",
                "content": f"Is the number you are thinking of greater than {next_guess}?" if game_continues else f"The number must be {next_guess}!",
            }, tool_call_id=tool_call_id)
        ]
    })
