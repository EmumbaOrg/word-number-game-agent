import uuid
import logging

from langgraph.types import Command

from app.graphs.main import supervisor

logger = logging.getLogger(__name__)

class NumberGameService:
    
    async def number_slected(self, user_will: str, user_id: str):
        """
        Handles the user's selection in the number game.

        Args:
            user_will (str): The user's selected number or will.
            user_id (str): The unique identifier for the user.

        Returns:
            dict: A message dict if interrupted, otherwise None.

        Raises:
            Exception: Propagates any exception encountered during processing.
        """
        try:
            config = {"configurable": {"thread_id": user_id}}
            response = await supervisor.ainvoke(
                Command(resume=user_will), 
                config=config,
            )

            if "__interrupt__" in response:
                return {"message": response["__interrupt__"][0].value}
        
        except Exception as e:
            logger.error(f"Error in number_slected: {e}")
            raise

    async def guess_number(self, user_input: str, user_id: str):
        """
        Handles the user's guess in the number guessing game.

        Args:
            user_input (str): The user's guess input.
            user_id (str): The unique identifier for the user.

        Returns:
            dict: A message dict with the result and status.

        Raises:
            Exception: Propagates any exception encountered during processing.
        """
        try:
            config = {"configurable": {"thread_id": user_id}}
            
            # Invoke the number guessing graph with the user's input
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
            logger.error(f"Error in guess_number: {e}")
            raise