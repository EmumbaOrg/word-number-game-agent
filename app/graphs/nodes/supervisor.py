from app.graphs.states.supervisor import SupervisorState
from app.graphs.states.number import NumberGameState, num_init_state
from app.graphs.states.word import WordGameState, word_init_state
from app.graphs.number_graph import num_game_graph
from app.graphs.word_graph import word_game_graph
import logging

logger = logging.getLogger(__name__)

async def num_sub_graph(state: SupervisorState, config) -> SupervisorState:
    """
    Determine the sub-graph to transition to based on the current state.
    """

    init_state = num_init_state()
    response: NumberGameState = await num_game_graph.ainvoke({
        **init_state
    }, config=config)
    state["total_number_games"] += 1
    if response["is_number_correct"]:
        state["correct_numbers"] += 1
        
    state["messages"] = response["messages"]
    return state



async def word_sub_graph(state: SupervisorState, config) -> SupervisorState:
    """
    Determine the sub-graph to transition to based on the current state.
    """
    init_state = word_init_state()
    response: WordGameState = await word_game_graph.ainvoke({
        **init_state
    }, config=config)
    state["total_word_games"] += 1
    if response["is_word_correct"]:
        state["correct_words"] += 1
    
    state["messages"] = response["messages"]
    return state