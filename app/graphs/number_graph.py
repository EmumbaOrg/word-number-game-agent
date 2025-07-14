from langgraph.graph import StateGraph, START, END

from app.graphs.edges.number import end_number_game_edge
from app.graphs.nodes.number import choose_number, guessing_number, number_question_user, end_number_game, final_number_guess
from app.graphs.states.number import NumberGameState

num_graph_builder = StateGraph(NumberGameState)

num_graph_builder.add_node("choose_number", choose_number)
num_graph_builder.add_node("number_agent", guessing_number)
num_graph_builder.add_node("number_question_user", number_question_user)
num_graph_builder.add_node("final_number_guess", final_number_guess)
num_graph_builder.add_node("end_number_game", end_number_game)

num_graph_builder.add_edge(START, "choose_number")
num_graph_builder.add_edge("choose_number", "number_agent")
num_graph_builder.add_conditional_edges("number_agent", end_number_game_edge, {
    "final_number_guess": "final_number_guess",
    "number_question_user": "number_question_user",
})
num_graph_builder.add_edge("number_question_user", "number_agent")
num_graph_builder.add_edge("final_number_guess", "end_number_game")
num_graph_builder.add_edge("end_number_game", END)

num_game_graph = num_graph_builder.compile()