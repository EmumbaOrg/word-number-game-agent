from langgraph.prebuilt import create_react_agent

from app.core.chat_model.main import chat_model
from app.graphs.tools.number import guess_number_tool
from app.graphs.states.number import NumberToolState

number_guessing_agent = create_react_agent(
    model=chat_model, 
    tools=[guess_number_tool],
    state_schema=NumberToolState,
    prompt="""You are part of playing a number guessing game. 
    User have already selected a number between 1 and 50.
    Your task is to use the tool in that will return question that you can ask user.
    This will narrow down the range of possible numbers.
    If you cannot access the tool, you can simply respond that I can not access the tool.
    You will not guess the number directly.
    Keep using the tool until it return status as "guessing"
    You will not ask the user to think of a number."""


)
