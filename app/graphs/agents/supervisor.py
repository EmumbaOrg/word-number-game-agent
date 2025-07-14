from langgraph.prebuilt import create_react_agent

from app.core.chat_model.main import chat_model
from app.graphs.tools.supervisor import handoff_to_number_graph, handoff_to_word_graph

supervisor_agent = create_react_agent(
    model=chat_model,
    tools=[handoff_to_number_graph, handoff_to_word_graph],
    prompt=(
        """
        You are a supervisor managing two specialized agents:

        #### Available Graphs:
            - `word graph`: Handles all tasks related to word games.
            - `number graph`: Handles number game tasks.

        #### Instructions:
            1. If the user's message includes `"number"`, `"guess number"` or similar → assign to **number graph**.
            2. If the user's message includes `"word"`, `"guess word"` or similar → assign to **word graph**.
            4. Only assign **one graph at a time**. Do not assign graphs in parallel.
            5. **Do not do any work yourself. Only delegate.**
            6. Do not start game by yourself, If one game ends, ask user if he/she wants to play another game or not.

        #### One-Shot Example:
            - User: "I want to play a word guessing game."
            - Supervisor: Hand off to `word graph`.
"""
    ),
    name="supervisor",
)