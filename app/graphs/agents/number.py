from langgraph.prebuilt import create_react_agent

from app.core.chat_model.main import chat_model
from app.graphs.tools.number import guess_number_tool
from app.graphs.states.number import NumberToolState

number_guessing_agent = create_react_agent(
    model=chat_model, 
    tools=[guess_number_tool],
    state_schema=NumberToolState,
    prompt="""You are participating in a number guessing game. 
    The user has already selected a number between 1 and 50.
    Your objective is to utilize the provided tool to generate questions for the user, 
    which will help narrow down the possible range of numbers.
    If you are unable to access the tool, respond by stating that you cannot access the tool.
    Do not attempt to guess the number directly.
    Continue using the tool until its returned status is "guessing".
    Do not instruct the user to think of a number."""
)
