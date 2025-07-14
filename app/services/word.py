import logging
from langgraph.types import Command
from langsmith import tracing_context
from app.graphs.main import supervisor

logger = logging.getLogger(__name__)

class WordGameService:
    """
    Service class for handling word game operations such as word selection and guessing.
    """

    async def word_selected(self, user_will: str, user_id: str):
        """
        Processes the user's selected word in the word game.

        Args:
            user_will (str): The word or command selected by the user.
            user_id (str): The unique identifier for the user.

        Returns:
            dict: A response message if an interrupt occurs.

        Raises:
            Exception: Propagates any exception that occurs during processing.
        """
        try:
            config = {"configurable": {"thread_id": user_id}}
            
            with tracing_context(enabled=True):
                response = await supervisor.ainvoke(
                    Command(resume=user_will), 
                    config=config,
                )

            if "__interrupt__" in response:
                return {"message": response["__interrupt__"][0].value}
        except Exception as e:
            logger.error("Error in word_selected: %s", e, exc_info=True)
            raise

    async def guess_word(self, user_input: str, user_id: str):
        """
        Handles the user's guess in the word guessing game.

        Args:
            user_input (str): The user's guess or input.
            user_id (str): The unique identifier for the user.

        Returns:
            dict: A response message and status based on the game state.

        Raises:
            Exception: Propagates any exception that occurs during processing.
        """
        try:
            config = {"configurable": {"thread_id": user_id}}
            
            # Invoke the word guessing graph with the user's input
            with tracing_context(enabled=True):
                response = await supervisor.ainvoke(
                    Command(resume=user_input), 
                    config=config,
                )

            if "__interrupt__" in response:
                return {"message": response["__interrupt__"][0].value, "status": "guessing"}
            else:
                return {
                    "message": response["messages"][-1].content if response["messages"] else "No messages returned.",
                    "status": "success",   
                }
        except Exception as e:
            logger.error("Error in guess_word: %s", e, exc_info=True)
            raise