import uuid

from langgraph.types import Command

from app.graphs.main import supervisor

class NumberGameService:

    async def number_slected(self, user_will: str, user_id: str):
        
        config = {"configurable": {"thread_id": user_id}}
        response = await supervisor.ainvoke(
            Command(resume=user_will), 
            config=config,
        )

        print(f"Response from number_slected: {response}")
        if "__interrupt__" in response:
            return {"message": response["__interrupt__"][0].value}
    
    async def guess_number(self, user_input: str, user_id: str):
        """
        Handles the user's guess in the number guessing game.
        This method processes the user's input and returns a response based on the game state.
        """
        config = {"configurable": {"thread_id": user_id}}
        
        # Invoke the number guessing graph with the user's input
        response = await supervisor.ainvoke(
            Command(resume=user_input), 
            config=config,
        )

        if "__interrupt__" in response:
            return {"message": response["__interrupt__"][0].value}
        else:
            return {
                "message": response["messages"][-1].content if response["messages"] else "No messages returned.",
                "status": "success",   
                }