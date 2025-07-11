from langgraph.prebuilt import create_react_agent

from app.core.chat_model.main import chat_model
from app.graphs.tools.supervisor import handoff_to_number_graph, handoff_to_word_graph

supervisor_agent = create_react_agent(
    model=chat_model,
    tools=[handoff_to_number_graph, handoff_to_word_graph],
    prompt=(
        "You are a supervisor managing three agents:\n"
        "- a word graph. Assign any word game related task to this graph\n"
        "- a number graph. Assign number game tasks to this graph when something is mentioned about number game\n"
        "- an exit graph. If the user wants to exit, assign this graph\n"
        "Instructions:\n"
        "If the user's message contains 'number', 'guess number', or similar, hand off to the number graph.\n"
        "If the user's message contains 'word', 'guess word', or similar, hand off to the word graph.\n"
        "If the user wants to exit, hand off to the exit graph.\n"
        "Assign work to one graph at a time, do not call graphs in parallel.\n"
        "Do not do any work yourself."
    ),
    name="supervisor",
)