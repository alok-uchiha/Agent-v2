import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain.agents.middleware import before_model, SummarizationMiddleware
from langchain_core.messages import trim_messages

from backend.app.ai.tools.tool import (
    get_info,
    get_order,
    cancel_order,
    check_payment,
    get_user,
    save_memory,
    get_memory
)
from backend.app.ai.tools.knowledge_base_tool import search_knowledge_base
from backend.app.ai.schemas import MyContext, MyState



load_dotenv()
os.environ["OPENROUTER_API_KEY"]=os.getenv("OPENROUTER_API_KEY")


trimmer = trim_messages(
    max_tokens=100,
    strategy="last",
    start_on="human",
    include_system=True,
    token_counter="approximate"
)

@before_model
def trim_history(state, runtime):
    trimmed = trimmer.invoke(state["messages"])

    print(
        f"Before: {len(state["messages"])}",
        f"After: {len(trimmed)}"
    )

    return {
        "messages": trimmed
    }

@before_model
def test_middleware(state, runtime):
    print("Before model")
    print("message:", len(state["messages"]))

    return None


model=create_agent(
    model="openrouter:nvidia/nemotron-3-super-120b-a12b:free",
    tools=[get_info,
           get_order,
           cancel_order,
           check_payment,
           get_user,
           save_memory,
           get_memory,
           search_knowledge_base,
           ],
    system_prompt="you are a costmer suport ai agent at aroku",
    state_schema=MyState,
    context_schema=MyContext,
    checkpointer=InMemorySaver(),
    middleware=[SummarizationMiddleware(
        model="openrouter:google/gemma-4-31b-it:free",
        trigger=("tokens", 10000),
        keep=("tokens",2000)
    ),],
    store=InMemoryStore(),
)