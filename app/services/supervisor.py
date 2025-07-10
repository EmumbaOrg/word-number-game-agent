import uuid

from langchain_core.messages import HumanMessage

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
        Start the number game by creating the initial state and returning the command.
        """
        
        try:
            user = get_user_session(user_id)
            if user is None:
                initial_state = init_state()
                initial_state["messages"] = [HumanMessage(content=message)]
                create_user_session(user_id)
                response = await supervisor.ainvoke(
                    initial_state,
                    config={"configurable": {"thread_id": user_id}},
                )
            else:
                response = await supervisor.ainvoke(
                    {
                        "messages": [HumanMessage(content=message)]
                    },
                    config={"configurable": {"thread_id": user_id}},
                )
            if "__interrupt__" in response:
                return response["__interrupt__"][0].value
        except Exception as e:
            print(f"Error starting game: {e}")
            return {"status": "error", "message": str(e)}
            
    
    def get_game_history(self, user_id: str):
        """
        Retrieve the game history for a user.
        This is a placeholder implementation. Replace with actual logic to retrieve game history.
        """
        config={"configurable": {"thread_id": user_id}}
        state = supervisor.get_state(config=config)
        
        return {
            "correct_words": state.values.get("correct_words", 0),
            "correct_numbers": state.values.get("correct_numbers", 0),
            "number_games": state.values.get("total_number_games", 0),
            "word_games": state.values.get("total_word_games", 0),
        }
        