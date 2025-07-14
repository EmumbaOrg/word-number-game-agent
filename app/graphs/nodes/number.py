from langgraph.types import interrupt, Command
from langgraph.graph import  END
from langchain_core.messages import AIMessage, HumanMessage

from app.graphs.states.number import NumberGameState
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

def final_number_guess(state: NumberGameState) -> NumberGameState:
    """
    Node that interrupts the flow to present the agent's final guess to the human user and asks if the guess is correct.
    The user's answer is then used to update the state with whether the guess was correct.

    Args:
        state (NumberGameState): The current state of the number guessing game.

    Returns:
        NumberGameState: The updated game state after recording the correctness of the guess.
    """
    guess = state.get("current_guess", None)
    if guess:
        response = interrupt(f"My guess is: '{guess}'. Is this correct? (yes/no)")
        state["messages"].append(HumanMessage(content=response))
        state["is_number_correct"] = response.strip().lower() == "yes"
    return state

def end_number_game(state: NumberGameState) -> Command:
    """
    Node function to end the number guessing game.
    Updates stats, resets number game state, and appends a final message.

    Args:
        state (NumberGameState): The current state of the number guessing game.

    Returns:
        Command: A Command to end the game with the updated state.
    """
    # state["total_number_games"] += 1
    # is_number_correct = state.get("is_number_correct", None)
    # if is_number_correct:
    #     state["correct_numbers"] = state.get("correct_numbers", 0) + 1

    state["messages"] = [AIMessage(content="The number guessing game has ended. Thank you for playing!")]
    
    return Command(
        goto=END,
        update=state
    )