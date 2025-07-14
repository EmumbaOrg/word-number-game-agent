from langgraph.graph import StateGraph, START, END

from app.graphs.nodes.word import choose_word, guessing_word, word_question_user, end_word_game, final_guess
from app.graphs.states.word import WordGameState
from app.graphs.edges.word import make_final_guess


word_graph_builder = StateGraph(WordGameState)
word_graph_builder.add_node("choose_word", choose_word)
word_graph_builder.add_node("guessing_word", guessing_word)
word_graph_builder.add_node("word_question_user", word_question_user)
word_graph_builder.add_node("final_guess", final_guess)
word_graph_builder.add_node("end_word_game", end_word_game)


word_graph_builder.add_edge(START, "choose_word")
word_graph_builder.add_edge("choose_word", "guessing_word")
word_graph_builder.add_conditional_edges("guessing_word", make_final_guess, {
    "final_guess": "final_guess",
    "word_question_user": "word_question_user"
})

word_graph_builder.add_edge("word_question_user", "guessing_word")
word_graph_builder.add_edge("final_guess", "end_word_game")
word_graph_builder.add_edge("end_word_game", END)

word_game_graph = word_graph_builder.compile()