from typing import Literal, Optional
from langgraph.graph import MessagesState
from langgraph.prebuilt.chat_agent_executor import AgentState


class NumberGameState(MessagesState):
  current_guess: int
  user_answer: Optional[Literal["yes", "no", "YES", "NO"]] = None
  low_bound: int
  upper_bound: int
  guess_count: int
  game_in_progress: bool

class NumberToolState(AgentState, NumberGameState):
    pass


def num_init_state() -> NumberGameState:
    return NumberGameState(
        current_guess=0,
        low_bound=1,
        upper_bound=50,
        guess_count=0,
        game_in_progress=False,
        user_answer=None,
    )