from langgraph.types import interrupt, Command
from langgraph.graph import  END
from langchain_core.messages import AIMessage, HumanMessage

from app.graphs.states.number import NumberGameState, num_init_state
from app.graphs.states.supervisor import SupervisorState
from app.graphs.agents.number import number_guessing_agent

def choose_number(state: NumberGameState) -> NumberGameState:
    """
    Initializes the number guessing game by prompting the user to think of a number within the specified bounds.
    Updates the game state to indicate the game is in progress and appends relevant messages to the conversation history.
    Args:
        state (NumberGameState): The current state of the number guessing game, including bounds and messages.
    Returns:
        NumberGameState: The updated game state after initialization.
    """
    low = state["low_bound"]
    high = state["upper_bound"]

    state["messages"].append(AIMessage(content="Let's play a number guessing game! I will try to guess the number you are thinking of."))
    interrupt(
        f"Think of a number between {low} and {high} (inclusive). I will try to guess it!"
    )

    state["game_in_progress"] = True
    state["messages"].append(HumanMessage(content=f"I have selected a number between {state['low_bound']} and {state['upper_bound']}. You can start guessing."))
    return state



async def guessing_number(state: NumberGameState, config) -> NumberGameState:
    """
    Node in the LangGraph graph responsible for invoking the guessing agent (react agent) to make a guess based on the current game state.
    Args:
        state (NumberGameState): The current state of the number game.
        config: Configuration parameters for the guessing agent.
    Returns:
        NumberGameState: Returns the updated game state after the agent's guess.
    """
    
    response = await number_guessing_agent.ainvoke(
        state,
        config=config,
    )
    return response


def number_question_user(state: NumberGameState) -> NumberGameState:
    """
    Node function that interacts with the user to get feedback on the agent's guess.
    This function prompts the user for input, appends the response to the conversation history,
    and updates the game state with the user's answer.
    Args:
        state (NumberGameState): The current state of the number guessing game.
    Returns:
        NumberGameState: The updated game state with the user's response.
    """

    response = interrupt(
        state["messages"][-1].content
    )
    state["messages"].append(HumanMessage(content=response))
    state["user_answer"] = response.strip().lower()
    return state

def end_number_game(state: SupervisorState):
    """
    Node function to end the number guessing game.
    It updates the game state to indicate that the game is no longer in progress and appends a final message to the conversation history.
    Args:
        state (NumberGameState): The current state of the number guessing game.
    Returns:
        Union[Command, NumberGameState]: A Command to end the game or the updated game state.
    """
    num_state = num_init_state()
    state["total_number_games"] += 1
    state["correct_words"] += 1 
    
    state = {
        **state,  # Unpack the SupervisorState to include all fields
        **num_state,  # Reset number game state
    }
    state["messages"].append(AIMessage(content=state["messages"][-1].content))
    return Command(goto=END, update=state)