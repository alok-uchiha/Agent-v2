from langchain.agents import AgentState
from dataclasses import dataclass


class MyState(AgentState):
    user_id:int

@dataclass
class MyContext:
    user_id:int