import uuid

from langchain_core.messages import HumanMessage
from langsmith import tracing_context

from app.graphs.main import supervisor
from app.graphs.states.supervisor import init_state
from app.core.session import create_user_session, get_user_session

class SupervisorService:
    """
    Service to handle the supervisor's role in the number game.
    """

    @staticmethod
    async def start_game(user_id: str, message: str):
        """
        Start the number game for a user.

        Creates the initial game state if the user session does not exist,
        or continues the game if the session is found. 
        """
        try:
            user = get_user_session(user_id)
            if user is None:
                initial_state = init_state()
                initial_state["messages"] = [HumanMessage(content=message)]
                create_user_session(user_id)

                with tracing_context(enabled=True):
                    response = await supervisor.ainvoke(
                        initial_state,
                        config={"configurable": {"thread_id": user_id}},
                    )
            else:
                with tracing_context(enabled=True):
                    response = await supervisor.ainvoke(
                        {
                            "messages": [HumanMessage(content=message)]
                        },
                        config={"configurable": {"thread_id": user_id}},
                    )

            # Check if the response contains an interrupt message
            if "__interrupt__" in response:
                return response["__interrupt__"][0].value
            
        except Exception as e:
            print(f"Error starting game for user {user_id}: {e}")
            raise
    
    def get_game_history(self, user_id: str):
        """
        Retrieve the game history for a user.

        Attempts to fetch the current game state for the given user.
        """
        try:
            config = {"configurable": {"thread_id": user_id}}
            state = supervisor.get_state(config=config)
            return {
            "correct_words": state.values.get("correct_words", 0),
            "correct_numbers": state.values.get("correct_numbers", 0),
            "number_games": state.values.get("total_number_games", 0),
            "word_games": state.values.get("total_word_games", 0),
            }
        except Exception as e:
            print(f"Error retrieving game history for user {user_id}: {e}")
            raise
        