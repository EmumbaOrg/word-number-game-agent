from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.graphs.states.supervisor import SupervisorState
from app.graphs.agents.supervisor import supervisor_agent
from app.graphs.nodes.supervisor import num_sub_graph, word_sub_graph


checkpointer = InMemorySaver()

supervisor = (
    StateGraph(SupervisorState)
    # NOTE: `destinations` is only needed for visualization and doesn't affect runtime behavior
    .add_node(supervisor_agent, destinations=("number_graph", "word_graph", END))
    .add_node("number_graph", num_sub_graph)
    .add_node("word_graph", word_sub_graph)
    .add_edge(START, "supervisor")
    # always return back to the supervisor
    .add_edge("number_graph", "supervisor")
    .add_edge("word_graph", "supervisor")
    .compile(checkpointer=checkpointer)
)


print("Supervisor graph compiled successfully.")
print(supervisor.get_graph().draw_mermaid())